import os
from flask import jsonify, request, Blueprint, send_from_directory, send_file
from flask import current_app as app

from config import ACHIEVEMENT_FILE_SEND
from project.model import Achievement, db
from project.schema.AchievementSchema import AchievementSchema
from project.utils.jwt import token_required

achievement_bp = Blueprint('achievement_bp', __name__)
achievement_schema_many = AchievementSchema(many=True)


@achievement_bp.route("/addAchievement", methods=["POST"])
@token_required
def add_achievement(current_user):
    files = request.files.getlist('file')
    photo = app.config['UPLOAD_FOLDER_ACHIEVEMENT'] + files[0].filename
    files[0].save(photo)
    try:
        achievement = Achievement(photo=request.host_url + photo)
        db.session.add(achievement)
        db.session.commit()
        return jsonify(
            message="achievement added"
        )
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )


@achievement_bp.route("/deleteAchievement/<int:id>", methods=["POST"])
@token_required
def delete_achievements(current_user,id):
    try:
        achievement = Achievement.query.get(id)
        photo_url = achievement.photo.replace(request.host_url, "")
        if os.path.exists(photo_url): os.remove(photo_url)
        db.session.delete(achievement)
        db.session.commit()
        return jsonify(
            message='achievement deleted'
        )
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )


@achievement_bp.route("/getAchievements", methods=["GET"])
def get_achievements():
    try:
        achievements = Achievement.query.all()
        return jsonify(achievement_schema_many.dump(achievements))
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )


@achievement_bp.route(ACHIEVEMENT_FILE_SEND + "<string:filename>",methods = ['GET'])
def achievement_photo(filename):
    return send_from_directory("../"+app.config['UPLOAD_FOLDER_ACHIEVEMENT'],filename)
