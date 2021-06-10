from sys import path
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import csv
import re

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://nikolaj:alabamamud1@cluster0.kk6ac.mongodb.net/eyecandy?retryWrites=true&w=majority"

mongo = PyMongo(app)

db_posts = mongo.db.images

@app.route("/upload", methods=["POST"])
def upload_to_db():

    with open('cleaned_database.csv', 'r') as data:

        rows = csv.DictReader(data)

        counter = 0

        to_upload = []

        for row in rows:
            try:
                object = {
                    "full-image": row["full-image"],
                    "label-image": row["label-image"],
                    "tags": row["tags"],
                    "height": int(row["height"]),
                    "width": int(row["width"]),
                    "clicks": int(row['clicks'])
                }
                
                to_upload.append(object)
            except KeyError:
                continue
            counter += 1
        
        db_posts.insert_many(to_upload)

        print("Complete")

        return {'data': "success" + str(len(to_upload))}, 200

if __name__ == "__main__":
    app.run(threaded=True, debug=True, host='0.0.0.0', port='5000')

