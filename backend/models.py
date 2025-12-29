from sqlalchemy import Column, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"
    txn_id = Column(String, primary_key=True)
    user_id = Column(String)
    datetime = Column(DateTime)
    amount = Column(Numeric)
    direction = Column(String)
    merchant = Column(String)
