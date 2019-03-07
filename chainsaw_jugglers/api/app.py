from flask import Flask, g, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict

DATABASE = 'chainsaw.db'

app = Flask(__name__)

database = SqliteDatabase(DATABASE)

class Chainsaw(Model):
    name = CharField()
    country = CharField()
    catches = IntegerField()

    class Meta:
        database = database


database.create_tables([Chainsaw])

@app.before_request
def before_request():
    g.db = database
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/api/chainsaw')
def get_all():
    res = Chainsaw.select()
    return jsonify([model_to_dict(c) for c in res])

@app.route('/api/chainsaw/<catcher_id>')
def get_by_id(catcher_id):
    try:
        c = Chainsaw.get_by_id(catcher_id)
        return jsonify(model_to_dict(c))
    except DoesNotExist:
        return 'Not found', 404

@app.route('/api/chainsaw', methods=['POST'])
def add_new():
    with database.atomic():
        c = Chainsaw.create(**request.form.to_dict())
        return jsonify(model_to_dict(c)), 201

@app.route('/api/chainsaw/<catcher_id>', methods=['PATCH'])
def update_chainsaw(catcher_id):
    with database.atomic():
        Chainsaw.update(**request.form.to_dict())\
            .where(Chainsaw.id == catcher_id)\
            .execute()
        return 'ok', 200

@app.route('/api/chainsaw/<catcher_id>', methods=['DELETE'])
def delete_chainsaw(catcher_id):
    with database.atomic():
        Chainsaw.delete().where(Chainsaw.id == catcher_id).execute()
    return 'ok', 200

if __name__ == '__main__':
    app.run()


