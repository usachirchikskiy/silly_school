import json
import os
from flask import jsonify, request, Blueprint, send_from_directory
from flask import current_app as app

from config import ADMINISTRATION_FILE_SEND
from dto.AdministrationDto import AdministrationDto
from project.model import db, Administration
from project.utils.jwt import token_required

administration_bp = Blueprint('administration_bp', __name__)

@administration_bp.route("/addAdministration", methods=["POST"])
@token_required
def add_administration(current_user):
    body = json.loads(request.form['data'])
    name_ru = body['name_ru']
    name_uz = body['name_uz']
    profession_id = body['profession_id']
    files = request.files.getlist('file')
    photo = app.config['UPLOAD_FOLDER_ADMINISTRATION'] + files[0].filename
    files[0].save(photo)
    try:
        administration = Administration(name_ru=name_ru, name_uz=name_uz, photo=request.host_url + photo,
                                       profession_id = profession_id)
        db.session.add(administration)
        db.session.commit()
        return jsonify(
            message="administration added"
        )
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )


# @administration_bp.route("/updateAdministration/<int:id>", methods=["POST"])
# def update_administration(id):
#     try:
#         administration = Administration.query.get(id)
#         body = json.loads(request.form['data'])
#         name = body['name']
#         profession = body['profession']
#         files = request.files.getlist('file')
#         if files[0].filename != "":
#             if os.path.exists(administration.photo): os.remove(administration.photo)
#             photo = app.config['UPLOAD_FOLDER_ADMINISTRATION'] + files[0].filename
#             files[0].save(photo)
#             administration.photo = photo
#         administration.name = name
#         administration.profession = profession
#         db.session.commit()
#         return jsonify(
#             message='administration updated'
#         )
#     except Exception as ex:
#         return jsonify(
#             error=str(ex)
#         )


@administration_bp.route("/deleteAdministration/<int:id>", methods=["POST"])
@token_required
def delete_administrations(current_user,id):
    try:
        administration = Administration.query.get(id)
        photo_url = administration.photo.replace(request.host_url, "")
        if os.path.exists(photo_url): os.remove(photo_url)
        db.session.delete(administration)
        db.session.commit()
        return jsonify(
            message='administration deleted'
        )
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )


@administration_bp.route("/getAdministrations", methods=["GET"])
def get_administrations():
    try:
        args = request.args
        lang = args.get('lang')
        administrations = Administration.query.all()
        listDto = []
        if lang == "uz":
            for item in administrations:
                print(item.profession)
                administration_uz_dto = AdministrationDto(
                    id=item.id,
                    name=item.name_uz,
                    profession=item.profession.name_uz,
                    photo=item.photo
                )
                listDto.append(administration_uz_dto)
            return jsonify(listDto)
        else:
            for item in administrations:
                administration_ru_dto = AdministrationDto(
                    id=item.id,
                    name=item.name_ru,
                    profession=item.profession.name_ru,
                    photo=item.photo
                )
                listDto.append(administration_ru_dto)
            return jsonify(listDto)
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )


@administration_bp.route(ADMINISTRATION_FILE_SEND + "<string:filename>", methods=['GET'])
def administration_photo(filename):
    return send_from_directory("../" + app.config['UPLOAD_FOLDER_ADMINISTRATION'], filename)
