import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, root_validator


class ExpenseModel(BaseModel):
    type: str = 'expense'
    date: datetime.date = Field(default_factory=datetime.date.today)
    from_account_id: int
    from_amount: Decimal
    from_currency_id: str
    to_amount: Optional[Decimal] = None
    to_currency_id: Optional[str] = None

    @root_validator(pre=True)
    def check_to_values(cls, values):
        values['from_currency_id'] = values['from_currency_id'].upper()
        if values.get('to_currency_id'):
            values['to_currency_id'] = values['to_currency_id'].upper()
        else:
            values['to_currency_id'] = values['from_currency_id']

        if values.get('to_amount') is None:
            values['to_amount'] = values['from_amount']

        return values

