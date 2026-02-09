import os
import psycopg2
from celery import Celery


def make_celery():
    broker_url = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@localhost:5672//")
    backend_url = os.getenv("CELERY_RESULT_BACKEND", "rpc://")

    app = Celery(
        "mutation_browser",
        broker=broker_url,
        backend=backend_url,
    )

    app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
    )

    return app


celery_app = make_celery()


@celery_app.task(name="log_query_event")
def log_query_event(payload):
    db_name = os.getenv("DB_NAME", "mutation_browser")
    db_user = os.getenv("DB_USER", os.getenv("USER"))
    db_password = os.getenv("DB_PASSWORD", "")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = int(os.getenv("DB_PORT", "5432"))

    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
    )

    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO query_events (request_id, gene, requested_at, status)
            VALUES (%s, %s, %s, %s)
            """,
            (
                payload["request_id"],
                payload["gene"],
                payload["requested_at"],
                payload["status"],
            ),
        )
        conn.commit()
        cur.close()
    finally:
        conn.close()

    return {"status": "logged", "request_id": payload["request_id"]}
