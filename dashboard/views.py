from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
import json

from orders.models import Order
from products.models import Product, Category
from invoices.models import Invoice
from .models import Expense
from .forms import ExpenseForm


@staff_member_required
def dashboard_home(request):
    """Main admin dashboard"""
    now = timezone.now()
    this_month_start = now.replace(day=1, hour=0, minute=0, second=0)

    # ---- Key Metrics ----
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    pending_orders = Order.objects.filter(status='pending').count()
    paid_orders = Order.objects.filter(payment_status='paid').count()
    this_month_orders = Order.objects.filter(created_at__gte=this_month_start).count()
    this_month_revenue = Order.objects.filter(
        created_at__gte=this_month_start
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    # ---- Recent Orders ----
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]

    # ---- Low Stock Products ----
    low_stock_products = Product.objects.filter(is_active=True, stock__lte=5).order_by('stock')[:10]

    # ---- Monthly Sales Chart Data (last 6 months) ----
    six_months_ago = now - timedelta(days=180)
    monthly_data = (
        Order.objects
        .filter(created_at__gte=six_months_ago)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(revenue=Sum('total_amount'), count=Count('id'))
        .order_by('month')
    )

    chart_labels = []
    chart_revenue = []
    chart_orders = []
    for entry in monthly_data:
        chart_labels.append(entry['month'].strftime('%b %Y'))
        chart_revenue.append(float(entry['revenue']))
        chart_orders.append(entry['count'])

    # ---- Expense Tracking ----
    total_expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    net_profit = float(total_revenue) - float(total_expenses)
    recent_expenses = Expense.objects.order_by('-date')[:5]

    # ---- Order Status Distribution ----
    status_counts = dict(
        Order.objects.values('status').annotate(count=Count('id')).values_list('status', 'count')
    )

    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'pending_orders': pending_orders,
        'paid_orders': paid_orders,
        'this_month_orders': this_month_orders,
        'this_month_revenue': this_month_revenue,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
        'total_expenses': total_expenses,
        'net_profit': net_profit,
        'recent_expenses': recent_expenses,
        'chart_labels': json.dumps(chart_labels),
        'chart_revenue': json.dumps(chart_revenue),
        'chart_orders': json.dumps(chart_orders),
        'status_counts': json.dumps(status_counts),
    }
    return render(request, 'dashboard/home.html', context)


@staff_member_required
def inventory_management(request):
    """Product inventory view"""
    products = Product.objects.select_related('category').order_by('stock')
    categories = Category.objects.all()
    low_stock = products.filter(stock__lte=5)
    out_of_stock = products.filter(stock=0)
    context = {
        'products': products,
        'categories': categories,
        'low_stock_count': low_stock.count(),
        'out_of_stock_count': out_of_stock.count(),
    }
    return render(request, 'dashboard/inventory.html', context)


@staff_member_required
def expense_list(request):
    """List and add expenses"""
    expenses = Expense.objects.all().order_by('-date')
    form = ExpenseForm()
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.added_by = request.user
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('expense_list')
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    context = {'expenses': expenses, 'form': form, 'total': total}
    return render(request, 'dashboard/expenses.html', context)


@staff_member_required
def expense_delete(request, pk):
    """Delete expense"""
    expense = get_object_or_404(Expense, pk=pk)
    expense.delete()
    messages.success(request, 'Expense deleted.')
    return redirect('expense_list')


@staff_member_required
def reports(request):
    """Revenue and expense reports"""
    from django.db.models.functions import TruncMonth
    monthly_revenue = (
        Order.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(revenue=Sum('total_amount'), orders=Count('id'))
        .order_by('-month')[:12]
    )
    monthly_expenses = (
        Expense.objects
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('-month')[:12]
    )

    # Build combined report
    report_data = []
    revenue_by_month = {entry['month']: entry for entry in monthly_revenue}
    expense_by_month = {entry['month']: entry['total'] for entry in monthly_expenses}
    all_months = sorted(set(list(revenue_by_month.keys()) + list(expense_by_month.keys())), reverse=True)

    for month in all_months:
        rev_data = revenue_by_month.get(month, {'revenue': 0, 'orders': 0})
        exp = expense_by_month.get(month, 0)
        report_data.append({
            'month': month,
            'revenue': rev_data['revenue'],
            'orders': rev_data['orders'],
            'expenses': exp,
            'profit': float(rev_data['revenue']) - float(exp),
        })

    context = {'report_data': report_data}
    return render(request, 'dashboard/reports.html', context)
