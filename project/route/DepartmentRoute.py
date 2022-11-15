import json
import os
from flask import jsonify, request, Blueprint, send_file, send_from_directory, Response
from flask import current_app as app

from config import DEPARTMENT_FILE_SEND
from dto.DepartmentDto import DepartmentDto
from dto.TeacherDto import TeacherDto
from project.model import db, Department
from project.utils.jwt import token_required

department_bp = Blueprint('department_bp', __name__)


@department_bp.route("/addStaticDepartments", methods=["POST"])
def add_static_departments():
    piano = {
        "name_ru": "Фортепиано",
        "name_uz": "Fortepiano",
        "photo": request.host_url + "photos/department_photos/Фортепиано.png",
        "description_ru": "",
        "description_uz": ""
    }
    brass = {
        "name_ru": "Духовые и ударные инструменты",
        "name_uz": "Damli va zarbli cholg`ular",
        "photo": request.host_url + "photos/department_photos/Духовые и ударные инструменты.png",
        "description_ru": "",
        "description_uz": ""
    }
    folk = {
        "name_ru": "Народные инструменты",
        "name_uz": "Xalq cholg`ulari",
        "photo": request.host_url + "photos/department_photos/Народные инструменты.png",
        "description_ru": "",
        "description_uz": ""
    }
    string_instr = {
        "name_ru": "Струнные инструменты",
        "name_uz": "Torli cholg`ular",
        "photo": request.host_url + "photos/department_photos/Струнные инструменты.png",
        "description_ru": "",
        "description_uz": ""
    }
    folk_instrumental = {
        "name_ru": "Традиционное исполнение",
        "name_uz": "An`anaviy cholg`u ijrochiligi",
        "photo": request.host_url + "photos/department_photos/Народные инструменты.png",
        "description_ru": "",
        "description_uz": ""
    }
    folk_vocal = {
        "name_ru": "Традиционное пение",
        "name_uz": "An`anaviy xonandalik",
        "photo": request.host_url + "photos/department_photos/Народное пение.png",
        "description_ru": "",
        "description_uz": ""
    }
    stage_instrumental = {
        "name_ru": "Эстрадное исполнение",
        "name_uz": "Estrada ijrochilik",
        "photo": request.host_url + "photos/department_photos/Эстрадное_исполнение_инструменты.png",
        "description_ru": "",
        "description_uz": ""
    }
    stage_vocal = {
        "name_ru": "Эстрадное пение",
        "name_uz": "Estrada xonandalik",
        "photo": request.host_url + "photos/department_photos/Эстрадный вокал.png",
        "description_ru": "",
        "description_uz": ""
    }
    choir = {
        "name_ru": "Академический хор",
        "name_uz": "Akademik xor",
        "photo": request.host_url + "photos/department_photos/хор.png",
        "description_ru": "",
        "description_uz": ""
    }
    drawing = {
        "name_ru": "Изобразительное искусство",
        "name_uz": "Tasviriy san`at",
        "photo": request.host_url + "photos/department_photos/Изобразительное исскуство.png",
        "description_ru": "",
        "description_uz": ""
    }
    drawing_do = {
        "name_ru": "Прикладное исскуство",
        "name_uz": "Amaliy san`at",
        "photo": request.host_url + "photos/department_photos/Прикладное исскуство.png",
        "description_ru": "",
        "description_uz": ""
    }
    dance = {
        "name_ru": "Хореография",
        "name_uz": "Xoreografiya",
        "photo": request.host_url + "photos/department_photos/Хореография.png",
        "description_ru": "",
        "description_uz": ""
    }
    theatre = {
        "name_ru": "Театральное исскуство",
        "name_uz": "Teatr san`ati",
        "photo": request.host_url + "photos/department_photos/Театральное исскусство.png",
        "description_ru": "",
        "description_uz": ""
    }
    baxshi = {
        "name_ru": "Бахшичилик",
        "name_uz": "Baxshichilik",
        "photo": request.host_url + "photos/department_photos/Бахшичилик_тоже_пение_узбекское.png",
        "description_ru": "",
        "description_uz": ""
    }
    departments = [piano, brass, folk, string_instr, folk_instrumental, folk_vocal,
                   stage_instrumental, stage_vocal, choir, drawing, drawing_do, dance, theatre, baxshi]
    for item in departments:
        department = Department(name_ru=item["name_ru"], name_uz=item["name_uz"], description_ru=item["description_ru"],
                                description_uz=item["description_uz"], photo=item["photo"])
        db.session.add(department)
        db.session.commit()
    return jsonify(
        message="departments created"
    )


# @department_bp.route("/addDepartment", methods=["POST"])
# def add_department():
#     body = json.loads(request.form['data'])
#     name_ru = body['name_ru']
#     name_uz = body['name_uz']
#     description_ru = body['description_ru']
#     description_uz = body['description_ru']
#     files = request.files.getlist('file')
#     photo = app.config['UPLOAD_FOLDER_DEPARTMENT'] + files[0].filename
#     files[0].save(photo)
#     try:
#         department = Department(name_ru=name_ru, name_uz=name_uz, description_ru=description_ru,
#                                 description_uz=description_uz, photo=request.host_url  + photo)
#         db.session.add(department)
#         db.session.commit()
#         return jsonify(
#             message="department added"
#         )
#     except Exception as ex:
#         return jsonify(
#             error=str(ex)
#         )


@department_bp.route("/updateDepartmentDescription/<int:id>", methods=["POST"])
@token_required
def update_department_description(current_user, id):
    try:
        body = request.get_json()
        department = Department.query.get(id)
        department.description_ru = body["description_ru"]
        department.description_uz = body["description_uz"]
        db.session.commit()
        return jsonify(
            message="department description updated"
        )
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )


@department_bp.route("/deleteDepartment/<int:id>", methods=["POST"])
@token_required
def delete_department(current_user, id):
    try:
        department = Department.query.get(id)
        photo_url = department.photo.replace(request.host_url, "")
        if os.path.exists(photo_url): os.remove(photo_url)
        db.session.delete(department)
        db.session.commit()
        return jsonify(
            message='department deleted'
        )
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )


@department_bp.route("/getDepartment/<int:id>", methods=["GET"])
def get_department_id(id):
    try:
        args = request.args
        lang = args.get('lang')
        departments = Department.query.get(id)
        if lang == "ru":
            teachersList = []
            for teacher in departments.teachers:
                teacherDto = TeacherDto(
                    id=teacher.id,
                    photo=teacher.photo,
                    name=teacher.name_ru,
                    timetable=teacher.timetable,
                    department_id=teacher.department_id
                )
                teachersList.append(teacherDto)
            department = DepartmentDto(
                id=departments.id,
                name=departments.name_ru,
                photo=departments.photo,
                description=departments.description_ru,
                teachers=teachersList  # item.teachers
            )
            return jsonify(department)
        else:
            teachersList = []
            for teacher in departments.teachers:
                teacherDto = TeacherDto(
                    id=teacher.id,
                    photo=teacher.photo,
                    name=teacher.name_uz,
                    timetable=teacher.timetable,
                    department_id=teacher.department_id
                )
                teachersList.append(teacherDto)
            department = DepartmentDto(
                id=departments.id,
                name=departments.name_uz,
                photo=departments.photo,
                description=departments.description_uz,
                teachers=teachersList  # item.teachers
            )
            return jsonify(department)
    except Exception as ex:
        return Response(
            str(ex),
            status=400,
        )


@department_bp.route("/getDepartments", methods=["GET"])
def get_departments():
    try:
        args = request.args
        lang = args.get('lang')
        departments = Department.query.order_by(Department.id.asc()).all()
        listDto = []
        if lang == "ru":
            for item in departments:
                teachersList = []
                for teacher in item.teachers:
                    teacherDto = TeacherDto(
                        id=teacher.id,
                        photo=teacher.photo,
                        name=teacher.name_ru,
                        timetable=teacher.timetable,
                        department_id=teacher.department.name_ru
                    )
                    teachersList.append(teacherDto)
                department = DepartmentDto(
                    id=item.id,
                    name=item.name_ru,
                    photo=item.photo,
                    description=item.description_ru,
                    teachers=teachersList  # item.teachers
                )
                listDto.append(department)
        else:
            for item in departments:
                teachersList = []
                for teacher in item.teachers:
                    teacherDto = TeacherDto(
                        id=teacher.id,
                        photo=teacher.photo,
                        name=teacher.name_uz,
                        timetable=teacher.timetable,
                        department_id=teacher.department.name_uz
                    )
                    teachersList.append(teacherDto)
                department = DepartmentDto(
                    id=item.id,
                    name=item.name_uz,
                    photo=item.photo,
                    description=item.description_uz,
                    teachers=teachersList
                )
                listDto.append(department)
        return jsonify(listDto)
    except Exception as ex:
        return Response(
            "The response body goes here",
            status=400,
        )


@department_bp.route(DEPARTMENT_FILE_SEND + "<string:filename>", methods=['GET'])
def department_photo(filename):
    return send_from_directory("../" + app.config['UPLOAD_FOLDER_DEPARTMENT'], filename)
