from django.db import models

class MeasurementUnit(models.TextChoices):
    KG = 'kg', 'Kilogramm'
    TONNA = 'tonna', 'Tonna'
    METR = 'metr', 'Metr'
    DONA = 'dona', 'Dona'
    LITR = 'litr', 'Litr'
    ORAM = 'oram', 'O‘ram'
    QOP = 'qop', 'Qop'
    QUTI = 'quti', 'Quti'

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Mahsulot nomi")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Miqdor")
    unit = models.CharField(
        max_length=10,
        choices=MeasurementUnit.choices,
        default=MeasurementUnit.DONA,
        verbose_name="O‘lchov birligi"
    )
    supplier = models.CharField(max_length=255, verbose_name="Yetkazib beruvchi")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narx", default=0)  # Qo‘shildi
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")  # Qo‘shildi
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")  # Qo‘shildi
    contract_number = models.CharField(max_length=255, verbose_name="Shartnoma raqami",default=0)  # 🔥 Qo‘shildi

    def save(self, *args, **kwargs):
        """ Mahsulot saqlanganda tranzaksiya ham yaratiladi """
        is_new = self.pk is None  # 🔥 Mahsulot yangi yaratilayotganini tekshiramiz
        super().save(*args, **kwargs)  # Asosiy saqlash

        if is_new:  # Faqat yangi mahsulot qo‘shilganda ishlaydi
            Transaction.objects.create(
                product=self,
                transaction_type='incoming',  # Kirim tranzaksiya
                quantity=self.quantity,
                person=self.supplier,
                contract_number=self.contract_number,  # 🔥 Majburiy maydon
                total_sum=self.quantity * self.price
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
    quantity = models.PositiveIntegerField(verbose_name="Miqdor")
    person = models.CharField(max_length=255, verbose_name="Kimdan/Kimga")
    contract_number = models.CharField(max_length=50, verbose_name="Shartnoma raqami", blank=True, null=True)  # Qo‘shildi
    total_sum = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Jami summa", editable=False)  # Qo‘shildi
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")  # Qo‘shildi

    def save(self, *args, **kwargs):
        """ Narx va miqdordan jami summani hisoblab yozib qo‘yamiz """
        self.total_sum = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} ({self.transaction_type})"


class Proba(models.Model):
    name = models.CharField(max_length=50)