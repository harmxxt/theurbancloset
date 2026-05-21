from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import FileResponse, Http404
from .models import Invoice
from orders.models import Order


@login_required
def invoice_detail(request, invoice_number):
    invoice = get_object_or_404(Invoice, invoice_number=invoice_number)
    # Customers can only view their own invoices
    if not request.user.is_staff and invoice.order.user != request.user:
        raise Http404
    return render(request, 'invoices/invoice_detail.html', {'invoice': invoice})


@login_required
def download_invoice(request, invoice_number):
    invoice = get_object_or_404(Invoice, invoice_number=invoice_number)
    if not request.user.is_staff and invoice.order.user != request.user:
        raise Http404

    if invoice.pdf_file:
        return FileResponse(
            invoice.pdf_file.open('rb'),
            as_attachment=True,
            filename=f'Invoice_{invoice.invoice_number}.pdf',
            content_type='application/pdf',
        )

    # PDF not yet generated — regenerate on the fly
    try:
        from .services import generate_invoice_pdf
        from django.http import HttpResponse
        pdf_buf = generate_invoice_pdf(invoice)
        response = HttpResponse(pdf_buf.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Invoice_{invoice.invoice_number}.pdf"'
        return response
    except Exception:
        raise Http404("Invoice PDF is not available.")


@staff_member_required
def admin_invoice_list(request):
    invoices = Invoice.objects.select_related('order').order_by('-created_at')
    return render(request, 'invoices/admin_invoice_list.html', {'invoices': invoices})


@staff_member_required
def manually_create_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    from .services import create_invoice_for_order
    create_invoice_for_order(order)
    return redirect('admin_invoice_list')
