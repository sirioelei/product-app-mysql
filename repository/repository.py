# repository.py

from model.product import db, Product

class ProductRepository:
    @staticmethod
    def get_all_products():
        return Product.query.all()

    @staticmethod
    def create_product(name, price):
        new_product = Product(name=name, price=price)
        db.session.add(new_product)
        db.session.commit()
        return new_product

    @staticmethod
    def delete_product(product_id):
        product = Product.query.get(product_id)
        if not product:
            return False
        db.session.delete(product)
        db.session.commit()
        return True
