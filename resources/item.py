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
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store_id"
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
        item = ItemModel(name, data['price'], data['store_id'])

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
                item = ItemModel(name, data['price'], data['store_id'])
                item.upsert()
            except:
                return {'message': 'An error occurred inserting item: ' + name}, 500
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
