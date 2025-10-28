from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, World!'}), 200


@app.route('/test', methods=['POST'])
def test():
    data = request.get_json()
    return jsonify(data), 200


if __name__ == '__main__':
    app.run(debug=True)
