from flask import Flask, render_template, redirect

app = Flask(__name__)

# ✅ Add this block to handle the home route "/"
@app.route("/")
def home():
    return redirect("/profile")

# ✅ Your main profile route
@app.route("/profile")
def profile():
    user = {
        "name": "Your Name",
        "email": "your@email.com"
    }
    return render_template("profile.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)
