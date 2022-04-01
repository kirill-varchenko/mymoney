from decimal import Decimal
from locale import currency
from typing import Any, Optional

from django.db import models


class Currency(models.Model):
    id = models.CharField(primary_key=True, max_length=3)
    symbol = models.CharField(max_length=1)

    class Meta:
        db_table = "content\".\"currency"

    def __str__(self) -> str:
        return self.id

class Account(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    currency = models.ForeignKey('Currency', blank=False, on_delete=models.PROTECT)
    initial_amount = models.DecimalField(default=0, max_digits=19, decimal_places=2)

    class Meta:
        db_table = "content\".\"account"

    def __str__(self) -> str:
        return f"{self.name} ({self.currency})"

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('expense', 'Expense'),
        ('income', 'Income'),
        ('transfer', 'Transfer')
    )
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=10, blank=False, choices=TRANSACTION_TYPES)
    date = models.DateField(blank=False, editable=True)
    from_account = models.ForeignKey('Account', null=True, blank=True, related_name='from_acc_transaction', on_delete=models.PROTECT)
    from_amount = models.DecimalField(null=True, blank=True, max_digits=19, decimal_places=2)
    from_currency = models.ForeignKey('Currency', null=True, blank=True, related_name='from_cur_transaction', on_delete=models.PROTECT)
    to_account = models.ForeignKey('Account', null=True, blank=True, related_name='to_acc_transaction', on_delete=models.PROTECT)
    to_amount = models.DecimalField(null=True, blank=True, max_digits=19, decimal_places=2)
    to_currency = models.ForeignKey('Currency', null=True, blank=True, related_name='to_cur_transaction', on_delete=models.PROTECT)
    fee_amount = models.DecimalField(null=True, blank=True, max_digits=19, decimal_places=2)
    fee_currency = models.ForeignKey('Currency', null=True, blank=True, related_name='+', on_delete=models.PROTECT)

    class Meta:
        db_table = "content\".\"transaction"


class Expense(Transaction):
    class Meta:
        proxy = True

    def create(self, **kwargs):
        kwargs['type'] = 'expense'
        if not kwargs.get('to_amount'):
            kwargs['to_amount'] = kwargs['from_amount']
        if not kwargs.get('to_currency'):
            kwargs['to_currency'] = kwargs['to_currency'
                                           ]
        return super(Expense, self).create(**kwargs)

### VIEWS ###

class Assets(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    amount = models.DecimalField(blank=False, max_digits=19, decimal_places=2)
    currency = models.ForeignKey('Currency', blank=False, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "content\".\"assets"
        managed = False

class Total(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    amount = models.DecimalField(blank=False, max_digits=19, decimal_places=2)
    currency = models.ForeignKey('Currency', blank=False, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "content\".\"total"
        managed = False

class Exchange(models.Model):
    id = models.BigIntegerField(primary_key=True)
    date = models.DateField(blank=False)
    from_amount =models.DecimalField(blank=False, max_digits=19, decimal_places=2)
    from_currency = models.ForeignKey('Currency', related_name='+', blank=False, on_delete=models.DO_NOTHING)
    to_amount = models.DecimalField(blank=False, max_digits=19, decimal_places=2)
    to_currency = models.ForeignKey('Currency', related_name='+', blank=False, on_delete=models.DO_NOTHING)
    fee_amount = models.DecimalField(blank=False, max_digits=19, decimal_places=2)
    fee_currency = models.ForeignKey('Currency', related_name='+', blank=True, on_delete=models.DO_NOTHING)
    fee_percent = models.FloatField(blank=True)
    rate_dir = models.FloatField(blank=False)
    rate_dir_fee = models.FloatField(blank=True)
    currencies_dir = models.CharField(max_length=10)
    rate_rev = models.FloatField(blank=False)
    rate_rev_fee = models.FloatField(blank=True)
    currencies_rev = models.CharField(max_length=10)

    class Meta:
        db_table = "content\".\"exchange"
        managed = False
