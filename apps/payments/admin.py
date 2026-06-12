from django.contrib import admin

from apps.payments.models import FavoritePayment, Payment, PaymentCategory, ServiceProvider


@admin.register(PaymentCategory)
class PaymentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')


@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'min_amount', 'max_amount', 'is_active')
    list_filter = ('category', 'is_active')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('provider', 'amount', 'status', 'user', 'created_at')
    list_filter = ('status',)


@admin.register(FavoritePayment)
class FavoritePaymentAdmin(admin.ModelAdmin):
    list_display = ('title', 'provider', 'user', 'account_number')
