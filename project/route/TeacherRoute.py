import json
import os
from flask import jsonify, request, Blueprint, send_file, send_from_directory
from flask import current_app as app

from config import TEACHER_FILE_SEND
from dto.TeacherDto import TeacherDto
from project.model import db, Teacher
from project.utils.jwt import token_required

teacher_bp = Blueprint('teacher_bp', __name__)


@teacher_bp.route("/addTeacher", methods=["POST"])
@token_required
def add_teacher(current_user):
    body = json.loads(request.form['data'])
    files = request.files.getlist('file')
    timetables = request.files.getlist('timetable')

    photo = app.config['UPLOAD_FOLDER_TEACHER'] + files[0].filename
    timetable = app.config['UPLOAD_FOLDER_TEACHER_TIMETABLE'] + timetables[0].filename

    files[0].save(photo)
    timetables[0].save(timetable)

    name_ru = body['name_ru']
    name_uz = body['name_uz']
    department_id = body['department_id']
    try:
        teacher = Teacher(name_ru=name_ru, name_uz=name_uz, timetable=timetable,
                          photo=request.host_url + photo,
                          department_id=department_id)
        db.session.add(teacher)
        db.session.commit()
        return jsonify(
            message="teacher added"
        )
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )


@teacher_bp.route("/updateTeacherTimetable/<int:id>", methods=["POST"])
@token_required
def update_teacher_timeTable(current_user,id):
    try:
        timetables = request.files.getlist('timetable')
        timetable = app.config['UPLOAD_FOLDER_TEACHER_TIMETABLE'] + timetables[0].filename

        timetables[0].save(timetable)

        teacher = Teacher.query.get(id)
        if os.path.exists(teacher.timetable): os.remove(teacher.timetable)
        teacher.timetable = timetable
        db.session.commit()
        return jsonify(
            message="Teacher Timetable Updated"
        )
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )


@teacher_bp.route("/deleteTeacher/<int:id>", methods=["POST"])
@token_required
def delete_teacher(current_user,id):
    try:
        teacher = Teacher.query.get(id)
        photo_url = teacher.photo.replace(request.host_url, "")
        if os.path.exists(photo_url): os.remove(photo_url)
        if os.path.exists(teacher.timetable): os.remove(teacher.timetable)
        db.session.delete(teacher)
        db.session.commit()
        return jsonify(
            message='teacher deleted'
        )
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )


@teacher_bp.route("/getTeachers", methods=["GET"])
def get_teachers():
    try:
        args = request.args
        lang = args.get('lang')
        teachers = Teacher.query.all()
        listDto = []
        if lang == "ru":
            for item in teachers:
                teacherDto = TeacherDto(
                    id=item.id,
                    photo=item.photo,
                    name=item.name_ru,
                    timetable=item.timetable,
                    department_id=item.department.name_ru
                )
                listDto.append(teacherDto)
        else:
            for item in teachers:
                teacherDto = TeacherDto(
                    id=item.id,
                    photo=item.photo,
                    name=item.name_uz,
                    timetable=item.timetable,
                    department_id=item.department.name_uz
                )
                listDto.append(teacherDto)
        return jsonify(listDto)
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )


@teacher_bp.route(TEACHER_FILE_SEND + "<string:filename>", methods=['GET'])
def teacher_photo(filename):
    return send_from_directory("../" + app.config['UPLOAD_FOLDER_TEACHER'], filename)


@teacher_bp.route('/getTeacherTimetable/<int:id>', methods=["GET"])
def get_document_file(id):
    try:
        teacher = Teacher.query.get(id)
        return send_file("../"+teacher.timetable)
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )
