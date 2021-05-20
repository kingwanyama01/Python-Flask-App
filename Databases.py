from peewee import *
from os import path

ROOT = path.dirname(path.realpath(__file__))
db = SqliteDatabase(path.join(ROOT, "users.db"))


class User(Model):
    names = CharField()
    email = CharField(unique=True)
    password = CharField()
    sum_purchase = IntegerField()

    class Meta:
        database = db


class Person(Model):
    owner = ForeignKeyField(User, related_name="persons")
    names = CharField()
    weight = DecimalField()
    age = IntegerField()

    class Meta:
        database = db


class Product(Model):
    name = CharField()
    price = DecimalField()
    description = CharField()
    category = CharField()
    out_of_stock = IntegerField()
    image = CharField()

    class Meta:
        database = db


class Cart(Model):
    name = CharField()
    price = DecimalField()
    description = CharField()
    image = CharField()

    class Meta:
        database = db


class Order(Model):
    name = CharField()
    price = DecimalField()
    description = CharField()
    delivered = IntegerField()
    image = CharField()

    class Meta:
        database = db


User.create_table(fail_silently=True)
Person.create_table(fail_silently=True)
Product.create_table(fail_silently=True)
Cart.create_table(fail_silently=True)
Order.create_table(fail_silently=True)
