from flask import jsonify


def ok_jsonify(payload):
    return jsonify(status=200, title='OK', payload=payload)