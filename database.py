from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random
import json
db = SQLAlchemy()


class Product(db.Model):
    __tablename__ = 'Products'
    Id = db.Column(db.Integer, primary_key=True)
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

    def __repr__(self) -> str:
        return 'Product>>> {self.id}'

