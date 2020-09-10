#!/usr/bin/python3
""" Place view """
from flask import jsonify, make_response, request
from api.v1.views import app_views, State, City
from models import storage
from models.place import Place
from models.user import User
from flask import abort


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """ Retrives the list of all
        places objs base on city id """
    objs = storage.get(City, city_id)
    list_places = []
    if objs.__class__.__name__ == 'City':
        for place in objs.places:
            list_places.append(place.to_dict())
        return jsonify(list_places)
    return abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_places_by_id(place_id):
    """ Retrieves place object """
    place = storage.get(Place, place_id)
    result = None
    if place.__class__.__name__ == 'Place':
        result = jsonify(place.to_dict())
    else:
        result = abort(404)
    return result


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_by_id(place_id):
    """ DELETE place by ID """
    place_object = storage.get(Place, place_id)
    result = None
    if place_object.__class__.__name__ == 'Place':
        storage.delete(place_object)
        storage.save()
        result = make_response(jsonify({}), 200)
    else:
        result = abort(404)
    return result


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """ Creates a place obj """
    data = request.get_json()
    city_object = storage.get(City, city_id)
    if not city_object.__class__.__name__ == 'City':
        return abort(404)
    if request.is_json:
        if 'user_id' not in data:
            return jsonify({'error': 'Missing user_id'}), 400
        user_object = storage.get(User, data['user_id'])
        if not user_object.__class__.__name__ == 'User':
            return abort(404)
        if 'name' not in data:
            result = jsonify({'error': 'Missing name'}), 400
        else:
            new_object = Place(**data)
            setattr(new_object, 'city_id', city_id)
            storage.new(new_object)
            storage.save()
            result = jsonify(new_object.to_dict()), 201
    else:
        result = jsonify({'error': 'Not a JSON'}), 400
    return result


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_places(place_id):
    """ PUT places """
    place_object = storage.get(Place, place_id)
    if not place_object.__class__.__name__ == 'Place':
        return abort(404)
    if request.is_json:
        data = request.get_json()
        for key, value in data.items():
            setattr(place_object, key, value)
        storage.save()
        result = jsonify(place_object.to_dict()), 200
    else:
        result = jsonify({'error': 'Not a JSON'}), 400
    return result
