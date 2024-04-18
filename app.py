import os
from flask import Flask
from controller.controller import *
from dotenv import load_dotenv

app = Flask(__name__)

dotenv_path = '.env.mysql'
load_dotenv(dotenv_path)
db_uri = f"mysql+pymysql://root:{os.getenv('MYSQL_ROOT_PASSWORD')}@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db.init_app(app)

@app.route('/products', methods=['GET'])
def get_products_route():
    return get_all_products()

@app.route('/products/paged', methods=['GET'])
def get_paged_products_route():
    return get_paged_products()

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product_route(product_id):
    return update_product(product_id)

@app.route('/products', methods=['POST'])
def create_product_route():
    return create_product()

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product_route(product_id):
    return delete_product(product_id)

@app.route('/savetocsv', methods=['GET'])
def get_to_csv_route():
    return get_to_csv()

@app.route('/importcsv', methods=['POST'])
def import_csv_to_db_route():
    return import_csv_to_db()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Product.query.all():
            initial_products = [
                {'name': 'Product1', 'price': 10.99},
                {'name': 'Product2', 'price': 20.99},
                {'name': 'Product3', 'price': 30.99}
            ]
            for product_data in initial_products:
                new_product = Product(name=product_data['name'], price=product_data['price'])
                db.session.add(new_product)
            db.session.commit()

    app.run(debug=True)
