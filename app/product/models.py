import sqlalchemy as sa
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class Product(Base):
    __tablename__ = "product"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String(50))
    price = sa.Column(sa.Float)
    description = sa.Column(sa.String(100))
    
    def __str__(self):
        return f"{self.name} - {self.price}"