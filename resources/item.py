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

    #@jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            message = f"An item with the {name} already exists."
            return {'message': message}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])

        try:
            item.insert()
        except:
            return {'message': 'An error occurred.'}, 500

        return item.json(), 201

    def delete(self, name):
        if ItemModel.delete_item(name):
            return {'message': 'Item deleted: ' + name}
        return {'message': 'Item not deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        existing_item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])

        if existing_item:
            try:
                updated_item.update()
            except:
                return {'message': 'An error occurred updating item.'}, 500
        else:
            try:
                updated_item.insert()
            except:
                return {'message': 'An error occurred inserting item.'}, 500
        return updated_item.json()


class ItemList(Resource):

    @classmethod
    def find_all(cls):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "select * from items"
        results = cursor.execute(query)
        items = []
        for row in results:
            items.append({'name': row[0], 'price': row[1]})
        connection.close()
        if items:
            return {'items': items}, 200
        return {'message': 'No items found'}, 404

    def get(self):
        return self.find_all()
