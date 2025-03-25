from django.contrib import admin
from .models import Product, Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('product', 'transaction_type', 'quantity', 'person', 'contract_number', 'total_sum', 'created_at')  # Ko‘rinadigan ustunlar
    list_filter = ('transaction_type', 'created_at')  # **Kirim va chiqim bo‘yicha filter**
    search_fields = ('product__name', 'person', 'contract_number')  # **Qidirish uchun ustunlar**
    date_hierarchy = 'created_at'  # **Sana bo‘yicha filter qo‘shish**

admin.site.register(Product)
