<<<<<<< HEAD
from flask import Flask, render_template, request
from predict import greedy_translate

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    user_input = ""
    translation = ""

    if request.method == "POST":
        user_input = request.form.get("text", "").strip()

        if user_input:
            try:
                translation = greedy_translate(user_input)
            except Exception as e:
                translation = f"Error: {str(e)}"

    return render_template(
        "index.html",
        user_input=user_input,
        translation=translation
    )

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
=======
from flask import Flask, render_template, request
from predict import greedy_translate

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    user_input = ""
    translation = ""

    if request.method == "POST":
        user_input = request.form.get("text", "").strip()

        if user_input:
            try:
                translation = greedy_translate(user_input)
            except Exception as e:
                translation = f"Error: {str(e)}"

    return render_template(
        "index.html",
        user_input=user_input,
        translation=translation
    )

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
>>>>>>> ca4968bb2bb755ffc586f63ec736f7bd04bb0055
    app.run(host="0.0.0.0", port=port, debug=False)