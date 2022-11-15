import json
import os
from flask import jsonify, request, Blueprint, send_file, send_from_directory
from flask import current_app as app

from config import GALLERY_FILE_SEND
from project.model import db, Gallery
from project.schema.GallerySchema import GallerySchema
from project.utils.jwt import token_required

gallery_bp = Blueprint('gallery_bp', __name__)
gallery_schema_many = GallerySchema(many=True)


@gallery_bp.route("/addGallery", methods=["POST"])
@token_required
def add_gallery(current_user):
    files = request.files.getlist('file')
    photo = app.config['UPLOAD_FOLDER_GALLERY'] + files[0].filename
    files[0].save(photo)
    try:
        gallery = Gallery(photo=request.host_url + photo)
        print(request.host_url + photo)
        db.session.add(gallery)
        db.session.commit()
        return jsonify(
            message="gallery added"
        )
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )


@gallery_bp.route("/deleteGallery/<int:id>", methods=["POST"])
@token_required
def delete_gallery(current_user,id):
    try:
        gallery = Gallery.query.get(id)
        photo_url = gallery.photo.replace(request.host_url, "")
        if os.path.exists(photo_url): os.remove(photo_url)
        db.session.delete(gallery)
        db.session.commit()
        return jsonify(
            message='gallery deleted'
        )
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )

@gallery_bp.route("/getAllGalleries", methods=["GET"])
def get_all_gallerys():
    try:
        galleries = Gallery.query.order_by(Gallery.id.desc()).all()
        return jsonify(gallery_schema_many.dump(galleries))
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )


@gallery_bp.route("/getGalleries", methods=["GET"])
def get_gallerys():
    args = request.args
    page = args.get('page')
    per_page = app.config['GALLERY_PER_PAGE']
    try:
        all_pages = 0
        if(Gallery.query.count() % per_page == 0):
            all_pages = int(Gallery.query.count() / per_page)-1
        else:
            all_pages = int(Gallery.query.count() / per_page)
        galleries = Gallery.query.order_by(Gallery.id.desc()).paginate(page=int(page)+1, per_page=per_page, error_out=False)
        return jsonify(
            pages=all_pages,
            data = gallery_schema_many.dump(galleries)
        )
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )

@gallery_bp.route(GALLERY_FILE_SEND + "<string:filename>", methods=['GET'])
def gallery_photo(filename):
    try:
        return send_from_directory("../" + app.config['UPLOAD_FOLDER_GALLERY'], filename)
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )