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

with app.app_context():
    # db.create_all()
    print('init done')

    # users = Product.query.filter_by(Name="Gorgeous Concrete Towels").all()
    # print(users)
    # orders = Order.query.filter_by(UserId="1").all()
    # # print(orders)
    # ordersID = [o.Id for o in orders]
    # # print(ordersID)
    # order_items = OrderItems.query.filter_by(OrderId=func.any(ordersID)).all()
    # # print(order_items)
    # productsId = [o.ProductId for o in order_items]
    # products = Product.query.filter_by(Id=func.any(productsId)).all()
    # print(products)
        

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
    # orders = Order.query.all()
    # filtered = [project for project in orders if project.UserId == "11"]
    # # print(filtered)
    # for i in range(len(filtered)):
    #     order_items = OrderItems.query.all()
    #     itemsFiltered = [project for project in order_items if project.OrderId == filtered[i].Id]
    #     for j in range(len(itemsFiltered)):
    #         print(itemsFiltered[j].ProductId) 
    #         products = Product.query.all()
    #         productFiltered = [project for project in products if project.Id == itemsFiltered[j].ProductId]
    #         for k in range(len(productFiltered)):
    #             print(productFiltered[k].Name)

def tokenizer(text):
    return word_tokenize(text, format="text")


def add_data_user(json_data, id_trip):
    data = json.loads(json_data.decode('utf-8'))
    id_trip = data['idTrip']
    title = data['title']
    description = data['description']
    activities = data['activities']
    with open(id_trip+'.csv', 'a', encoding='utf-8', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([id_trip, activities, description, title])


def get_trip_index(trips_df, idTrip):
    return trips_df[trips_df['idTrip'] == idTrip].index[0]


def get_trip_id(trips_df, index):
    return trips_df[trips_df.index == index]['idTrip'].values[0]


@app.route("/")
def hello_world():
    return "<p>Hello world</p>"


class UndertheseaTokenizer:
    def __call__(self, text):
        return word_tokenize(text)


@app.route("/recommend_products", methods=['GET'])
def get_recommendations():
    id_trip = json.loads(request.data.decode('utf-8'))['idTrip']
    #get products
    products = getOrdersByUserId('1')
    print(products)
    # query.getData(id_trip)
    # add_data_user(request.data,id_trip)
    # trips_df = pd.read_csv(id_trip+'.csv')
    # trips_df['text'] = trips_df['title'] + ' ' + trips_df['description']+ ' ' + trips_df['activities']
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
    vectorizer = TfidfVectorizer(tokenizer=UndertheseaTokenizer())
    tfidf_matrix = vectorizer.fit_transform(df['Desc'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    product_id ="1"
    try:
        # Find the index of the product in the DataFrame
        product_index = df[df['Id'] == product_id].index[0]

        # Get similarity scores of all products with the given product
        sim_scores = list(enumerate(cosine_sim[product_index]))

        # Sort products based on similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Select top similar products (excluding the given product itself)
        top_similar_products = sim_scores[1:11]  # Change the range as needed

        # Retrieve recommended product IDs
        recommended_product_ids = [df.iloc[i[0]]['Id'] for i in top_similar_products]

        # Return recommended product IDs as a JSON response
        return jsonify({"recommended_products": recommended_product_ids}), 200

    except IndexError:
        return jsonify({"error": "Product ID not found"}), 404


if __name__ == "__main__":
    app.run()
