#!/usr/bin/python3
""" Reviews view """
from flask import abort
from models import storage
from models.user import User
from models.place import Place
from flask import jsonify, make_response, request
from api.v1.views import app_views, State, City, Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """ Retrives the list of all
        reviews objs base on place_id """
    objs = storage.get(Place, place_id)
    list_reviews = []
    if objs.__class__.__name__ == 'Place':
        for review in objs.reviews:
            list_reviews.append(review.to_dict())
        return jsonify(list_reviews)
    return abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_reviews_by_id(review_id):
    """ Retrieves review object """
    review = storage.get(Review, review_id)
    result = None
    if review.__class__.__name__ == 'Review':
        result = jsonify(review.to_dict())
    else:
        result = abort(404)
    return result


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review_by_id(review_id):
    """ DELETE review by ID """
    review_object = storage.get(Review, review_id)
    result = None
    if review_object.__class__.__name__ == 'Review':
        storage.delete(review_object)
        storage.save()
        result = make_response(jsonify({}), 200)
    else:
        result = abort(404)
    return result


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """ Creates a review obj """
    data = request.get_json()
    place_object = storage.get(Place, place_id)
    if not place_object.__class__.__name__ == 'Place':
        return abort(404)
    if request.is_json:
        if 'user_id' not in data:
            return jsonify({'error': 'Missing user_id'}), 400
        user_object = storage.get(User, data['user_id'])
        if not user_object.__class__.__name__ == 'User':
            return abort(404)
        if 'text' not in data:
            result = jsonify({'error': 'Missing text'}), 400
        else:
            new_object = Review(**data)
            setattr(new_object, 'place_id', place_id)
            storage.new(new_object)
            storage.save()
            result = jsonify(new_object.to_dict()), 201
    else:
        result = jsonify({'error': 'Not a JSON'}), 400
    return result


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_reviews(review_id):
    """ PUT reviews """
    review_object = storage.get(Review, review_id)
    if not review_object.__class__.__name__ == 'Review':
        return abort(404)
    if request.is_json:
        data = request.get_json()
        for key, value in data.items():
            setattr(review_object, key, value)
        storage.save()
        result = jsonify(review_object.to_dict()), 200
    else:
        result = jsonify({'error': 'Not a JSON'}), 400
    return result
