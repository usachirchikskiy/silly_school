import json
from flask import jsonify, request, Blueprint

from dto.FaqDto import FaqDto
from project.model import db, Faq
from project.utils.jwt import token_required

faq_bp = Blueprint('faq_bp', __name__)


@faq_bp.route("/addFaq", methods=["POST"])
@token_required
def add_faq(current_user):
    body = request.get_json()
    question_ru = body['question_ru']
    question_uz = body['question_uz']
    answer_ru = body['answer_ru']
    answer_uz = body['answer_uz']
    try:
        faq = Faq(question_ru=question_ru, question_uz=question_uz, answer_ru=answer_ru,answer_uz=answer_uz)
        db.session.add(faq)
        db.session.commit()
        return jsonify(
            message="faq added"
        )
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )


@faq_bp.route("/deleteFaq/<int:id>", methods=["POST"])
@token_required
def delete_faq(current_user,id):
    try:
        faq = Faq.query.get(id)
        db.session.delete(faq)
        db.session.commit()
        return jsonify(
            message='faq deleted'
        )
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )

@faq_bp.route("/getFaqs", methods=["GET"])
def get_faqs():
    try:
        args = request.args
        lang = args.get('lang')
        faqs = Faq.query.all()
        listDto = []
        if lang == "ru":
            for item in faqs:
                faqDto = FaqDto(
                    id=item.id,
                    question = str(item.question_ru),
                    answer = str(item.answer_ru)
                )
                listDto.append(faqDto)
        else:
            for item in faqs:
                faqDto = FaqDto(
                    id=item.id,
                    question=str(item.question_uz),
                    answer=str(item.answer_uz)
                )
                listDto.append(faqDto)
        return jsonify(listDto)
    except Exception as ex:
        return jsonify(
            error=str(ex)
        )
