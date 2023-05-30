__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

from faker import Faker
from models import User, Product, Tag, ProductTag, Transaction
from peewee import IntegrityError, fn


def search_products_by_term(term):
    term = term.lower()
    products = Product.select().where(Product.name ** f"%{term}%")
    return products

def view_user_products(user_id):
    try:
        user = User.get_by_id(user_id)
        products = Product.select().where(Product.user == user)
        return products
    except User.DoesNotExist:
        return []

def view_products_by_tag(tag_name):
    try:
        tag = Tag.get(Tag.name == tag_name)
        products = Product.select().join(ProductTag).where(ProductTag.tag == tag).execute()
        return products
    except Tag.DoesNotExist:
        return []

def add_product_to_user(user_id, product_data):
    try:
        user = User.get_by_id(user_id)
        product = Product.create(user=user, **product_data)
        return product
    except User.DoesNotExist:
        return None

def remove_product_from_user(user_id, product_id):
    try:
        product = Product.get(Product.id == product_id, Product.user == user_id)
        product.delete_instance()
        return True
    except Product.DoesNotExist:
        return False

def update_product_quantity(product_id, new_quantity):
    try:
        product = Product.get_by_id(product_id)
        product.quantity = new_quantity
        product.save()
        return True
    except Product.DoesNotExist:
        return False

def handle_purchase(buyer_id, product_id, quantity):
    try:
        buyer = User.get_by_id(buyer_id)
        product = Product.get_by_id(product_id)

        if product.quantity >= quantity:
            transaction = Transaction.create(
                buyer=buyer, product=product, quantity=quantity
            )

            product.quantity -= quantity
            product.save()

            return transaction
        else:
            return None
    except (User.DoesNotExist, Product.DoesNotExist):
        return None

fake = Faker()

def create_fake_users(n):
    products_names = ["sweater", "Pants", "Horse-suit"]
    for _ in range(n):
        user = User.create(
            name=fake.unique.user_name(),
            address=fake.address(),
            billing_information=fake.credit_card_full()
        )
        for product_name in products_names:
            create_fake_products(user, product_name)

def create_fake_products(user, product_name):
    for _ in range(fake.random_int(min=1, max=5)):
        product = Product.create(
            user=user,
            name=product_name,
            description=fake.sentence(),
            price=fake.random_number(digits=2, fix_len=True),
            quantity=fake.random_int(min=1, max=100)
        )
        create_fake_tags(product)

def create_fake_tags(product):
    for _ in range(fake.random_int(min=1, max=5)):
        tag_name = fake.color_name()
        try:
            tag = Tag.create(name=tag_name)
        except IntegrityError: # when the tag exists already
            tag = Tag.get(Tag.name == tag_name)
        
        try:
            ProductTag.get(product=product, tag=tag)
        except ProductTag.DoesNotExist:
            ProductTag.create(product=product, tag=tag)

def create_fake_transactions(n):
    for _ in range(n):
        buyer = User.select().order_by(fn.Random()).get()
        product = Product.select().order_by(fn.Random()).get()
        quantity = fake.random_int(min=1, max=product.quantity)
        handle_purchase(buyer.id, product.id, quantity)

# create 5 full user profiles with products and tags
# create_fake_users(5)

# create some transactions
# create_fake_transactions(10)


## tests ##

# print_users_and_transactions()

# print the products according to the search term
# products = search_products_by_term('sweater')

# for product in products:
    # print(f"ID: {product.id}, Name: {product.name}, Description: {product.description})")

    # search for the produdct related to the ID-number
# products = view_user_products(1)

# for product in products:
    # print(f"ID: {product.id}, Name: {product.name})")

# def print_all_tags():
#     tags = Tag.select()
#     for tag in tags:
#         print(f"ID: {tag.id}, Name: {tag.name}")

# Call the function
# print_all_tags()

# showing products by tag 

# def view_products_by_tag(tag_name):
#     try:
#         tag = Tag.get(Tag.name == tag_name)
#         products = Product.select().join(ProductTag).join(Tag).where(Tag.name == tag_name)
#         return products
#     except Tag.DoesNotExist:
#         return []

# products = view_products_by_tag('Peru')
# for product in products:
#     print(f"ID: {product.id}, Name: {product.name}, Description: {product.description}, Price: {product.price}, Quantity: {product.quantity}")

# adding product to a user
# product_data = {
#     'name': 'Cool Sweater',
#     'description': 'A dope cool sweater.',
#     'price': 49.99,
#     'quantity': 100
# }
# product = add_product_to_user(1, product_data)
# print(f"Added product with ID: {product.id} to user with ID: {product.user_id}")

#removing product from a user - 1st value is the user, 2nd the product
# result = remove_product_from_user(1, 3)
# if result:
#     print("Product removed successfully.")
# else:
#     print("Failed to remove product.")

# updating the stock quantity of a product
# result = update_product_quantity(6, 45)
# if result:
#     print("Product quantity updated successfully.")
# else:
#     print("Failed")

# #handle a purchase between a buyer and a seller for a product
# # buyer, product id, quality
# transaction = handle_purchase(1, 6, 30)
# if transaction:
#     print(f"Transaction successful. ID: {transaction.id}, Buyer ID: {transaction.buyer_id}, Product ID: {transaction.product_id}, Quantity: {transaction.quantity}")
# else:
#     print("Transaction failed.")



# printing general information

# def print_users_and_transactions():
#     users = User.select()
    
#     for user in users:
#         print(f"User ID: {user.id}, name: {user.name}, addres: {user.address}, billing Information: {user.billing_information}")
#         transactions = Transaction.select().where(Transaction.buyer == user)
        
#         if transactions.exists():
#             print("transactions:")
#             for transaction in transactions:
#                 product = transaction.product
#                 print(f"\tProduct ID: {product.id}, Name: {product.name}, Quantity: {transaction.quantity}")
#         else:
#             print(f"No transactions by {user.name}")
#         print('\n')