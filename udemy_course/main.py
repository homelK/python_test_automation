import random
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            #Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random",  methods=["GET"])
def get_random_cafe():
    all_cafes = Cafe.query.all()
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe=random_cafe.to_dict())

@app.route("/all",  methods=["GET"])
def get_all_cafe():
    all_cafes = Cafe.query.all()
    list_of_cafes = [cafe.to_dict() for cafe in all_cafes]
    return jsonify(cafes=list_of_cafes)

@app.route("/search",  methods=["GET"])
def get_one_cafe():
    cafe_to_find = request.args.get("loc")
    requested_cafe = Cafe.query.filter(Cafe.location == cafe_to_find).all()
    if requested_cafe is not None:
        return jsonify(cafes=[cafe.to_dict() for cafe in requested_cafe])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have cafe at the location"}), 404


# HTTP POST - Create Record
@app.route("/add",  methods=["POST"])
def add_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully add the new cafe"})

# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<cafe_id>",  methods=["PATCH"])
def update_cafe_price(cafe_id):
    new_coffee_price = request.args.get("new_price")
    existing_cafe = Cafe.query.filter(Cafe.id == cafe_id).one_or_none()

    if existing_cafe is not None:
        existing_cafe.coffee_price = new_coffee_price
        db.session.commit()
        return jsonify(success="Successfully updated the price"), 200
    else:
        return jsonify(error={"Not found": "Sorry a cafe with that id was not found in the database"}), 404

# HTTP DELETE - Delete Record
@app.route("/report-closed/<cafe_id>",  methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")

    if api_key != "TopSecretAPIKey":
        return jsonify(error="Sorry, that's not allowed. Make sure you have the correct api-key"), 403

    cafe_to_delete = Cafe.query.filter(Cafe.id == cafe_id).one_or_none()

    if cafe_to_delete is None:
        return jsonify(error={"Not found": "Sorry a cafe with that id was not found in the database"}), 404
    else:
        db.session.delete(cafe_to_delete)
        db.session.commit()
        return jsonify(cafe=f"Cafe with id {cafe_id} was successfully deleted"), 200


if __name__ == '__main__':
    app.run(debug=True)
