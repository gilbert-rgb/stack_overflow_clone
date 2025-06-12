from flask import Blueprint, request, jsonify
from models import db, Vote, Question, Answer, User
from datetime import datetime

vote_bp = Blueprint("vote_bp", __name__)

# Cast a vote (either on a question or an answer)
@vote_bp.route("/votes", methods=["POST"])
def cast_vote():
    data = request.get_json()
    user_id = data.get("user_id")
    question_id = data.get("question_id")
    answer_id = data.get("answer_id")
    value = data.get("value")  # Should be 1 or -1

    if value not in [1, -1]:
        return jsonify({"error": "Vote value must be 1 (upvote) or -1 (downvote)"}), 400

    if (question_id is None) == (answer_id is None):
        return jsonify({"error": "Vote must be for either a question or an answer, not both or neither"}), 400

    if not User.query.get(user_id):
        return jsonify({"error": "User not found"}), 404

    # Check for duplicates
    existing_vote = Vote.query.filter_by(
        user_id=user_id,
        question_id=question_id,
        answer_id=answer_id
    ).first()
    if existing_vote:
        return jsonify({"error": "You have already voted"}), 400

    vote = Vote(
        user_id=user_id,
        question_id=question_id,
        answer_id=answer_id,
        value=value,
        created_at=datetime.utcnow()
    )
    db.session.add(vote)
    db.session.commit()
    return jsonify({"success": "Vote registered"}), 201

# Get vote count for a question or answer
@vote_bp.route("/votes/count", methods=["GET"])
def vote_count():
    question_id = request.args.get("question_id", type=int)
    answer_id = request.args.get("answer_id", type=int)

    if (question_id is None) == (answer_id is None):
        return jsonify({"error": "Provide either question_id or answer_id"}), 400

    query = Vote.query
    if question_id:
        votes = query.filter_by(question_id=question_id).all()
    else:
        votes = query.filter_by(answer_id=answer_id).all()

    upvotes = sum(1 for v in votes if v.value == 1)
    downvotes = sum(1 for v in votes if v.value == -1)

    return jsonify({
        "upvotes": upvotes,
        "downvotes": downvotes,
        "total": upvotes + downvotes
    }), 200
