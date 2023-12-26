from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from underthesea import word_tokenize
import csv
import json
import subprocess
import query
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from database import db, Product, Order, OrderItems
import os
from sqlalchemy import func


app = Flask(__name__, instance_relative_config=True)


app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DB_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db.init_app(app)

        

def getOrdersByUserId(userId):
    orders = Order.query.filter_by(UserId=userId).all()
    # print(orders)
    ordersID = [o.Id for o in orders]
    # print(ordersID)
    order_items = OrderItems.query.filter_by(OrderId=func.any(ordersID)).all()
    # print(order_items)
    productsId = [o.ProductId for o in order_items]
    products = Product.query.filter_by(Id=func.any(productsId)).all()
    # print(products)
    return products

def tokenizer(text):
    return word_tokenize(text, format="text")


@app.route("/")
def hello_world():
    return "<p>Hello world</p>"


class UndertheseaTokenizer:
    def __call__(self, text):
        return word_tokenize(text)


@app.route("/recommend_products/<int:user_id>", methods=['GET'])
def get_recommendations(user_id):
    products_user = getOrdersByUserId(str(user_id))
    products = Product.query.all()
    product_data = [
    {
        'Id': product.Id,
        'Name': product.Name,
        'Desc': product.Desc,
        'Price': product.Price,
        'BrandId': product.BrandId,
        'ImportPrice': product.ImportPrice,
        'CategoryId': product.CategoryId,
        'Inventory': product.Inventory,
        'Sold': product.Sold
    }
    for product in products
    ]
    df = pd.DataFrame(product_data)
    if not products_user:  # Nếu không có sản phẩm cho người dùng cụ thể
        recommended_product_ids = df.head(10).to_dict(orient='records')
        return jsonify({"recommended_products": recommended_product_ids}), 200

    vectorizer = TfidfVectorizer(tokenizer=UndertheseaTokenizer())
    tfidf_matrix = vectorizer.fit_transform(df['Desc'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    product_id =products_user[0].Id
    try:
        product_index = df[df['Id'] == product_id].index[0]

        # Get similarity scores of all products with the given product
        sim_scores = list(enumerate(cosine_sim[product_index]))

        # Sort products based on similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Select top similar products (excluding the given product itself)
        top_similar_products = sim_scores[1:11]  # Change the range as needed

        # Retrieve recommended product IDs
        recommended_product_ids = [df.iloc[i[0]].to_dict() for i in top_similar_products]

        # Return recommended product IDs as a JSON response
        return jsonify({"recommended_products": recommended_product_ids}), 200

    except IndexError:
        return jsonify({"error": "Product ID not found"}), 404


if __name__ == "__main__":
    app.run()
