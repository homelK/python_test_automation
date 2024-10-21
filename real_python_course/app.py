from flask import render_template # Remove: import Flask
import config
from models import Person

app = config.connex_app
app.add_api("swagger.yml")

@app.route("/")
def home():
    people = Person.query.all()
    return render_template("home.html", people=people)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)