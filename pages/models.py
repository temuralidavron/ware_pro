from django.db import models
from decimal import Decimal

class MeasurementUnit(models.TextChoices):
    KG = 'kg', 'Kilogramm'
    TONNA = 'tonna', 'Tonna'
    METR = 'metr', 'Metr'
    DONA = 'dona', 'Dona'
    LITR = 'litr', 'Litr'
    ORAM = 'oram', 'O‘ram'
    QOP = 'qop', 'Qop'
    QUTI = 'quti', 'Quti'
    GRAMM='gramm','Gramm'

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Mahsulot nomi")
    quantity = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), verbose_name="Miqdor")  # 🔥 DecimalField
    unit = models.CharField(
        max_length=10,
        choices=MeasurementUnit.choices,
        default=MeasurementUnit.DONA,
        verbose_name="O‘lchov birligi"
    )
    supplier = models.CharField(max_length=255, verbose_name="Yetkazib beruvchi")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name="Narx")  # 🔥 DecimalField
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")  # Qo‘shildi
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")  # Qo‘shildi
    contract_number = models.CharField(max_length=255, verbose_name="Shartnoma raqami",default=0)  # 🔥 Qo‘shildi
    total_price = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))

    def save(self, *args, **kwargs):
        # ✅ Agar total_price None bo‘lsa, uni hisoblab chiqamiz
        if self.total_price is None:
            self.total_price = self.price * self.quantity

        is_new = self.pk is None  # Ob'ekt yangi yaratilayaptimi yoki yo‘q?

        super().save(*args, **kwargs)  # **Asosiy saqlashni bajaramiz**

        # ✅ Har safar yangi Transaction yaratamiz
        Transaction.objects.create(
            product=self,
            transaction_type='incoming',
            quantity=self.quantity,
            person=self.supplier,
            contract_number=self.contract_number,
            total_sum=self.total_price
        )
    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('incoming', 'Kirim'),
        ('outgoing', 'Chiqim'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Mahsulot")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, verbose_name="Harakat turi")
    quantity = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), verbose_name="Miqdor")  # 🔥 DecimalField
    person = models.CharField(max_length=255, verbose_name="Kimdan/Kimga")
    contract_number = models.CharField(max_length=50, verbose_name="Shartnoma raqami", blank=True, null=True)  # Qo‘shildi
    total_sum = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Jami summa", editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")  # Qo‘shildi

    def save(self, *args, **kwargs):
        """ Narx va miqdordan jami summani hisoblab yozib qo‘yamiz """
        self.total_sum = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} ({self.transaction_type})"


class Proba(models.Model):
    name = models.CharField(max_length=50)

