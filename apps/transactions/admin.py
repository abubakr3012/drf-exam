from django.contrib import admin

from apps.transactions.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'amount', 'status', 'currency', 'created_at')
    list_filter = ('transaction_type', 'status', 'currency')
    search_fields = ('description',)
