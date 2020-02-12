from flask import jsonify
from copy import copy

api_response = {
    'status': 200,
    'title': 'OK',
    'detail': 'The request was fulfilled.',
    'payload': None
}


def api_jsonify(payload=None):
    if payload is None:
        payload = {}
    ret = copy(api_response)
    ret['payload'] = payload
    return jsonify(ret)
