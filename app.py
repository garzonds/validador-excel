<<<<<<< HEAD
from flask import Flask, render_template, request, send_file, jsonify, session, redirect, url_for
=======
from flask import Flask, render_template, request, send_file, jsonify
>>>>>>> 647152c126eca07e960fd3d375e21fe038a8e19c
from pathlib import Path
import json, uuid, os

from modules.loader    import load_excel
from modules.validator import apply_rules
from modules.reporter  import generate_report

app = Flask(__name__)
<<<<<<< HEAD
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
app.secret_key = os.environ.get("SECRET_KEY", "1234asdf")
=======
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB max
>>>>>>> 647152c126eca07e960fd3d375e21fe038a8e19c

BASE       = Path(__file__).parent
UPLOAD_DIR = BASE / "uploads"
OUTPUT_DIR = BASE / "output"
RULES_PATH = BASE / "config" / "rules.json"

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

<<<<<<< HEAD
APP_PASSWORD = os.environ.get("APP_PASSWORD","123")


def autenticado():
    return session.get("auth") is True


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form.get("password") == APP_PASSWORD:
            session["auth"] = True
            return redirect(url_for("index"))
        error = "Contraseña incorrecta."
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
def index():
    if not autenticado():
        return redirect(url_for("login"))
=======

@app.route("/")
def index():
>>>>>>> 647152c126eca07e960fd3d375e21fe038a8e19c
    return render_template("index.html")


@app.route("/procesar", methods=["POST"])
def procesar():
<<<<<<< HEAD
    if not autenticado():
        return jsonify({"error": "No autorizado."}), 401

=======
>>>>>>> 647152c126eca07e960fd3d375e21fe038a8e19c
    if "archivo" not in request.files:
        return jsonify({"error": "No se recibió ningún archivo."}), 400

    archivo = request.files["archivo"]
    if not archivo.filename.endswith((".xlsx", ".xls")):
        return jsonify({"error": "Solo se aceptan archivos Excel (.xlsx o .xls)."}), 400

    uid         = uuid.uuid4().hex
    input_path  = UPLOAD_DIR / f"{uid}_input.xlsx"
    output_path = OUTPUT_DIR / f"{uid}_reporte.xlsx"

    archivo.save(str(input_path))

    try:
        with open(RULES_PATH, encoding="utf-8") as f:
            config = json.load(f)
        out_col = config["output_column"]

        df        = load_excel(str(input_path))
        df_result = apply_rules(df, str(RULES_PATH))

<<<<<<< HEAD
=======
        # Resumen para mostrar en la UI
>>>>>>> 647152c126eca07e960fd3d375e21fe038a8e19c
        resumen = df_result[out_col].value_counts().to_dict()
        total   = len(df_result)

        generate_report(df_result, out_col, str(output_path))

<<<<<<< HEAD
        return jsonify({"ok": True, "uid": uid, "total": total, "resumen": resumen, "columna": out_col})
=======
        return jsonify({
            "ok":       True,
            "uid":      uid,
            "total":    total,
            "resumen":  resumen,
            "columna":  out_col,
        })
>>>>>>> 647152c126eca07e960fd3d375e21fe038a8e19c
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if input_path.exists():
            os.remove(input_path)


@app.route("/descargar/<uid>")
def descargar(uid):
<<<<<<< HEAD
    if not autenticado():
        return redirect(url_for("login"))
=======
>>>>>>> 647152c126eca07e960fd3d375e21fe038a8e19c
    output_path = OUTPUT_DIR / f"{uid}_reporte.xlsx"
    if not output_path.exists():
        return "Archivo no encontrado.", 404
    return send_file(str(output_path), as_attachment=True, download_name="reporte_validado.xlsx")


if __name__ == "__main__":
<<<<<<< HEAD
=======
    import os
>>>>>>> 647152c126eca07e960fd3d375e21fe038a8e19c
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Abriendo en http://localhost:{port}")
    app.run(debug=False, host="0.0.0.0", port=port)
