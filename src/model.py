from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Text, Float, DateTime, Integer


Base = declarative_base()

class Expense(Base):
    """
    Expense class attributes
    """
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    paid_to = Column(String(255))
    category = Column(String(255))
    date_added = Column(String)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at  = Column(DateTime, default=datetime.utcnow())
    
    def __repr__(self) -> str:
        return f"Expense(id={self.id!r}, title={self.title!r}"
    
        

       
    