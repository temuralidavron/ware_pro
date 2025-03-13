from django import forms
from .models import Product, Transaction
from django import forms
from .models import Product

from django import forms
from .models import Product  # Modelni import qilish
from django import forms
from .models import Product

from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'quantity',
            'price',
            'unit',
            'supplier',
            'contract_number',

        ]
        error_messages = {
            'name': {
                'min_length': "Mahsulot nomi kamida 3 ta harfdan iborat bo‘lishi kerak!",
                'max_length': "Mahsulot nomi juda uzun!",
            },
            'quantity': {
                'min_value': "Miqdor 1 dan kam bo‘lishi mumkin emas!",
            },
            'price': {
                'min_value': "Narx 1 dan kam bo‘lishi mumkin emas!",
            },
            'contract_number': {
                'required': "Shartnoma raqami kiritilishi shart!",
            }
        }

    # 🔥 `name` maydonining unikal bo‘lishini tekshiramiz
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Product.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("❌ Bu nomdagi mahsulot allaqachon mavjud!")
        return name

    # 🔥 `contract_number` unikal bo‘lishini tekshiramiz
    def clean_contract_number(self):
        contract_number = self.cleaned_data.get('contract_number')
        if Product.objects.filter(contract_number=contract_number).exists():
            raise forms.ValidationError("❌ Bu shartnoma raqami allaqachon mavjud!")
        return contract_number


class TransactionForm(forms.Form):
    TRANSACTION_TYPES = [
        ('incoming', 'Kirim'),
        ('outgoing', 'Chiqim')
    ]

    product = forms.ModelChoiceField(
        queryset=Product.objects.none(),
        label="Mahsulot"
    )
    transaction_type = forms.ChoiceField(
        label="Harakat turi",
        choices=TRANSACTION_TYPES
    )
    quantity = forms.IntegerField(
        label="Miqdor",
        min_value=1,
        error_messages={
            'min_value': "Miqdor 1 dan kam bo‘lishi mumkin emas!"
        }
    )
    person = forms.CharField(
        label="Kimdan/Kimga",
        max_length=255
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get("product")
        transaction_type = cleaned_data.get("transaction_type")
        quantity = cleaned_data.get("quantity")

        if transaction_type == "outgoing":
            if not product:
                raise forms.ValidationError("Mahsulotni tanlang!")
            if product.quantity < quantity:
                raise forms.ValidationError(f"Omborda {product.quantity} dona bor. {quantity} so‘ralgan!")

        return cleaned_data



from django import forms
from .models import Product

class UpdateProductForm(forms.ModelForm):
    additional_quantity = forms.IntegerField(
        min_value=1,
        required=True,
        label="Qo'shiladigan miqdor"
    )

    class Meta:
        model = Product
        fields = ['additional_quantity', 'price', 'supplier', 'contract_number']  # Productdan olamiz

    def clean_additional_quantity(self):
        quantity = self.cleaned_data.get('additional_quantity')
        if quantity <= 0:
            raise forms.ValidationError("Qo'shiladigan miqdor musbat bo‘lishi kerak!")
        return quantity


class BulkOutgoingForm(forms.Form):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Chiqim qilinadigan mahsulotlar"
    )
    recipient = forms.CharField(max_length=255, required=True, label="Kimga chiqarildi")
