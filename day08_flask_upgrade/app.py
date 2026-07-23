from functools import wraps
from pathlib import Path

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

from services.data_service import (
    get_available_categories,
    load_category_api_data,
    load_dashboard_data,
    load_metric_api_data,
)
from services.qa_service import answer_question


BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
app.config["SECRET_KEY"] = "day07-classroom-demo-key"


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "username" not in session:
            flash("请先登录后再访问数据看板。", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view


def json_error(message: str, status_code: int = 400):
    """生成统一的 JSON 错误响应。"""
    return jsonify({"ok": False, "error": message}), status_code


@app.route("/")
def index():
    return redirect(url_for("dashboard") if "username" in session else url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if username == "student" and password == "day07":
            session["username"] = username
            flash("登录成功，欢迎进入电商用户分析系统。", "success")
            return redirect(url_for("dashboard"))
        flash("账号或密码错误。演示账号：student / day07", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("你已安全退出。", "success")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    category = request.args.get("category", "全部").strip() or "全部"
    dashboard_data = load_dashboard_data(BASE_DIR, category)
    return render_template(
        "dashboard.html",
        username=session["username"],
        selected_category=category,
        **dashboard_data,
    )


@app.route("/assistant")
@login_required
def assistant():
    return render_template("assistant.html", username=session["username"])


@app.route("/api/ask", methods=["POST"])
@login_required
def ask():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return json_error("请求体必须是 JSON 对象。")

    question = str(payload.get("question", "")).strip()
    if not question:
        return json_error("请输入一个与项目数据有关的问题。")
    return jsonify({"ok": True, "answer": answer_question(BASE_DIR, question)})


@app.route("/health")
def health():
    """用于确认服务是否存活，不需要登录。"""
    return jsonify({"ok": True, "service": "day08-flask-upgrade"})


@app.route("/api/metrics")
@login_required
def metrics_api():
    """返回数据看板中的四张指标卡。"""
    return jsonify({"ok": True, "metrics": load_metric_api_data(BASE_DIR)})


@app.route("/api/categories")
@login_required
def categories_api():
    """按 category 查询参数返回品类分析记录。"""
    category = request.args.get("category", "全部").strip() or "全部"
    available_categories = get_available_categories(BASE_DIR)
    if category not in available_categories:
        return json_error(
            f"未知品类：{category}。可选值为：{'、'.join(available_categories)}。"
        )

    rows = load_category_api_data(BASE_DIR, category)
    return jsonify({"ok": True, "category": category, "rows": rows})


@app.errorhandler(400)
def bad_request(error):
    message = getattr(error, "description", None) or "请求格式不正确。"
    return json_error(str(message), 400)


@app.errorhandler(404)
def page_not_found(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=False, port=5000)
