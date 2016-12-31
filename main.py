from flask import Flask, render_template, request, json

import dice

app = Flask(__name__)


@app.context_processor
def inject_debug():
    return { "debug": app.debug }


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return json.jsonify(dice.execute(request.data.decode("utf-8")))

    return render_template("index.html", code="")

if __name__ == "__main__":
    app.run()
    print(app.debug)
