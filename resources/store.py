from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': f'Store: {name} not found!'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f"Store: '{name}' already exists!"}, 400
        store = StoreModel(name)
        try:
            store.upsert()
        except:
            return {'message': f"Store: '{name}' cannot be saved!"}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete()
            return {'message': f"Store: {name} deleted!"}
        else:
            return {'message': f"Store: {name} not found. Not deleted."}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
