import os
from flask import Flask, jsonify, render_template, request
import requests

# Point this to your FastAPI GraphQL endpoint (the Strawberry router prefix)
# Examples:
#   http://localhost:8000/greetings
#   https://your.domain/greetings
FASTAPI_GRAPHQL_URL = os.getenv(
    "FASTAPI_GRAPHQL_URL", "http://localhost:8000/v1/graphql"
)

app = Flask(__name__, static_folder="static", template_folder="templates")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.post("/ask")
def ask():
    data = request.get_json(silent=True) or {}
    question = (data.get("question") or "").strip()
    if not question:
        return jsonify({"error": "Missing 'question'"}), 400

    # GraphQL payload to call your field: askAQuestion(question: String!): String
    payload = {
        "query": "query($q:String!){ askAQuestion(question:$q) }",
        "variables": {"q": question},
    }

    try:
        resp = requests.post(
            FASTAPI_GRAPHQL_URL,
            json=payload,
            timeout=30,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "flask-frontend/1.0",
            },
        )
        resp.raise_for_status()
        body = resp.json()

        if "errors" in body:
            # Surface GraphQL errors nicely
            return jsonify({"error": body["errors"]}), 502

        answer = body.get("data", {}).get("askAQuestion")
        return jsonify({"answer": answer})
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 502


if __name__ == "__main__":
    # Run Flask dev server
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5070")), debug=True)
