from django.contrib import admin

from apps.wallets.models import BankCard, Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('wallet_number', 'user', 'balance', 'currency', 'status')
    search_fields = ('wallet_number', 'user__username')


@admin.register(BankCard)
class BankCardAdmin(admin.ModelAdmin):
    list_display = ('masked_pan', 'card_holder', 'card_type', 'status', 'user')
    search_fields = ('masked_pan', 'card_holder')
