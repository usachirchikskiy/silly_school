import json
import os
from flask import jsonify, request, Blueprint, send_file
from flask import current_app as app

from dto.DocumentDto import DocumentDto
from project.model import db, Document
from project.utils.jwt import token_required

document_bp = Blueprint('document_bp', __name__)


@document_bp.route("/addDocument", methods=["POST"])
@token_required
def add_document(current_user):
    body = json.loads(request.form['data'])
    name_ru = body['name_ru']
    name_uz = body['name_uz']
    files = request.files.getlist('file')
    file = app.config['UPLOAD_FOLDER_DOCUMENT'] + files[0].filename
    files[0].save(file)
    try:
        document = Document(name_ru=name_ru, name_uz=name_uz, file=file)
        db.session.add(document)
        db.session.commit()
        return jsonify(
            message="document added"
        )
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )


@document_bp.route("/deleteDocument/<int:id>", methods=["POST"])
@token_required
def delete_document(current_user,id):
    try:
        document = Document.query.get(id)
        if os.path.exists(document.file): os.remove(document.file)
        db.session.delete(document)
        db.session.commit()
        return jsonify(
            message='document deleted'
        )
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )


@document_bp.route("/getDocuments", methods=["GET"])
def get_documents():
    try:
        args = request.args
        lang = args.get('lang')
        documents = Document.query.all()
        listDto = []
        if lang == "uz":
            for item in documents:
                documents_uz_dto = DocumentDto(
                    id=item.id,
                    name=item.name_uz,
                    file=item.file
                )
                listDto.append(documents_uz_dto)
        else:
            for item in documents:
                documents_ru_dto = DocumentDto(
                    id=item.id,
                    name=item.name_ru,
                    file=item.file
                )
                listDto.append(documents_ru_dto)
        return jsonify(listDto)
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )


@document_bp.route('/getDocumentFile/<int:id>', methods=["GET"])
def get_document_file(id):
    try:
        document = Document.query.get(id)
        return send_file("../" + document.file)
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )
