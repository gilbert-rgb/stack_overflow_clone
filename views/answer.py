from flask import Blueprint, request, jsonify
from models import db, Answer, Question, User
from datetime import datetime

answer_bp = Blueprint("answer_bp", __name__)

# Create an answer
@answer_bp.route("/answers", methods=["POST"])
def create_answer():
    data = request.get_json()
    body = data.get("body")
    user_id = data.get("user_id")
    question_id = data.get("question_id")

    if not all([body, user_id, question_id]):
        return jsonify({"error": "Body, user_id, and question_id are required"}), 400

    # Check user and question exist
    if not User.query.get(user_id):
        return jsonify({"error": "User not found"}), 404
    if not Question.query.get(question_id):
        return jsonify({"error": "Question not found"}), 404

    answer = Answer(body=body, user_id=user_id, question_id=question_id, created_at=datetime.utcnow())
    db.session.add(answer)
    db.session.commit()

    return jsonify({"success": "Answer created", "answer_id": answer.id}), 201

# Get answers for a specific question
@answer_bp.route("/questions/<int:question_id>/answers", methods=["GET"])
def get_answers_for_question(question_id):
    answers = Answer.query.filter_by(question_id=question_id).all()
    return jsonify([{
        "id": ans.id,
        "body": ans.body,
        "user_id": ans.user_id,
        "is_hidden": ans.is_hidden,
        "created_at": ans.created_at
    } for ans in answers]), 200

# Delete an answer
@answer_bp.route("/answers/<int:answer_id>", methods=["DELETE"])
def delete_answer(answer_id):
    answer = Answer.query.get(answer_id)
    if not answer:
        return jsonify({"error": "Answer not found"}), 404

    db.session.delete(answer)
    db.session.commit()
    return jsonify({"success": "Answer deleted"}), 200
