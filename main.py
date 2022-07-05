# rest_api.py
from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://root:root123@cluster0.b67ih.mongodb.net/?retryWrites=true&w=majority"
mongo = PyMongo(app, uri="mongodb+srv://root:root123@cluster0.b67ih.mongodb.net/?retryWrites=true&w=majority")
db = mongo.cx.iot
collection = db.device_by_user

@app.route('/')
def index():
    return {
        'message': "welcome to my api tempe"
    }

@app.route('/user')
def get_user():
    user = collection.find()
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")

@app.route("/user", methods=["POST"])
def user():
    json = request.json
    collection.insert_one(json)
    json.pop('_id')
    return({
        'message':'datos registrados correctamente', 
        'user':json
        })
    
@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    collection.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response

@app.route('/user/<_id>', methods=['PUT'])
def update_user(_id):
    name = request.json['name'] 
    nameMoto=request.json['nameMoto'] 
    temperaturaMoto= request.json['temperaturaMoto'] 
    humedadMoto= request.json['humedadMoto'] 
    if name:
        if nameMoto:
            collection.update_one(
                {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'temperaturaMoto':temperaturaMoto,'humedadMoto':humedadMoto}})
            response = jsonify({'message': 'User' + _id + 'Updated Successfuly'})
            response.status_code = 200
            return response
        else:
            return not_found()

if __name__ == '__main__':
    print("Be careful, the API is open to the rest of the world.")
    app.run("0.0.0.0") # F