"""
Reviews controller module
"""

from flask import abort, request
from src.models.review import Review


def get_reviews():
    """Returns all reviews"""
    reviews = Review.get_all()

    return [review.to_dict() for review in reviews], 200


def create_review(place_id: str, data: dict):
    """Creates a new review"""
    try:
        review = Review.create(data | {"place_id": place_id})
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(400, str(e))

    return review.to_dict(), 201


def get_reviews_from_place(place_id: str):
    """Returns all reviews from a specific place"""
    reviews = Review.get_all()

    return [
        review.to_dict() for review in reviews
        if review.place_id == place_id
    ], 200


def get_reviews_from_user(user_id: str):
    """Returns all reviews from a specific user"""
    reviews = Review.get_all()

    return [
        review.to_dict() for review in reviews
        if review.user_id == user_id
    ], 200


def get_review_by_id(review_id: str):
    """Returns a review by ID"""
    review: Review | None = Review.get(review_id)

    if not review:
        abort(404, f"Review with ID {review_id} not found")

    return review.to_dict(), 200


def update_review(review_id: str, data: dict):
    """Updates a review by ID"""
    try:
        review: Review | None = Review.update(review_id, data)
    except ValueError as e:
        abort(400, str(e))

    if not review:
        abort(404, f"Review with ID {review_id} not found")

    return review.to_dict(), 200


def delete_review(review_id: str):
    """Deletes a review by ID"""
    if not Review.delete(review_id):
        abort(404, f"Review with ID {review_id} not found")

    return "", 204
