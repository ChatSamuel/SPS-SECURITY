from flask import Flask, request, jsonify
from sps_security.api.multi_scan import MultiAPI

app = Flask(__name__)
scanner = MultiAPI()


@app.route("/")
def home():
    return {"status": "SPS-SECURITY API ONLINE"}


@app.route("/scan", methods=["POST"])
def scan_file():

    if "file" not in request.files:
        return jsonify({"error": "No file"}), 400

    file = request.files["file"]
    path = f"/tmp/{file.filename}"
    file.save(path)

    result = scanner.scan(path)

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
