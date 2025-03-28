
from .forms import ProductForm, TransactionForm
from django.shortcuts import render, get_object_or_404, redirect
from .forms import UpdateProductForm
from django.contrib import messages
from .models import Product, Transaction
from .forms import BulkOutgoingForm
from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

from django.contrib.auth.decorators import login_required

def homeing(request):
    return render(request, 'table.html', {'user_authenticated': request.user.is_authenticated})


# Ro‘yxatdan o‘tish funksiyasi
def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Bu foydalanuvchi allaqachon mavjud!")
            return redirect("register")

        user = User.objects.create_user(username=username, password=password)
        messages.success(request, "Ro‘yxatdan o‘tish muvaffaqiyatli yakunlandi. Endi tizimga kiring.")
        return redirect("login")

    return render(request, "signup.html")


# Login funksiyasi
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")  # Bosh sahifaga yo‘naltiramiz
        else:
            messages.error(request, "Login yoki parol xato!")
            return redirect("login")

    return render(request, "login.html")


def user_logout(request):
    logout(request)
    return redirect("login")
from django.contrib.auth.decorators import login_required



@login_required
def dashboard(request):
    total_products = Product.objects.count()
    total_incoming = Transaction.objects.filter(transaction_type='incoming').count()
    total_outgoing = Transaction.objects.filter(transaction_type='outgoing').count()

    context = {
        'total_products': total_products,
        'total_incoming': total_incoming,
        'total_outgoing': total_outgoing,
    }
    return render(request, 'dashboard.html', context)




# Mahsulot qo‘shish

#
# def create_product(request):
#     if request.method == "POST":
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             form.save()  # ✅ ModelForm bo‘lsa, save() orqali avtomatik saqlanadi
#             return redirect('dashboard')
#     else:
#         form = ProductForm()
#
#     return render(request, 'product_form.html', {'form': form})

def create_product(request):
    """ Yangi mahsulot yaratish """
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)  # Save qilishni kechiktiramiz
            product.total_price = product.quantity * product.price  # ✅ to‘g‘ri hisoblash
            product.save()  # Endi saqlaymiz

            return redirect('dashboard')
    else:
        form = ProductForm()

    return render(request, 'product_form.html', {'form': form})

# Kirim yoki chiqim qo‘shish
def create_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            transaction_type = form.cleaned_data['transaction_type']
            quantity = form.cleaned_data['quantity']
            person = form.cleaned_data['person']

            if transaction_type == "outgoing":
                product.quantity -= quantity
            else:
                product.quantity += quantity

            product.save()
            Transaction.objects.create(
                product=product,
                transaction_type=transaction_type,
                quantity=quantity,
                person=person
            )

            return redirect('dashboard')
    else:
        form = TransactionForm()

    return render(request, 'transaction_form.html', {'form': form})


from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Product

# def product_list(request):
#     products = Product.objects.all().order_by('-created_at')  # Eng oxirgi qo‘shilgan mahsulotlar birinchi chiqadi
#
#     # Sahifalash (Pagination)
#     paginator = Paginator(products, 10)  # Har bir sahifada 10 ta mahsulot bo‘ladi
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     # Har bir mahsulot uchun jami narxni hisoblash
#     for product in page_obj:
#         product.total_price = product.quantity * product.price
#
#     # Faqat shu sahifadagi mahsulotlar uchun umumiy qiymatlarni hisoblash
#     total_quantity = sum(product.quantity for product in page_obj)
#     total_price_sum = sum(product.total_price for product in page_obj)
#
#     context = {
#         'page_obj': page_obj,  # Sahifalangan obyektlar
#         'total_quantity': total_quantity,  # Jami soni
#         'total_price_sum': total_price_sum,  # Umumiy jami summa
#     }
#
#     return render(request, 'product_list.html', context)
#
def product_list(request):
    products = Product.objects.all().order_by('-created_at')  # Eng oxirgi qo‘shilgan mahsulotlar birinchi chiqadi

    # Sahifalash (Pagination)
    paginator = Paginator(products, 10)  # Har bir sahifada 10 ta mahsulot bo‘ladi
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Faqat shu sahifadagi mahsulotlar uchun umumiy qiymatlarni hisoblash
    total_quantity = sum(product.quantity for product in page_obj)
    total_price_sum = sum(product.total_price or 0 for product in page_obj)  # `None` bo‘lsa, 0 qo‘shiladi

    context = {
        'page_obj': page_obj,  # Sahifalangan obyektlar
        'total_quantity': total_quantity,  # Jami soni
        'total_price_sum': total_price_sum,  # Umumiy jami summa
    }

    return render(request, 'product_list.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Transaction
from .forms import UpdateProductForm


# def update_product(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#
#     if request.method == "POST":
#         form = UpdateProductForm(request.POST, instance=product)
#         if form.is_valid():
#             additional_quantity = form.cleaned_data['additional_quantity']
#
#             # Mahsulotni yangilash
#             product.quantity += additional_quantity
#             product.price = form.cleaned_data['price']  # Narxni yangilash
#             product.supplier = form.cleaned_data['supplier']  # Yetkazib beruvchini yangilash
#             product.contract_number = form.cleaned_data['contract_number']  # Shartnoma raqamini yangilash
#             product.save()
#
#             # Tranzaksiya qo'shish
#             Transaction.objects.create(
#                 product=product,
#                 transaction_type='incoming',
#                 quantity=additional_quantity,
#                 person=product.supplier
#             )
#
#             return redirect('dashboard')
#     else:
#         form = UpdateProductForm(instance=product)
#
#     return render(request, 'update_product.html', {'form': form, 'product': product})
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Transaction
from .forms import UpdateProductForm  # Formani loyihaga mos ravishda o‘zgartiring

def update_product(request, product_id):
    """ Mahsulot miqdorini va narxini yangilash """
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = UpdateProductForm(request.POST, instance=product)
        if form.is_valid():
            additional_quantity = form.cleaned_data['additional_quantity']  # ✅ Qo‘shilayotgan miqdor
            new_price = form.cleaned_data['price']  # ✅ Yangilanayotgan narx

            # **Eski jami narxni olish**
            old_total_price = product.total_price if product.total_price else 0  # Agar oldin None bo‘lsa, 0 ga almashtiramiz

            # **Yangi qo‘shilayotgan mahsulot summasi**
            new_total_sum = additional_quantity * new_price

            # **Yangi jami narxni hisoblash**
            new_total_price = old_total_price + new_total_sum

            # **Mahsulotni yangilash**
            product.quantity += additional_quantity  # ✅ Umumiy miqdor oshadi
            product.price = new_price  # ✅ Narx yangilanadi
            product.total_price = new_total_price  # ✅ Yangi jami narx
            product.supplier = form.cleaned_data['supplier']
            product.contract_number = form.cleaned_data['contract_number']
            product.save()

            # ✅ **Yangi tranzaksiya qo‘shish (faqat qo‘shilgan miqdor)**
            Transaction.objects.create(
                product=product,
                transaction_type='incoming',
                quantity=additional_quantity,  # ✅ Faqat qo‘shilgan miqdor
                person=product.supplier,
                contract_number=product.contract_number,
                total_sum=new_total_sum  # ✅ Yangi qo‘shilgan mahsulot qiymati hisoblanadi
            )

            return redirect('dashboard')
    else:
        form = UpdateProductForm(instance=product)

    return render(request, 'update_product.html', {'form': form, 'product': product})

# def bulk_outgoing(request):
#     if request.method == "POST":
#         form = BulkOutgoingForm(request.POST)
#         if form.is_valid():
#             products = request.POST.getlist('products')  # Checkboxda tanlangan mahsulotlar
#             recipient = form.cleaned_data['recipient']
#             quantities = {}
#
#             for product_id in products:
#                 quantity_key = f'quantity_{product_id}'
#                 quantity_value = request.POST.get(quantity_key)
#
#                 if quantity_value:
#                     try:
#                         quantity = int(quantity_value)
#                         if quantity > 0:
#                             quantities[int(product_id)] = quantity
#                         else:
#                             form.add_error(None, "Miqdor 0 dan katta bo‘lishi kerak!")
#                     except ValueError:
#                         form.add_error(None, "Miqdor noto‘g‘ri formatda!")
#
#             if len(products) != len(quantities):
#                 form.add_error(None, "Har bir mahsulot uchun miqdor kiritilishi shart!")
#             else:
#                 for product_id, quantity in quantities.items():
#                     product = Product.objects.get(id=product_id)
#                     if product.quantity < quantity:
#                         form.add_error(None, f"{product.name} uchun omborda yetarli mahsulot yo‘q!")
#                         break
#
#                 if not form.errors:
#                     for product_id, quantity in quantities.items():
#                         product = Product.objects.get(id=product_id)
#                         product.quantity -= quantity
#                         product.save()
#
#                         Transaction.objects.create(
#                             product=product,
#                             transaction_type='outgoing',
#                             quantity=quantity,
#                             person=recipient
#                         )
#
#                     messages.success(request, "Umumiy chiqim muvaffaqiyatli bajarildi!")
#                     return redirect('dashboard')
#
#     else:
#         form = BulkOutgoingForm()
#
#     return render(request, 'bulk_outgoing.html', {'form': form})
# def bulk_outgoing(request):
#     if request.method == "POST":
#         form = BulkOutgoingForm(request.POST)
#         if form.is_valid():
#             products = request.POST.getlist('products')  # Checkboxda tanlangan mahsulotlar
#             recipient = form.cleaned_data['recipient']
#             quantities = {}
#             prices = {}
#
#             for product_id in products:
#                 quantity_key = f'quantity_{product_id}'
#                 price_key = f'price_{product_id}'
#                 quantity_value = request.POST.get(quantity_key)
#                 price_value = request.POST.get(price_key)
#
#                 if quantity_value and price_value:
#                     try:
#                         quantity = int(quantity_value)
#                         price = float(price_value)
#                         if quantity > 0 and price > 0:
#                             quantities[int(product_id)] = quantity
#                             prices[int(product_id)] = price
#                         else:
#                             form.add_error(None, "Miqdor va narx 0 dan katta bo‘lishi kerak!")
#                     except ValueError:
#                         form.add_error(None, "Miqdor yoki narx noto‘g‘ri formatda!")
#
#             if len(products) != len(quantities):
#                 form.add_error(None, "Har bir mahsulot uchun miqdor va narx kiritilishi shart!")
#             else:
#                 for product_id, quantity in quantities.items():
#                     product = Product.objects.get(id=product_id)
#                     if product.quantity < quantity:
#                         form.add_error(None, f"{product.name} uchun omborda yetarli mahsulot yo‘q!")
#                         break
#
#                 if not form.errors:
#                     for product_id, quantity in quantities.items():
#                         product = Product.objects.get(id=product_id)
#                         total_sum = quantity * prices[product_id]
#
#                         if product.total_price < total_sum:
#                             form.add_error(None, f"{product.name} uchun omborda yetarli mablag‘ yo‘q!")
#                             break
#
#                     if not form.errors:
#                         for product_id, quantity in quantities.items():
#                             product = Product.objects.get(id=product_id)
#                             total_sum = quantity * prices[product_id]
#
#                             product.quantity -= int(quantity)
#                             product.total_price -= int(total_sum) # Total summani kamaytirish
#                             product.save()
#
#                             Transaction.objects.create(
#                                 product=product,
#                                 transaction_type='outgoing',
#                                 quantity=quantity,
#                                 person=recipient,
#                                 total_sum=total_sum  # Chiqim summasi
#                             )
#
#                         messages.success(request, "Umumiy chiqim muvaffaqiyatli bajarildi!")
#                         return redirect('dashboard')
#
#     else:
#         form = BulkOutgoingForm()
#
#     return render(request, 'bulk_outgoing.html', {'form': form})
# from decimal import Decimal
#

# def bulk_outgoing(request):
#     if request.method == "POST":
#         form = BulkOutgoingForm(request.POST)
#         if form.is_valid():
#             products = request.POST.getlist('products')  # Checkboxda tanlangan mahsulotlar
#             recipient = form.cleaned_data['recipient']
#             quantities = {}
#             prices = {}
#
#             for product_id in products:
#                 quantity_key = f'quantity_{product_id}'
#                 price_key = f'price_{product_id}'
#                 quantity_value = request.POST.get(quantity_key)
#                 price_value = request.POST.get(price_key)
#
#                 if quantity_value and price_value:
#                     try:
#                         quantity = float(quantity_value)  # ✅ `int` o‘rniga `float`
#                         price = float(price_value)
#                         if quantity > 0 and price > 0:
#                             quantities[int(product_id)] = quantity
#                             prices[int(product_id)] = price
#                         else:
#                             form.add_error(None, "Miqdor va narx 0 dan katta bo‘lishi kerak!")
#                     except ValueError:
#                         form.add_error(None, "Miqdor yoki narx noto‘g‘ri formatda!")
#
#             if len(products) != len(quantities):
#                 form.add_error(None, "Har bir mahsulot uchun miqdor va narx kiritilishi shart!")
#             else:
#                 for product_id, quantity in quantities.items():
#                     product = Product.objects.get(id=product_id)
#                     if product.quantity < quantity:
#                         form.add_error(None, f"{product.name} uchun omborda yetarli mahsulot yo‘q!")
#                         break
#
#                 if not form.errors:
#                     for product_id, quantity in quantities.items():
#                         product = Product.objects.get(id=product_id)
#                         total_sum = quantity * prices[product_id]
#
#                         if product.total_price < total_sum:
#                             form.add_error(None, f"{product.name} uchun omborda yetarli mablag‘ yo‘q!")
#                             break
#
#                     if not form.errors:
#                         for product_id, quantity in quantities.items():
#                             product = Product.objects.get(id=product_id)
#                             total_sum = quantity * prices[product_id]
#
#                             product.quantity -= quantity  # ✅ `int(quantity)` emas, `quantity`
#                             product.total_price -= Decimal(total_sum)  # ✅ `int(total_sum)` emas, `total_sum`
#                             product.save()
#
#                             Transaction.objects.create(
#                                 product=product,
#                                 transaction_type='outgoing',
#                                 quantity=quantity,  # ✅ Float sifatida saqlanadi
#                                 person=recipient,
#                                 total_sum=total_sum  # ✅ Float sifatida saqlanadi
#                             )
#
#                         messages.success(request, "Umumiy chiqim muvaffaqiyatli bajarildi!")
#                         return redirect('dashboard')
#
#     else:
#         form = BulkOutgoingForm()
#
#     return render(request, 'bulk_outgoing.html', {'form': form})

from decimal import Decimal

# def bulk_outgoing(request):
#     if request.method == "POST":
#         form = BulkOutgoingForm(request.POST)
#         if form.is_valid():
#             products = request.POST.getlist('products')  # Checkboxda tanlangan mahsulotlar
#             recipient = form.cleaned_data['recipient']
#             quantities = {}
#             prices = {}
#
#             for product_id in products:
#                 quantity_key = f'quantity_{product_id}'
#                 price_key = f'price_{product_id}'
#                 quantity_value = request.POST.get(quantity_key)
#                 price_value = request.POST.get(price_key)
#
#                 if quantity_value and price_value:
#                     try:
#                         # ✅ Float emas, to‘g‘ridan-to‘g‘ri Decimal ishlatamiz
#                         quantity = Decimal(str(quantity_value))
#                         price = Decimal(str(price_value))
#
#                         if quantity > 0 and price > 0:
#                             quantities[int(product_id)] = quantity
#                             prices[int(product_id)] = price
#                         else:
#                             form.add_error(None, "Miqdor va narx 0 dan katta bo‘lishi kerak!")
#                     except ValueError:
#                         form.add_error(None, "Miqdor yoki narx noto‘g‘ri formatda!")
#
#             if len(products) != len(quantities):
#                 form.add_error(None, "Har bir mahsulot uchun miqdor va narx kiritilishi shart!")
#             else:
#                 products_data = {p.id: p for p in Product.objects.filter(id__in=quantities.keys())}
#
#                 for product_id, quantity in quantities.items():
#                     product = products_data[product_id]
#                     if product.quantity < quantity:
#                         form.add_error(None, f"{product.name} uchun omborda yetarli mahsulot yo‘q!")
#                         break
#
#                 if not form.errors:
#                     for product_id, quantity in quantities.items():
#                         product = products_data[product_id]
#                         total_sum = quantity * prices[product_id]  # ✅ Endi ikkisi ham Decimal
#
#                         if product.total_price < total_sum:
#                             form.add_error(None, f"{product.name} uchun omborda yetarli mablag‘ yo‘q!")
#                             break
#
#                     if not form.errors:
#                         for product_id, quantity in quantities.items():
#                             product = products_data[product_id]
#                             total_sum = quantity * prices[product_id]  # ✅ Ikkisi ham Decimal
#
#                             print(f"Product: {product.name}, total_price: {product.total_price}, total_sum: {total_sum}")  # 🛠 Debug
#
#                             product.quantity -= quantity
#                             product.total_price -= total_sum
#                             product.save()
#
#                             Transaction.objects.create(
#                                 product=product,
#                                 transaction_type='outgoing',
#                                 quantity=quantity,
#                                 person=recipient,
#                                 total_sum=total_sum
#                             )
#
#                         messages.success(request, "Umumiy chiqim muvaffaqiyatli bajarildi!")
#                         return redirect('dashboard')
#
#     else:
#         form = BulkOutgoingForm()
#     print(request.POST)  # 🛠 Debug qilish uchun
#
#     return render(request, 'bulk_outgoing.html', {'form': form})

from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Transaction
from .forms import BulkOutgoingForm

def bulk_outgoing(request):
    if request.method == "POST":
        form = BulkOutgoingForm(request.POST)

        if form.is_valid():
            products = request.POST.getlist('products')  # ✅ Tanlangan mahsulotlar IDlari
            recipient = form.cleaned_data['recipient']
            quantities, prices = {}, {}

            # 🔹 Mahsulot miqdori va narxini to‘plash
            for product_id in products:
                quantity = request.POST.get(f'quantity_{product_id}')
                price = request.POST.get(f'price_{product_id}', '0')  # ✅ Agar yo‘q bo‘lsa, '0' bo‘lsin

                if not quantity:
                    form.add_error(None, "Har bir mahsulot uchun miqdor kiritilishi shart!")
                    continue

                try:
                    quantity = Decimal(quantity)
                    price = Decimal(price) if price not in [None, ''] else Decimal(0)  # ✅ None bo‘lsa, 0 qilish

                    if quantity <= 0:
                        form.add_error(None, "Miqdor 0 dan katta bo‘lishi kerak!")
                        continue

                    quantities[int(product_id)] = quantity
                    prices[int(product_id)] = price

                except ValueError:
                    form.add_error(None, "Miqdor yoki narx noto‘g‘ri formatda!")

            # 🔹 Agar xatolik bo‘lsa, qaytariladi
            if form.errors:
                return render(request, 'bulk_outgoing.html', {'form': form})

            # 🔹 Mahsulotlar bazadan olinadi
            products_data = {p.id: p for p in Product.objects.filter(id__in=quantities.keys())}

            # 🔹 Omborda yetarli mahsulot borligini tekshirish
            for product_id, quantity in quantities.items():
                product = products_data.get(product_id)
                if not product:
                    form.add_error(None, f"Mahsulot (ID: {product_id}) topilmadi!")
                    continue

                if product.quantity < quantity:
                    form.add_error(None, f"{product.name} uchun omborda yetarli mahsulot yo‘q!")
                    continue

            # 🔹 Agar xatolik bo‘lsa, yana qaytariladi
            if form.errors:
                return render(request, 'bulk_outgoing.html', {'form': form})

            # 🔹 Ombordan mahsulotlarni chiqarish
            for product_id, quantity in quantities.items():
                product = products_data[product_id]
                price = prices.get(product_id, Decimal(0))  # ✅ Agar `price` None bo‘lsa, 0 qilib olish

                total_sum = quantity * price if price > 0 else Decimal(0)  # ✅ Endi hech qachon None bo‘lmaydi

                product.quantity -= quantity

                # 🔹 Faqat `price > 0` bo‘lsa, `total_price` kamayadi
                if product.price and product.price > 0:  # ✅ `None` bo‘lish ehtimoli yo‘q qilindi
                    product.total_price -= total_sum

                product.save()

                Transaction.objects.create(
                    product=product,
                    transaction_type='outgoing',
                    quantity=quantity,
                    person=recipient,
                    total_sum=total_sum  # ✅ price 0 bo‘lsa ham ishlaydi
                )

            messages.success(request, "Umumiy chiqim muvaffaqiyatli bajarildi!")
            return redirect('dashboard')

    else:
        form = BulkOutgoingForm()

    return render(request, 'bulk_outgoing.html', {'form': form})




def outgoing_list(request):
    incoming_transactions = Transaction.objects.filter(transaction_type='outgoing')

    # Har bir mahsulot uchun jami narxni hisoblash
    for transaction in incoming_transactions:
        transaction.total_price = transaction.quantity * transaction.product.price

    # Umumiy kirim summasini hisoblash
    total_incoming = sum(transaction.total_price for transaction in incoming_transactions)

    context = {
        'incoming_transactions': incoming_transactions,
        'total_incoming': total_incoming,
    }
    return render(request, 'outgoing_list.html', context)



def incoming_transactions_list(request):
    incoming_transactions = Transaction.objects.filter(transaction_type='incoming')

    # Har bir mahsulot uchun jami narxni hisoblash
    for transaction in incoming_transactions:
        transaction.total_price = transaction.quantity * transaction.product.price

    # Umumiy kirim summasini hisoblash
    total_incoming = sum(transaction.total_price for transaction in incoming_transactions)

    context = {
        'incoming_transactions': incoming_transactions,
        'total_incoming': total_incoming,
    }
    return render(request, 'incoming_transactions.html', context)


import openpyxl
from django.http import HttpResponse
from .models import Transaction

def export_outgoing_to_excel(request):
    # Yangi Excel fayl yaratamiz
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Chiqimlar"

    # Ustun sarlavhalari
    headers = ["#", "Mahsulot", "Miqdor", "Kimga", "Sana"]
    ws.append(headers)

    # Chiqimlarni olish
    outgoing_transactions = Transaction.objects.filter(transaction_type='outgoing')

    for index, transaction in enumerate(outgoing_transactions, start=1):
        ws.append([
            index,
            transaction.product.name,
            f"{transaction.quantity} {transaction.product.unit}",
            transaction.person,
            # transaction.created_at.strftime("%Y-%m-%d %H:%M") if transaction.created_at else "",
        ])

    # Javob qaytarish
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="chiqimlar.xlsx"'

    wb.save(response)
    return response



from django.shortcuts import render
from django.db.models import Sum
from django.utils.timezone import now
from datetime import datetime
from .models import Product, Transaction

def warehouse_report(request):
    # Foydalanuvchi tanlagan oy (URL query orqali)
    month = request.GET.get('month', now().strftime('%Y-%m'))  # Default: joriy oy

    # Tanlangan oy bo‘yicha filter
    start_date = datetime.strptime(month, "%Y-%m")
    end_date = datetime(start_date.year, start_date.month + 1, 1) if start_date.month < 12 else datetime(start_date.year + 1, 1, 1)

    # O‘sha oyda omborda bo‘lgan mahsulotlar
    transactions = Transaction.objects.filter(created_at__gte=start_date, created_at__lt=end_date)

    # Mahsulotlar bo‘yicha umumiy miqdor va jami summa
    warehouse_data = transactions.values('product__name', 'product__unit').annotate(
        total_quantity=Sum('quantity'),
        total_sum=Sum('total_sum')
    )

    # Ombordagi umumiy qiymat
    total_value = transactions.aggregate(Sum('total_sum'))['total_sum__sum'] or 0

    # Mavjud oylar ro‘yxati
    months = Transaction.objects.dates('created_at', 'month', order='DESC')

    context = {
        'warehouse_data': warehouse_data,
        'total_value': total_value,
        'months': months,
        'selected_month': month
    }

    return render(request, 'warehouse_report.html', context)


import json
from django.shortcuts import render
from .models import Product

import json
from django.shortcuts import render
from .models import Product

def dashboard_view(request):
    products = Product.objects.all()

    # Statistik ma'lumotlarni yig‘ish
    labels = [product.name for product in products]
    data = [product.quantity for product in products]

    context = {
        'total_products': products.count(),
        'total_incoming': 12,  # Bu qiymatni kerakli joydan oling
        'total_outgoing': 10,   # Bu qiymatni kerakli joydan oling
        'labels': json.dumps(labels),
        'data': json.dumps(data),
    }

    return render(request, 'dashboard.html', context)


# loyiha ishlamoqd