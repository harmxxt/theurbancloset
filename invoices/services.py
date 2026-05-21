"""
TheUrbanCloset — Invoice Services
Pipeline: Create Invoice → Generate PDF → Email
"""

import os, io, logging
from datetime import date, timedelta
from django.conf import settings
from django.core.mail import EmailMessage

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle,
    Paragraph, Spacer, HRFlowable, KeepTogether,
)

logger = logging.getLogger(__name__)

# ── Colours ────────────────────────────────────────────────────────────────────
GOLD    = HexColor('#C9A96E')
INK     = HexColor('#1A1A1A')
STEEL   = HexColor('#555555')
MIST    = HexColor('#999999')
PAPER   = HexColor('#F9F6F1')
RULE    = HexColor('#E0D8CC')
WHITE_H = HexColor('#FFFFFF')

def _rs(amount):
    try:
        return f"Rs.{float(amount):,.2f}"
    except Exception:
        return f"Rs.{amount}"

def _p(text, size=9, bold=False, color=INK, align=TA_LEFT, leading=None):
    return Paragraph(str(text), ParagraphStyle(
        'x',
        fontName  = 'Helvetica-Bold' if bold else 'Helvetica',
        fontSize  = size,
        textColor = color,
        alignment = align,
        leading   = leading or (size * 1.4),
        wordWrap  = 'CJK',
    ))

# ── Main orchestration ─────────────────────────────────────────────────────────
def create_invoice_for_order(order):
    from .models import Invoice

    invoice, _ = Invoice.objects.get_or_create(
        order=order,
        defaults={
            'status'  : 'paid' if order.payment_status == 'paid' else 'issued',
            'due_date': date.today() + timedelta(days=7),
        }
    )

    # 1. Generate PDF
    try:
        pdf_buf = generate_invoice_pdf(invoice)
        from django.core.files.base import ContentFile
        invoice.pdf_file.save(
            f"invoice_{invoice.invoice_number}.pdf",
            ContentFile(pdf_buf.getvalue()),
            save=False,
        )
        invoice.pdf_generated = True
    except Exception as e:
        logger.error(f"PDF generation failed [{invoice.invoice_number}]: {e}")
        invoice.save()
        return invoice

    invoice.save()

    # 2. Email
    try:
        send_invoice_email(invoice, pdf_buf)
        invoice.email_sent = True
        invoice.save()
    except Exception as e:
        logger.error(f"Email failed [{invoice.invoice_number}]: {e}")

    return invoice


# ── PDF generation ─────────────────────────────────────────────────────────────
def generate_invoice_pdf(invoice):
    order  = invoice.order
    buf    = io.BytesIO()

    PAGE_W, PAGE_H = A4
    LM = RM = 18 * mm
    TM = BM = 18 * mm
    IW = PAGE_W - LM - RM

    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=LM, rightMargin=RM,
        topMargin=TM,  bottomMargin=BM,
        title=f"Invoice {invoice.invoice_number}",
    )

    story = []

    SNAME = getattr(settings, 'STORE_NAME',    'TheUrbanCloset')
    SADDR = getattr(settings, 'STORE_ADDRESS', '12 Urban Lane, Mumbai 400001')
    STEL  = getattr(settings, 'STORE_PHONE',   '+91 98765 43210')
    SMAIL = getattr(settings, 'STORE_EMAIL',   'hello@theurbancloset.in')
    PAID  = 'PAID' if order.payment_status == 'paid' else 'PENDING'

    # 1. HEADER
    hdr = Table(
        [[
            _p('THE URBAN CLOSET', size=22, bold=True, color=GOLD),
            _p('INVOICE', size=22, bold=True, color=INK, align=TA_RIGHT),
        ]],
        colWidths=[IW * 0.55, IW * 0.45],
    )
    hdr.setStyle(TableStyle([
        ('VALIGN',        (0,0), (-1,-1), 'BOTTOM'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING',    (0,0), (-1,-1), 0),
    ]))
    story.append(hdr)
    story.append(_p('Urban Fashion — Style for Every Street', size=8, color=MIST))
    story.append(Spacer(1, 2*mm))
    story.append(HRFlowable(width='100%', thickness=2, color=GOLD, spaceAfter=4))

    # 2. META
    meta = Table(
        [[
            Paragraph(
                f'<b>{SNAME}</b><br/>{SADDR}<br/>{STEL}<br/>{SMAIL}',
                ParagraphStyle('sl', fontName='Helvetica', fontSize=8,
                               textColor=STEEL, leading=13),
            ),
            Paragraph(
                f'<b>Invoice No :</b> {invoice.invoice_number}<br/>'
                f'<b>Order No   :</b> {order.order_number}<br/>'
                f'<b>Date       :</b> {invoice.issued_date.strftime("%d %B %Y")}<br/>'
                f'<b>Status     :</b> {PAID}',
                ParagraphStyle('mr', fontName='Helvetica', fontSize=8,
                               textColor=STEEL, leading=14,
                               alignment=TA_RIGHT),
            ),
        ]],
        colWidths=[IW * 0.55, IW * 0.45],
    )
    meta.setStyle(TableStyle([
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta)
    story.append(Spacer(1, 3*mm))

    # 3. BILLED TO
    story.append(_p('BILLED TO', size=8, bold=True, color=GOLD))
    story.append(HRFlowable(width='100%', thickness=0.6, color=GOLD, spaceBefore=2, spaceAfter=4))

    billed = Table(
        [[
            Paragraph(
                f'<b>{order.full_name}</b><br/>'
                f'{order.get_full_address()}<br/>'
                f'Ph: {order.phone}  &nbsp; Email: {order.email}',
                ParagraphStyle('bl', fontName='Helvetica', fontSize=8,
                               textColor=STEEL, leading=13),
            ),
            Paragraph(
                f'<b>Payment Method:</b> {order.get_payment_method_display()}<br/>'
                f'<b>Payment Status:</b> {PAID}',
                ParagraphStyle('br', fontName='Helvetica', fontSize=8,
                               textColor=STEEL, leading=13,
                               alignment=TA_RIGHT),
            ),
        ]],
        colWidths=[IW * 0.60, IW * 0.40],
    )
    billed.setStyle(TableStyle([
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(billed)

    # 4. ITEMS TABLE
    C_NO   =  8 * mm
    C_SIZE = 16 * mm
    C_QTY  = 12 * mm
    C_UPRC = 34 * mm
    C_TOT  = 34 * mm
    C_PROD = IW - C_NO - C_SIZE - C_QTY - C_UPRC - C_TOT
    col_widths = [C_NO, C_PROD, C_SIZE, C_QTY, C_UPRC, C_TOT]

    def _th(txt, align=TA_CENTER):
        return Paragraph(txt, ParagraphStyle(
            'th', fontName='Helvetica-Bold', fontSize=8.5,
            textColor=WHITE_H, alignment=align, leading=12,
        ))

    rows = [[
        _th('#'),
        _th('Product Description', align=TA_LEFT),
        _th('Size'),
        _th('Qty'),
        _th('Unit Price', align=TA_RIGHT),
        _th('Total', align=TA_RIGHT),
    ]]

    items = list(order.items.all())
    for idx, item in enumerate(items, 1):
        try:
            cat_name = item.product.category.name
        except Exception:
            cat_name = ''

        prod_para = Paragraph(
            f'<b>{item.product_name}</b>'
            + (f'<br/><font size="7" color="#999999">{cat_name}</font>' if cat_name else ''),
            ParagraphStyle('pn', fontName='Helvetica', fontSize=8.5, leading=12, textColor=INK),
        )

        def _cv(t, bold=False, align=TA_CENTER):
            return Paragraph(str(t), ParagraphStyle(
                'cv', fontName='Helvetica-Bold' if bold else 'Helvetica',
                fontSize=8.5, alignment=align, leading=12, textColor=INK,
            ))

        rows.append([
            _cv(str(idx)),
            prod_para,
            _cv(item.size or '—'),
            _cv(str(item.quantity)),
            _cv(_rs(item.product_price), align=TA_RIGHT),
            _cv(_rs(item.get_subtotal()), bold=True, align=TA_RIGHT),
        ])

    ts = TableStyle([
        ('BACKGROUND',    (0, 0), (-1,  0), INK),
        ('TEXTCOLOR',     (0, 0), (-1,  0), WHITE_H),
        ('FONTNAME',      (0, 0), (-1,  0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1,  0), 8.5),
        ('TOPPADDING',    (0, 0), (-1,  0), 7),
        ('BOTTOMPADDING', (0, 0), (-1,  0), 7),
        ('FONTSIZE',      (0, 1), (-1, -1), 8.5),
        ('TOPPADDING',    (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING',   (0, 0), (-1, -1), 5),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 5),
        ('LINEBELOW',     (0, 0), (-1, -1), 0.4, RULE),
        *[('BACKGROUND',  (0, r), (-1, r), PAPER if r % 2 == 0 else WHITE_H)
          for r in range(1, len(rows))],
    ])

    item_tbl = Table(rows, colWidths=col_widths, repeatRows=1)
    item_tbl.setStyle(ts)
    story.append(KeepTogether(item_tbl))
    story.append(Spacer(1, 4*mm))

    # 5. TOTALS BLOCK
    GAP   = IW * 0.48
    LBL_W = 48 * mm
    VAL_W = IW - GAP - LBL_W

    def _tr(label, value, grand=False):
        lbl_style = ParagraphStyle(
            'tl', fontName='Helvetica-Bold' if grand else 'Helvetica',
            fontSize=10 if grand else 8.5,
            textColor=WHITE_H if grand else STEEL,
            alignment=TA_RIGHT, leading=14,
        )
        val_style = ParagraphStyle(
            'tv', fontName='Helvetica-Bold',
            fontSize=11 if grand else 9,
            textColor=WHITE_H if grand else INK,
            alignment=TA_RIGHT, leading=14,
        )
        return [Paragraph('', ParagraphStyle('g')),
                Paragraph(label, lbl_style),
                Paragraph(value, val_style)]

    totals = Table(
        [
            _tr('Subtotal',        _rs(order.subtotal)),
            _tr('Tax (18% GST)',   _rs(order.tax_amount)),
            _tr('Delivery Charge', _rs(order.delivery_charge)),
            _tr('GRAND TOTAL',     _rs(order.total_amount), grand=True),
        ],
        colWidths=[GAP, LBL_W, VAL_W],
    )
    totals.setStyle(TableStyle([
        ('ALIGN',         (0,0), (-1,-1), 'RIGHT'),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0), (-1, 2), 4),
        ('BOTTOMPADDING', (0,0), (-1, 2), 4),
        ('RIGHTPADDING',  (0,0), (-1,-1), 6),
        ('LINEABOVE',     (1,3), (-1, 3), 1.5, GOLD),
        ('BACKGROUND',    (1,3), (-1, 3), INK),
        ('TOPPADDING',    (1,3), (-1, 3), 8),
        ('BOTTOMPADDING', (1,3), (-1, 3), 8),
        ('LEFTPADDING',   (1,3), (-1, 3), 10),
        ('RIGHTPADDING',  (1,3), (-1, 3), 10),
    ]))
    story.append(totals)
    story.append(Spacer(1, 6*mm))

    # 6. NOTES
    if order.notes and order.notes.strip():
        story.append(_p('NOTES', size=8, bold=True, color=GOLD))
        story.append(HRFlowable(width='100%', thickness=0.5, color=RULE, spaceAfter=3))
        story.append(_p(order.notes, size=8, color=STEEL))
        story.append(Spacer(1, 4*mm))

    # 7. FOOTER
    story.append(HRFlowable(width='100%', thickness=1.5, color=GOLD, spaceBefore=2, spaceAfter=5))
    story.append(Paragraph(
        f'Thank you for shopping with {SNAME}  |  '
        f'{SMAIL}  |  {STEL}  |  '
        f'Computer-generated invoice — no signature required.',
        ParagraphStyle('ft', fontName='Helvetica', fontSize=7.5,
                       textColor=MIST, alignment=TA_CENTER, leading=11),
    ))

    doc.build(story)
    buf.seek(0)
    return buf


# ── Email ──────────────────────────────────────────────────────────────────────
def send_invoice_email(invoice, pdf_buffer):
    order  = invoice.order
    status = 'Paid' if order.payment_status == 'paid' else 'Pending'
    SNAME  = getattr(settings, 'STORE_NAME',  'TheUrbanCloset')
    SMAIL  = getattr(settings, 'STORE_EMAIL', 'hello@theurbancloset.in')
    STEL   = getattr(settings, 'STORE_PHONE', '+91 98765 43210')

    msg = EmailMessage(
        subject    = f'Your {SNAME} Invoice — {invoice.invoice_number}',
        body       = (
            f"Dear {order.full_name},\n\n"
            f"Thank you for your order! Your invoice is attached.\n\n"
            f"Order No   : {order.order_number}\n"
            f"Invoice No : {invoice.invoice_number}\n"
            f"Total      : {_rs(order.total_amount)}\n"
            f"Payment    : {order.get_payment_method_display()} — {status}\n\n"
            f"Delivery to: {order.get_full_address()}\n\n"
            f"Questions? Contact us at {SMAIL}\n\n"
            f"Warm regards,\nThe {SNAME} Team\n{STEL}"
        ),
        from_email = settings.DEFAULT_FROM_EMAIL,
        to         = [order.email],
    )
    pdf_buffer.seek(0)
    msg.attach(
        filename = f'Invoice_{invoice.invoice_number}.pdf',
        content  = pdf_buffer.read(),
        mimetype = 'application/pdf',
    )
    msg.send(fail_silently=False)
