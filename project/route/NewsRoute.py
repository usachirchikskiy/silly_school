import json
import os
from flask import jsonify, request, Blueprint, send_file, send_from_directory, Response
from flask import current_app as app

from config import NEWS_FILE_SEND
from dto.NewsDto import NewsDto
from project.model import db, News
from project.utils.jwt import token_required

news_bp = Blueprint('news_bp', __name__)


@news_bp.route("/addNews", methods=["POST"])
@token_required
def add_news(current_user):
    body = json.loads(request.form['data'])
    files = request.files.getlist('file')
    photo = app.config['UPLOAD_FOLDER_NEWS'] + files[0].filename
    files[0].save(photo)
    name_ru = body['name_ru']
    description_ru = body['description_ru']
    name_uz = body['name_uz']
    description_uz = body['description_uz']
    try:
        news = News(name_ru=name_ru, name_uz=name_uz, description_ru=description_ru, description_uz=description_uz,
                    photo=request.host_url + photo)
        db.session.add(news)
        db.session.commit()
        return jsonify(
            message="news added"
        )
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )


@news_bp.route("/deleteNews/<int:id>", methods=["POST"])
@token_required
def delete_news(current_user,id):
    try:
        news = News.query.get(id)
        photo_url = news.photo.replace(request.host_url, "")
        if os.path.exists(photo_url): os.remove(photo_url)
        db.session.delete(news)
        db.session.commit()
        return jsonify(
            message='news deleted'
        )
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )

# @news_bp.errorhandler(Exception)
@news_bp.route('/getNews/<int:id>', methods=['GET'])
def get_news_id(id):
    args = request.args
    lang = args.get('lang')
    try:
        news = News.query.get(id)
        if lang == "uz":
            news_uz_dto = NewsDto(
                id=news.id,
                name=news.name_uz,
                description=news.description_uz,
                datetime_posted=news.datetime_posted,
                photo=news.photo
            )
            return jsonify(news_uz_dto)
        else:
            news_ru_dto = NewsDto(
                id=news.id,
                name=news.name_ru,
                description=news.description_ru,
                datetime_posted=news.datetime_posted,
                photo=news.photo
            )
            return jsonify(news_ru_dto)
    except Exception as ex:
        return Response(
            "The response body goes here",
            status=400,
        )


@news_bp.route('/getAllNews', methods=['GET'])
def get_all_news():
    args = request.args
    lang = args.get('lang')
    try:
        news = News.query.order_by(News.id.desc()).all()
        listDto = []
        if lang == "uz":
            for item in news:
                news_uz_dto = NewsDto(
                    id=item.id,
                    name=item.name_uz,
                    description=item.description_uz,
                    datetime_posted=item.datetime_posted,
                    photo=item.photo
                )
                listDto.append(news_uz_dto)
        else:
            for item in news:
                news_ru_dto = NewsDto(
                    id=item.id,
                    name=item.name_ru,
                    description=item.description_ru,
                    datetime_posted=item.datetime_posted,
                    photo=item.photo
                )
                listDto.append(news_ru_dto)
        return jsonify(listDto)
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )



@news_bp.route('/getNews', methods=['GET'])
def get_news():
    args = request.args
    page = args.get('page')
    lang = args.get('lang')
    per_page = app.config['NEWS_PER_PAGE']
    try:
        all_pages = 0
        if (News.query.count() % per_page == 0):
            all_pages = int(News.query.count() / per_page) - 1
        else:
            all_pages = int(News.query.count() / per_page)
        news = News.query.order_by(News.id.desc()).paginate(page=int(page)+1, per_page=per_page, error_out=False)
        listDto = []
        if lang == "uz":
            for item in news:
                news_uz_dto = NewsDto(
                    id=item.id,
                    name=item.name_uz,
                    description=item.description_uz,
                    datetime_posted=item.datetime_posted,
                    photo=item.photo
                )
                listDto.append(news_uz_dto)
        else:
            for item in news:
                news_ru_dto = NewsDto(
                    id=item.id,
                    name=item.name_ru,
                    description=item.description_ru,
                    datetime_posted=item.datetime_posted,
                    photo=item.photo
                )
                listDto.append(news_ru_dto)
        return jsonify(
            pages = all_pages,
            data = listDto
        )
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )


@news_bp.route(NEWS_FILE_SEND + "<string:filename>", methods=['GET'])
def department_photo(filename):
    return send_from_directory("../" + app.config['UPLOAD_FOLDER_NEWS'], filename)
