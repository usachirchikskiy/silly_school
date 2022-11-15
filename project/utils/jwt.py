import jwt
from flask import request, jsonify, current_app as app, Response
from functools import wraps

from project.model.User import User


def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):

      token = None

      if 'x-access-tokens' in request.headers:
         token = request.headers['x-access-tokens']

      if not token:
         return Response(
            "a valid token is missing",
            status=400,
         )


      try:
         data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])
         current_user = User.query.get(data['id'])
      except Exception as e:
         print(e)
         return Response(
            "token is invalid",
            status=400,
         )

      return f(current_user, *args, **kwargs)
   return decorator
