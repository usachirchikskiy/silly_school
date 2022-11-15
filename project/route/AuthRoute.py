import datetime
from flask import jsonify, request, Blueprint, make_response
from flask import current_app as app
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
from project.model import db
from project.model.User import User
from project.utils.jwt import token_required

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/register', methods=['POST'])
def signup_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(name=data['name'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'registered successfully'})


@auth_bp.route('/login', methods=['POST'])
def login_user():
    body = request.get_json()

    if not body['name'] or not body['password']:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = User.query.filter_by(name=body['name']).first()

    if user and check_password_hash(user.password, body['password']):
        token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=60000)},
                           app.config['SECRET_KEY'], "HS256")
        return jsonify({'token': token})

    return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

@auth_bp.route("/check", methods = ['GET'])
@token_required
def check(current_user):
    return jsonify(
        status = 'success'
    )