from flask import Flask


app = Flask(__name__)


@app.route("/", methods=['GET'])
def main():
    return "API running..."


if __name__ == '__main__':
    # Run on the network
    app.run(host='0.0.0.0', port=5000, debug=True)