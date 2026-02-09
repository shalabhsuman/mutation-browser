from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os
from uuid import uuid4
from datetime import datetime, timezone

from backend.celery_app import log_query_event

app = Flask(__name__)
CORS(app)

# Database connection settings (environment-based)
DB_NAME = os.getenv("DB_NAME", "mutation_browser")
DB_USER = os.getenv("DB_USER", os.getenv("USER"))
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))


def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/status/<request_id>", methods=["GET"])
def get_status(request_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT request_id, gene, requested_at, status
        FROM query_events
        WHERE request_id = %s
        """,
        (request_id,)
    )
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return jsonify({"error": "request_id not found"}), 404

    return jsonify({
        "request_id": row[0],
        "gene": row[1],
        "requested_at": row[2].isoformat(),
        "status": row[3],
    })


@app.route("/variants", methods=["GET"])
def get_variants():
    gene = request.args.get("gene")

    if not gene:
        return jsonify({"error": "gene parameter is required"}), 400

    request_id = str(uuid4())
    payload = {
        "request_id": request_id,
        "gene": gene,
        "requested_at": datetime.now(timezone.utc).isoformat(),
        "status": "received",
    }

    # Fire-and-forget async logging (do not block request/response).
    log_query_event.delay(payload)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT sample_id, gene, variant, vaf, tumor_type
        FROM variants
        WHERE gene = %s
        """,
        (gene,)
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    results = []
    for r in rows:
        results.append({
            "sample_id": r[0],
            "gene": r[1],
            "variant": r[2],
            "vaf": r[3],
            "tumor_type": r[4],
        })

    return jsonify({
        "request_id": request_id,
        "results": results,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
