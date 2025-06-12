from flask import Blueprint, request, jsonify
from models import db, Question, User
from datetime import datetime

question_bp = Blueprint("question_bp", __name__)

# Create a new question
@question_bp.route("/questions", methods=["POST"])
def create_question():
    data = request.get_json()
    title = data.get("title")
    body = data.get("body")
    tags = data.get("tags")
    user_id = data.get("user_id")

    if not all([title, body, tags, user_id]):
        return jsonify({"error": "Title, body, tags, and user_id are required"}), 400

    existing_question = Question.query.filter_by(title=title).first()
    if existing_question:
        return jsonify({"error": "Question with this title already exists"}), 400

    # Check if user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    question = Question(
        title=title,
        body=body,
        tags=tags,
        user_id=user_id,
        created_at=datetime.utcnow()
    )
    db.session.add(question)
    db.session.commit()

    return jsonify({"success": "Question created", "question_id": question.id}), 201


# Get all questions
@question_bp.route("/questions", methods=["GET"])
def get_all_questions():
    questions = Question.query.all()
    result = []
    for q in questions:
        result.append({
            "id": q.id,
            "title": q.title,
            "body": q.body,
            "tags": q.tags,
            "is_approved": q.is_approved,
            "user_id": q.user_id,
            "created_at": q.created_at
        })
    return jsonify(result), 200


# Get a specific question by ID
@question_bp.route("/questions/<int:question_id>", methods=["GET"])
def get_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    return jsonify({
        "id": question.id,
        "title": question.title,
        "body": question.body,
        "tags": question.tags,
        "is_approved": question.is_approved,
        "user_id": question.user_id,
        "created_at": question.created_at
    }), 200


# Delete a question
@question_bp.route("/questions/<int:question_id>", methods=["DELETE"])
def delete_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({"success": "Question deleted successfully"}), 200
