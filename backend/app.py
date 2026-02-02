from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Database connection settings
DB_NAME = "mutation_browser"
DB_USER = os.getenv("USER")   # your macOS username
DB_HOST = "localhost"
DB_PORT = 5432


def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT
    )


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/variants", methods=["GET"])
def get_variants():
    gene = request.args.get("gene")

    if not gene:
        return jsonify({"error": "gene parameter is required"}), 400

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

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True, port=5000)