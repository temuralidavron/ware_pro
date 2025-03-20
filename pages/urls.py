from django.urls import path
from .views import dashboard, create_product, create_transaction, product_list, update_product, bulk_outgoing, \
    outgoing_list, export_outgoing_to_excel, incoming_transactions_list, warehouse_report, dashboard_view, user_login, \
    user_logout, user_register

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('product/create/', create_product, name='create_product'),
    path('transaction/create/', create_transaction, name='create_transaction'),
    path('products/', product_list, name='product_list'),
    path('update-product/<int:product_id>/', update_product, name='update_product'),
    path('bulk-outgoing/', bulk_outgoing, name='bulk_outgoing'),
    path('chiqimlar/', outgoing_list, name='outgoing_list'),
    path('kirimlar/', incoming_transactions_list, name='incoming_list'),
    path('warehouse-report/', warehouse_report, name='warehouse_report'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('chiqimlar/excel/', export_outgoing_to_excel, name='export_outgoing_to_excel'),
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path("logout/", user_logout, name="logout"),

]
