from flask import Flask, render_template, request, json

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        code = request.data.decode("utf-8")
        return json.jsonify({
            "code": code
        })

    return render_template("index.html", code="")


if __name__ == "__main__":
    app.run()
