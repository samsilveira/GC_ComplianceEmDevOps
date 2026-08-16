from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify(
        {
            "message": "Bem-vindo à API do experimento de Compliance em DevOps!",
            "version": "1.0.0",
        }
    )


@app.route("/health")
def health():
    return jsonify({"status": "up", "healthy": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
