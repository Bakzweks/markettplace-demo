from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "secret"

products = []
users = []

@app.route("/")
def index():
    return render_template("index.html", products=products)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        users.append((username, password, role))
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        for u in users:
            if u[0] == username and u[1] == password:
                session["user"] = u
                return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/add", methods=["GET", "POST"])
def add_product():
    if "user" not in session or session["user"][2] != "seller":
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form["title"]
        price = request.form["price"]
        description = request.form["description"]
        products.append({"title": title, "price": price, "description": description})
        return redirect(url_for("index"))
    return render_template("add_product.html")

if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
