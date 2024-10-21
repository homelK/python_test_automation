from flask import abort, make_response, request
from config import db
from models import Person, Note, note_schema


def create():
    note = request.get_json()
    person_id = note.get("person_id")
    person = Person.query.get(person_id)

    if person:
       new_note = note_schema.load(note, session=db.session)
       person.notes.append(new_note)
       db.session.commit()
       return note_schema.dump(new_note), 201
    else:
        abort(
            404,
            f"Person not found for ID: {person_id}"
        )

def read_one(note_id):
    note = Note.query.filter(Note.id == note_id).one_or_none()

    if note is not None:
        return note_schema.dump(note)
    else:
        abort(404, f"Nolte with ID {note_id} not found")

def update(note_id):
    note = request.get_json()
    existing_note = Note.query.filter(Note.id == note_id).one_or_none()

    if existing_note:
        update_note = note_schema.load(note, session=db.session)
        existing_note.content = update_note.content
        db.session.merge(existing_note)
        db.session.commit()
        return note_schema.dump(existing_note), 201
    else:
        abort(404, f"Note with ID {note_id} not found")


def delete(note_id):
    existing_note = Note.query.filter(Note.id == note_id).one_or_none()

    if existing_note:
        db.session.delete(existing_note)
        db.session.commit()
        return make_response(f"Note with ID {note_id} successfully deleted", 204)
    else:
        abort(404, f"Note with ID {note_id} not found")

