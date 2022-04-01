from django.contrib import admin

from .models import Account, Currency, Transaction


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'symbol')

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'initial_amount', 'currency')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'type',
                    'from_account', 'from_amount', 'from_currency',
                    'to_account', 'to_amount', 'to_currency',
                    'fee_amount', 'fee_currency')

    fields = ['date', 'type',
                    'from_account', 'from_amount', 'from_currency',
                    'to_account', 'to_amount', 'to_currency',
                    'fee_amount', 'fee_currency']

# @admin.register(Expense)
# class ExpenseAdmin(admin.ModelAdmin):
#     list_display = ('id', 'date',
#                     'from_account', 'from_amount', 'from_currency',
#                     'to_amount', 'to_currency')

#     fields = ['date',
#               'from_account', 'from_amount', 'from_currency',
#               'to_amount', 'to_currency']

#     def get_queryset(self, *args, **kwargs):
#         return Transaction.objects.filter(type='expense')
