from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
from abc import ABC, abstractmethod

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

    def get_json_data(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }


class AbstractDatabaseAdapter(ABC):

    @abstractmethod
    def create(self, entity):
        pass

    @abstractmethod
    def get_all(self, entity_type):
        pass

    @abstractmethod
    def get_by_id(self, entity_type, entity_id):
        pass

    @abstractmethod
    def update(self, entity):
        pass

    @abstractmethod
    def delete(self, entity):
        pass


class PostgreSQLAdapter(AbstractDatabaseAdapter):

    def create(self, entity):
        db.session.add(entity)
        db.session.commit()

    def get_all(self, entity_type, page=1, per_page=10):
        return entity_type.query.paginate(page=page, per_page=per_page, error_out=False)

    def get_by_id(self, entity_type, entity_id):
        return entity_type.query.get(entity_id)

    def update(self, entity):
        db.session.commit()

    def delete(self, entity):
        db.session.delete(entity)
        db.session.commit()


db_adapter = PostgreSQLAdapter()

with app.app_context():
    db.create_all()


@app.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'test route message'}), 200)


@app.route('/user', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'])
        db_adapter.create(new_user)
        return make_response(jsonify({'message': 'user created'}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'error creating user'}), 500)


@app.route('/users', methods=['GET'])
def get_users():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        pagination = db_adapter.get_all(User, page, per_page)
        users = pagination.items

        return make_response(jsonify({
            'users': [user.get_json_data() for user in users],
            'total_pages': pagination.pages,
            'current_page': pagination.page
        })), 200
    except Exception as e:
        return make_response(jsonify({'message': 'error getting users'}), 500)


@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = db_adapter.get_by_id(User, id)
        if user:
            return make_response(jsonify(user.get_json_data()), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting user'}), 500)


@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        user = db_adapter.get_by_id(User, id)
        if user:
            data = request.get_json()
            user.username = data['username']
            user.email = data['email']
            db_adapter.update(user)
            return make_response(jsonify(user.get_json_data()), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error updating user'}), 500)


@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = db_adapter.get_by_id(User, id)
        if user:
            db_adapter.delete(user)
            return make_response(jsonify({'message': 'user deleted'}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error deleting user'}), 500)


if __name__ == '__main__':
    app.run()
