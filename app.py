from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime

# Data contoh produk baju yang lebih lengkap
clothing_products = [
    {"id": "1", "name": "Basic T-Shirt", "description": "Comfortable cotton T-shirt in various colors.", "price": 120000},
    {"id": "2", "name": "Denim Jacket", "description": "Classic denim jacket with a modern fit.", "price": 300000},
    {"id": "3", "name": "Casual Hoodie", "description": "Warm and cozy hoodie for everyday wear.", "price": 220000},
    {"id": "4", "name": "Summer Dress", "description": "Lightweight dress perfect for summer days.", "price": 180000},
    {"id": "5", "name": "Cargo Pants", "description": "Durable cargo pants with multiple pockets.", "price": 250000},
    {"id": "6", "name": "Formal Blazer", "description": "Elegant blazer for formal occasions.", "price": 400000},
    {"id": "7", "name": "Graphic Tee", "description": "T-shirt with unique graphic designs.", "price": 130000},
    {"id": "8", "name": "Sweater", "description": "Soft sweater ideal for colder weather.", "price": 200000},
    {"id": "9", "name": "Jogger Pants", "description": "Comfortable jogger pants for casual style.", "price": 150000},
    {"id": "10", "name": "Polo Shirt", "description": "Classic polo shirt suitable for any occasion.", "price": 140000}
]

# Detail produk yang lebih lengkap
product_details = {product['id']: {**product, "customerReviews": []} for product in clothing_products}

app = Flask(__name__)
api = Api(app)

class ProductList(Resource):
    def get(self):
        return {
            "error": False,
            "message": "success",
            "count": len(clothing_products),
            "products": clothing_products
        }

class ProductDetail(Resource):
    def get(self, product_id):
        if product_id in product_details:
            return {
                "error": False,
                "message": "success",
                "product": product_details[product_id]
            }
        return {"error": True, "message": "Product not found"}, 404

class ProductSearch(Resource):
    def get(self):
        query = request.args.get('q', '').lower()
        result = [p for p in clothing_products if query in p['name'].lower() or query in p['description'].lower()]
        return {
            "error": False,
            "found": len(result),
            "products": result
        }

class AddReview(Resource):
    def post(self):
        data = request.get_json()
        product_id = data.get('id')
        name = data.get('name')
        review = data.get('review')
        
        if product_id in product_details:
            new_review = {
                "name": name,
                "review": review,
                "date": datetime.now().strftime("%d %B %Y")
            }
            product_details[product_id]['customerReviews'].append(new_review)
            return {
                "error": False,
                "message": "Review added successfully",
                "customerReviews": product_details[product_id]['customerReviews']
            }
        return {"error": True, "message": "Product not found"}, 404

class UpdateReview(Resource):
    def put(self):
        data = request.get_json()
        product_id = data.get('id')
        name = data.get('name')
        new_review_text = data.get('review')
        
        if product_id in product_details:
            reviews = product_details[product_id]['customerReviews']
            review_to_update = next((r for r in reviews if r['name'] == name), None)
            if review_to_update:
                review_to_update['review'] = new_review_text
                review_to_update['date'] = datetime.now().strftime("%d %B %Y")
                return {
                    "error": False,
                    "message": "Review updated successfully",
                    "customerReviews": reviews
                }
            return {"error": True, "message": "Review not found"}, 404
        return {"error": True, "message": "Product not found"}, 404

class DeleteReview(Resource):
    def delete(self):
        data = request.get_json()
        product_id = data.get('id')
        name = data.get('name')
        
        if product_id in product_details:
            reviews = product_details[product_id]['customerReviews']
            review_to_delete = next((r for r in reviews if r['name'] == name), None)
            if review_to_delete:
                reviews.remove(review_to_delete)
                return {
                    "error": False,
                    "message": "Review deleted successfully",
                    "customerReviews": reviews
                }
            return {"error": True, "message": "Review not found"}, 404
        return {"error": True, "message": "Product not found"}, 404

# Menambahkan resource ke API
api.add_resource(ProductList, '/list')
api.add_resource(ProductDetail, '/detail/<string:product_id>')
api.add_resource(ProductSearch, '/search')
api.add_resource(AddReview, '/review')
api.add_resource(UpdateReview, '/review/update')
api.add_resource(DeleteReview, '/review/delete')

if __name__ == '__main__':
    app.run(debug=True)
