from peewee import *

db = SqliteDatabase('cats.sqlite')


class Cat(Model):
    name = CharField()
    color = CharField()
    age = IntegerField()

    class Meta:
        database = db

    def __str__(self):
        return f'{self.name}, {self.color}, {self.age}'


db.connect()
db.create_tables([Cat])

Cat.delete().execute()  # clear database table

# create - insert
stella = Cat(name='Stella', color='Brown', age=6)
stella.save()  # don't forget to save

riley = Cat(name='Riley', color='Grey', age=3)
riley.save()

# read - select
cats = Cat.select()
for cat in cats:
    print(cat)

list_of_cats = list(cats)  # creates regular python list

"""
CRUD Operations:
Create - insert
Read - select
Update
Delete
"""

# update
stella.age = 7
stella.save()

print('After Stella\'s birthday')
cats = Cat.select()
for cat in cats:
    print(cat)

# can update many rows
rows_modified = Cat.update(age=4).where(Cat.name == 'Riley').execute()

print('After Riley\'s birthday')
cats = Cat.select()
for cat in cats:
    print(cat)

print(rows_modified)

august_pepper = Cat(name='August Pepper', color='Black\\White', age=2)
august_pepper.save()

cat_who_are_2 = Cat.select().where(Cat.age == 2)
for cat in cat_who_are_2:
    print(cat, 'is two')

cat_with_l_in_name = Cat.select().where(Cat.name % '*l*')  # use wildcard
# .where(Cat.name.contains('l')) is case insensitive
for cat in cat_with_l_in_name:
    print(cat, 'has l in name')

stella_from_db = Cat.get_or_none(name='Stella')  # returns None if entity does not exist
print(stella_from_db)

cat_1 = Cat.get_by_id(1)  # search by id - get or none is safer
print(cat_1)

# count, sort, limit

total = Cat.select().count()
print(total)

total_cats_who_are_2 = Cat.select().where(Cat.age == 2).count()
print(total_cats_who_are_2)

cats_by_name = Cat.select().order_by(Cat.name)  # use Cat.name.desc() for opposite order # can sort by multiple fields
print(list(cats_by_name))

first_2 = Cat.select().order_by(Cat.name).limit(2)
print(list(first_2))

# delete

# Cat.delete().execute()  # caution! this deletes everything
# print(list(Cat.select()))

rows_deleted = Cat.delete().where(Cat.name == 'Stella').execute()
print(rows_deleted, list(Cat.select()))
