# controller.py

import csv
from flask import jsonify, request, Response
from service.service import ProductService
from model.product import Product, db


def get_all_products():
    products = ProductService.get_all_products()
    products_json = [{'id': product.id, 'name': product.name, 'price': product.price} for product in products]
    return jsonify(products_json)

def create_product():
    data = request.json
    name = data.get('name')
    price = data.get('price')
    if not name or not price:
        return jsonify({'error': 'Name and price are required'}), 400
    new_product = ProductService.create_product(name, price)
    return jsonify({'message': 'Product created successfully', 'id': new_product.id}), 201

def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    data = request.json
    name = data.get('name')
    price = data.get('price')

    if name is not None:
        product.name = name
    if price is not None:
        product.price = price

    db.session.commit()

    return jsonify({'message': 'Product updated successfully', 'id': product.id}), 200

def delete_product(product_id):
    success = ProductService.delete_product(product_id)
    if not success:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify({'message': 'Product deleted successfully'})

def get_to_csv():
    products = ProductService.get_all_products()
    if not products:
        return jsonify({'error': 'No products found'}), 404

    csv_data = [['Name', 'Price']]
    for product in products:
        csv_data.append([product.name, product.price])

    with open('../products.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(csv_data)

    with open('../products.csv', 'r') as f:
        csv_content = f.read()

    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=products.csv"})

def import_csv_to_db():
    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({'error': 'No file uploaded'}), 400

    if file.filename.endswith('.csv'):
        csv_data = csv.reader(file.stream.read().decode('utf-8').splitlines())
        next(csv_data)  # Skip the header row
        for row in csv_data:
            name, price = row
            ProductService.create_product(name, price)
        return jsonify({'message': 'CSV data imported successfully'}), 200
    else:
        return jsonify({'error': 'Invalid file format. Please upload a CSV file'}), 400


def get_paged_products():
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)

    offset = (page - 1) * limit

    products = Product.query.offset(offset).limit(limit).all()

    total_products = Product.query.count()

    total_pages = total_products // limit
    if total_products % limit > 0:
        total_pages += 1

    products_json = [{'id': product.id, 'name': product.name, 'price': product.price} for product in products]

    return jsonify({
        'page': page,
        'limit': limit,
        'total_pages': total_pages,
        'total_products': total_products,
        'products': products_json
    }), 200
