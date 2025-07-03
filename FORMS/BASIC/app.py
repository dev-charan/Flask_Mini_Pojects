from flask import request, Flask, render_template


app = Flask(__name__)
user=[]
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        username=request.form.get("name")
        password=request.form.get("password")
        output = request.form.to_dict()
        user.append(output)
        return "user updated"

@app.route("/display",methods=["GET"])
def getuser():
    return user

if __name__ == "__main__":
    app.run(debug=True)