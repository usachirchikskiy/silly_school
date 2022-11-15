import json
import os
from flask import jsonify, request, Blueprint

from dto.ProfessionDto import ProfessionDto
from project.model import Profession, db
from project.utils.jwt import token_required

profession_bp = Blueprint('profession', __name__)


@profession_bp.route("/addStaticProfession", methods=["POST"])
def add_static_profession():
    director = {
        "name_ru": "Директор",
        "name_uz": "Director",
    }
    manager_supply = {
        "name_ru": "Заместитель директора по хозяйственной части",
        "name_uz": "Xo`jalik ishlari bo'yicha direktor o'rinbosari",
    }
    manager = {
        "name_ru": "Заместитель директора по учёбной части",
        "name_uz": "O‘quv ishlari bo‘yicha direktor o‘rinbosari",
    }
    accountant = {
        "name_ru": "Бухгалтер",
        "name_uz": "Buxgalter",
    }
    secretar = {
        "name_ru": "Секретарь",
        "name_uz": "Sekretar",
    }
    professions = [director, manager_supply, manager, accountant, secretar]
    for item in professions:
        profession = Profession(name_ru=item["name_ru"], name_uz=item["name_uz"], )
        db.session.add(profession)
        db.session.commit()
    return jsonify(
        message="profession created"
    )


@profession_bp.route("/deleteProfession/<int:id>", methods=["POST"])
@token_required
def delete_profession(current_user,id):
    try:
        profession = Profession.query.get(id)
        db.session.delete(profession)
        db.session.commit()
        return jsonify(
            message='profession deleted'
        )
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )


@profession_bp.route("/getProfessions", methods=["GET"])
def get_professions():
    try:
        args = request.args
        lang = args.get('lang')
        professions = Profession.query.all()
        listDto = []
        if lang == "ru":
            for item in professions:
                profession = ProfessionDto(
                    id=item.id,
                    name=item.name_ru,
                )
                listDto.append(profession)
        else:
            for item in professions:
                profession = ProfessionDto(
                    id=item.id,
                    name=item.name_uz,
                )
                listDto.append(profession)
        return jsonify(listDto)
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )
