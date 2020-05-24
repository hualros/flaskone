import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be blank!"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': f"Item '{name}' not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            message = f"An item with the {name} already exists."
            return {'message': message}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])

        try:
            item.upsert()
        except:
            return {'message': 'An error occurred.'}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete()
            return {'message': 'Item deleted: ' + name}
        else:
            return {'message': f"Item '{name}' not found!"}, 404

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item:
            try:
                item.price = data['price']
                item.upsert()
            except:
                return {'message': 'An error occurred updating item: ' + name}, 500
        else:
            try:
                item = ItemModel(name, data['price'])
                item.upsert()
            except:
                return {'message': 'An error occurred inserting item: ' + name}, 500
        return item.json()


class ItemList(Resource):

    @classmethod
    def find_all(cls):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "select * from items"
        results = cursor.execute(query)
        items = []
        for row in results:
            items.append({'id': row[0], 'name': row[1], 'price': row[2]})
        connection.close()
        if items:
            return {'items': items}, 200
        return {'message': 'No items found'}, 404

    def get(self):
        return self.find_all()
