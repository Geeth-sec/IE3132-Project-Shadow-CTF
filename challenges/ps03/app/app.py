from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    abort,
    send_from_directory,
)
import os
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "portal.db"
EVIDENCE_DIR = Path("/evidence")

app = Flask(__name__)

# Configuration
app.secret_key = os.environ.get("SECRET_KEY", "project-shadow-dev-secret")

PORTAL_USERNAME = os.environ.get("PORTAL_USERNAME", "shadow_dev")
PORTAL_ACCESS_PHRASE = os.environ.get(
    "PORTAL_ACCESS_PHRASE",
    "ShadowAccess27"
)

# The real Stage 3 flag will be supplied through Docker later.
STAGE3_FLAG = os.environ.get(
    "STAGE3_FLAG",
    "CyberTrace{S3_NOT_CONFIGURED}"
)


def get_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db()

    connection.execute("DROP TABLE IF EXISTS documents")

    connection.execute(
        """
        CREATE TABLE documents (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            owner TEXT NOT NULL,
            restricted INTEGER NOT NULL DEFAULT 0
        )
        """
    )

    documents = [
        (
            1,
            "Project Shadow Build Notes",
            "Development build completed. Internal testing is continuing.",
            "shadow_dev",
            0,
        ),
        (
            2,
            "Restricted Model Release Record",
            "Confidential release record for Project Shadow.",
            "release_admin",
            1,
        ),
        (
            3,
            "Developer Testing Checklist",
            "Unit testing completed. Integration review is pending.",
            "shadow_dev",
            0,
        ),
    ]

    connection.executemany(
        """
        INSERT INTO documents
        (id, title, content, owner, restricted)
        VALUES (?, ?, ?, ?, ?)
        """,
        documents,
    )

    connection.commit()
    connection.close()


@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))

    return redirect(url_for("documents"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username", "")
        access_phrase = request.form.get("access_phrase", "")

        if (
            username == PORTAL_USERNAME
            and access_phrase == PORTAL_ACCESS_PHRASE
        ):
            session["user"] = username
            return redirect(url_for("documents"))

        error = "Invalid username or access phrase."

    return render_template("login.html", error=error)


@app.route("/documents")
def documents():
    if "user" not in session:
        return redirect(url_for("login"))

    connection = get_db()

    # Correctly displays only documents belonging to the logged-in user.
    rows = connection.execute(
        """
        SELECT id, title
        FROM documents
        WHERE owner = ? AND restricted = 0
        ORDER BY id
        """,
        (session["user"],),
    ).fetchall()

    connection.close()

    return render_template("documents.html", documents=rows)


@app.route("/document/<int:document_id>")
def document(document_id):
    if "user" not in session:
        return redirect(url_for("login"))

    connection = get_db()

    document_row = connection.execute(
        """
        SELECT *
        FROM documents
        WHERE id = ?
        """,
        (document_id,),
    ).fetchone()

    connection.close()

    if document_row is None:
        abort(404)

    # INTENTIONAL CTF VULNERABILITY:
    # Authentication is checked, but ownership/authorization is NOT checked.
    # This produces the intended IDOR / broken object-level authorization flaw.

    flag = None

    if document_row["restricted"]:
        flag = STAGE3_FLAG
        session["restricted_seen"] = True

    return render_template(
        "document.html",
        document=document_row,
        flag=flag,
    )


@app.route("/download/evidence_drive.zip")
def download_evidence():
    if "user" not in session:
        return redirect(url_for("login"))

    if not session.get("restricted_seen"):
        abort(403)

    return send_from_directory(
        EVIDENCE_DIR,
        "evidence_drive.zip",
        as_attachment=True,
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    init_db()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
    )