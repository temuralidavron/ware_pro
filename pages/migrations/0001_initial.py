# Generated by Django 5.1.7 on 2025-03-13 16:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Mahsulot nomi')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Miqdor')),
                ('unit', models.CharField(choices=[('kg', 'Kilogramm'), ('tonna', 'Tonna'), ('metr', 'Metr'), ('dona', 'Dona'), ('litr', 'Litr'), ('oram', 'O‘ram'), ('qop', 'Qop'), ('quti', 'Quti')], default='dona', max_length=10, verbose_name='O‘lchov birligi')),
                ('supplier', models.CharField(max_length=255, verbose_name='Yetkazib beruvchi')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Narx')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan vaqt')),
                ('contract_number', models.CharField(default=0, max_length=255, verbose_name='Shartnoma raqami')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('incoming', 'Kirim'), ('outgoing', 'Chiqim')], max_length=10, verbose_name='Harakat turi')),
                ('quantity', models.PositiveIntegerField(verbose_name='Miqdor')),
                ('person', models.CharField(max_length=255, verbose_name='Kimdan/Kimga')),
                ('contract_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Shartnoma raqami')),
                ('total_sum', models.DecimalField(decimal_places=2, editable=False, max_digits=12, verbose_name='Jami summa')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.product', verbose_name='Mahsulot')),
            ],
        ),
    ]
