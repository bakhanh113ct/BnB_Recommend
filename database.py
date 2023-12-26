from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random
import json
db = SQLAlchemy()


class Product(db.Model):
    __tablename__ = 'Products'
    Id = db.Column(db.Text, primary_key=True)
    Name = db.Column(db.String(45), nullable=False)
    Desc = db.Column(db.String(225), nullable=False)
    Price = db.Column(db.Integer, nullable=False)
    BrandId = db.Column(db.Integer, nullable=False)
    ImportPrice = db.Column(db.Integer, nullable=False)
    CategoryId = db.Column(db.Integer, nullable=False)
    Inventory = db.Column(db.Integer, nullable=False)
    Sold = db.Column(db.Integer, nullable=False)
    

    def __init__(self, name, price):
        self.name = name
        self.price = price

    # def __repr__(self) -> str:
    #     return 'Product>>> {}'.format(self.Id)

class Order(db.Model):
    __tablename__ = 'Orders'
    Id = db.Column(db.Integer, primary_key=True)
    Status = db.Column(db.Integer, nullable=False)
    UserId = db.Column(db.Text, nullable=False)
    ReceiptAddress = db.Column(db.String(225), nullable=False)
    ReceiptPhone = db.Column(db.String(225), nullable=False)
    

    def __init__(self, status, userId):
        self.Status = status
        self.userId = userId

    # def __repr__(self) -> str:
    #     return 'Order>>> {self.Id}'
    
class OrderItems(db.Model):
    __tablename__ = 'OrderItems'
    Id = db.Column(db.Integer, primary_key=True)
    Quantity = db.Column(db.Integer, nullable=False)
    ProductId = db.Column(db.Text, nullable=False)
    OrderId = db.Column(db.String(225), nullable=False)
    SumPrice = db.Column(db.String(225), nullable=False)
    

    def __init__(self, status, userId):
        self.Status = status
        self.userId = userId

    # def __repr__(self) -> str:
    #     return 'Order>>> {self.Id}'