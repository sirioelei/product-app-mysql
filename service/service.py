# service.py

from repository.repository import ProductRepository

class ProductService:
    @staticmethod
    def get_all_products():
        return ProductRepository.get_all_products()

    @staticmethod
    def create_product(name, price):
        return ProductRepository.create_product(name, price)

    @staticmethod
    def delete_product(product_id):
        return ProductRepository.delete_product(product_id)
