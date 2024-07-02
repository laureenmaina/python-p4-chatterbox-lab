from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == "GET":
        messages = []
        for message in Message.query.order_by(Message.created_at.asc()).all():
            messages_dict = {
                "id": message.id,
                "body": message.body,
                "username": message.username,
                "created_at": message.created_at,
                "updated_at": message.updated_at
            }
            messages.append(messages_dict)

        response = make_response(jsonify(messages), 200)
        return response

    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(
            body=data.get("body"),
            username=data.get("username"),
        )
        db.session.add(new_message)
        db.session.commit()

        messages_dict = {
            "id": new_message.id,
            "body": new_message.body,
            "username": new_message.username,
            "created_at": new_message.created_at,
            "updated_at": new_message.updated_at
        }

        response = make_response(jsonify(messages_dict), 201)
        return response

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = db.session.get(Message, id)

    if request.method == 'PATCH':
        if message:
            data = request.get_json()
            message.body = data.get("body", message.body)
            db.session.commit()

            messages_dict = {
                "id": message.id,
                "body": message.body,
                "username": message.username,
                "created_at": message.created_at,
                "updated_at": message.updated_at
            }

            response = make_response(jsonify(messages_dict), 200)
            return response
        else:
            response = make_response(
                jsonify({"error": "Message not found"}),
                404
            )
            return response

    elif request.method == 'DELETE':
        if message:
            db.session.delete(message)
            db.session.commit()
            response = make_response('', 204)
            return response
        else:
            response = make_response(
                jsonify({"error": "Message not found"}),
                404
            )
            return response

if __name__ == '__main__':
    app.run(port=5555)
