import json
import os
from flask import jsonify, request, Blueprint

from project.model import SchoolInfo, db
from project.schema.SchoolInfoSchema import SchoolInfoSchema
from project.utils.jwt import token_required

school_info_bp = Blueprint('school_info', __name__)
school_info_schema = SchoolInfoSchema()


@school_info_bp.route("/addSchoolInfo", methods=["POST"])
@token_required
def add_school_info(current_user):
    body = request.get_json()
    school_number = body['school_number']
    telephone_number = body['telephone_number']
    location_name = body['location_name']
    location_url = body['location_url']
    telegram_url = body['telegram_url']
    instagram_url = body['instagram_url']
    facebook_url = body['facebook_url']
    youtube_url = body['youtube_url']

    try:
        school_info = SchoolInfo(school_number=school_number, telephone_number=telephone_number, location_name=location_name,
                                 location_url=location_url,telegram_url=telegram_url,instagram_url=instagram_url,
                                 facebook_url=facebook_url,youtube_url=youtube_url)
        db.session.add(school_info)
        db.session.commit()
        return jsonify(
            message="school_info added"
        )
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )

@school_info_bp.route("/updateSchoolInfo/<int:id>", methods=["POST"])
@token_required
def update_school_info(current_user,id):
    try:
        school_info = SchoolInfo.query.get(id)
        body = request.get_json()
        school_number = body['school_number']
        telephone_number = body['telephone_number']
        location_name = body['location_name']
        location_url = body['location_url']
        telegram_url = body['telegram_url']
        instagram_url = body['instagram_url']
        facebook_url = body['facebook_url']
        youtube_url = body['youtube_url']

        school_info.school_number = school_number
        school_info.telephone_number = telephone_number
        school_info.location_name = location_name
        school_info.location_url = location_url
        school_info.telegram_url = telegram_url
        school_info.instagram_url = instagram_url
        school_info.facebook_url = facebook_url
        school_info.youtube_url = youtube_url
        db.session.commit()
        return jsonify(
            message='school_info updated'
        )
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )


@school_info_bp.route("/getSchoolInfo/<int:id>", methods=["GET"])
def get_school_info(id):
    try:
        school_info = SchoolInfo.query.get(id)
        return jsonify(school_info_schema.dump(school_info))
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )
