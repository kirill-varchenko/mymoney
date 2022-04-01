from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class Expense(BaseModel):
    from_account: int
    from_amount: int
    from_currency: str
    to_amount: Optional[int] = None
    to_currency: Optional[str] = None
    date: date = Field(default_factory=date.today)
    type: str = 'expense'
