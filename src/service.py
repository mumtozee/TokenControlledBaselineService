from flask import Flask, request, jsonify
from src.da_bot import gen_response_batch, gen_response

app = Flask(__name__)


@app.route('/')
def hello():
    return "<h1>Hello, World</h1>"


@app.route("/respond", methods=["POST", "GET"])
def respond():
    try:
        req_data = request.get_json(force=True)
        print(f"data ----> {req_data}")
        history = req_data["history"]
        response = gen_response(history)
        return jsonify({
            "code": 0,
            "message": "ok",
            "data": response
        })

    except Exception as e:
        return jsonify({
            "code": 1,
            "message": f"Error: {e}",
            "data": None
        })


@app.route("/respond_batch", methods=["POST", "GET"])
def respond_batch():
    try:
        req_data = request.get_json(force=True)
        print(f"data ----> {req_data}")
        histories = req_data["histories"]
        responses = gen_response_batch(histories)
        return jsonify({
            "code": 0,
            "message": "ok",
            "data": responses
        })

    except Exception as e:
        return jsonify({
            "code": 1,
            "message": f"Error: {e}",
            "data": None
        })
