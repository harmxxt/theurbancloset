from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=50, unique=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('issued', 'Issued'), ('paid', 'Paid'), ('cancelled', 'Cancelled')], default='issued', max_length=20)),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='invoices/')),
                ('pdf_generated', models.BooleanField(default=False)),
                ('email_sent', models.BooleanField(default=False)),
                ('issued_date', models.DateField(auto_now_add=True)),
                ('due_date', models.DateField(null=True, blank=True)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to='orders.order')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
