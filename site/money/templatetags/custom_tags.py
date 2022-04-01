from decimal import Decimal
from typing import Optional

from django import template

register = template.Library()

@register.filter(name='amount')
def amount(value: Optional[Decimal]) -> str:
    if value is None:
        return ''
    return f"{value:,.2f}"
