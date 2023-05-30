import datetime
from peewee import *

db = SqliteDatabase('my_app.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    name = CharField(unique=True)
    address = CharField()
    billing_information = CharField()

class Product(BaseModel):
    user = ForeignKeyField(User, backref='products')
    name = CharField()
    description = TextField()
    price = DecimalField(max_digits=10, decimal_places=2)
    quantity = IntegerField()

class Tag(BaseModel):
    name = CharField(unique=True)

class ProductTag(BaseModel):
    product = ForeignKeyField(Product, backref='product_tags')
    tag = ForeignKeyField(Tag, backref='product_tags')

    class Meta:
        # A product can't have duplicated tags
        indexes = (
            # create a unique on product/tag
            (('product', 'tag'), True),
        )

class Transaction(BaseModel):
    buyer = ForeignKeyField(User, backref='purchases')
    product = ForeignKeyField(Product, backref='transactions')
    quantity = IntegerField()
    timestamp = DateTimeField(default=datetime.datetime.now)

db.create_tables([User, Product, Tag, ProductTag, Transaction], safe=True)
