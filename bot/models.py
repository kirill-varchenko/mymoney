from sqlalchemy import (Column, Date, ForeignKey, Integer, MetaData, Numeric,
                        String, Table, create_engine)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from settings import db_settings

engine = create_engine(db_settings.uri)

Base = declarative_base(metadata=MetaData(schema='content'))

Session = sessionmaker(engine)

class Currency(Base):
    __tablename__ = 'currency'

    id = Column(String(3), primary_key=True)
    symbol = Column(String(1))

class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer(), primary_key=True)
    name = Column(String(255), nullable=False)
    currency_id = Column(String(3), ForeignKey(Currency.id), nullable=False)
    initial_amount = Column(Numeric(precision=19, scale=2), default=0)

    currency = relationship('Currency', uselist=False, lazy='joined')

class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer(), primary_key=True)
    type = Column(String(10), nullable=False)
    date = Column(Date(), nullable=False)
    from_account_id = Column(Integer(), ForeignKey(Account.id))
    from_amount = Column(Numeric(precision=19, scale=2))
    from_currency_id = Column(String(3), ForeignKey(Currency.id))
    to_account_id = Column(Integer(), ForeignKey(Account.id))
    to_amount = Column(Numeric(precision=19, scale=2))
    to_currency_id = Column(String(3), ForeignKey(Currency.id))
    fee_amount = Column(Numeric(precision=19, scale=2))
    fee_currency_id = Column(String(3), ForeignKey(Currency.id))

