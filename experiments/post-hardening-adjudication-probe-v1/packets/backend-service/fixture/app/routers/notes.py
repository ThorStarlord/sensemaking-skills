from fastapi import APIRouter, HTTPException
from ..models import Note
from ..db import get_db

router = APIRouter(prefix="/notes")

@router.post("/")
def create(note: Note):
    db = get_db()
    cur = db.execute("INSERT INTO notes (body) VALUES (?)", (note.body,))
    db.commit()
    return {"id": cur.lastrowid}

@router.get("/{note_id}")
def read(note_id: int):
    db = get_db()
    row = db.execute("SELECT body FROM notes WHERE id = ?", (note_id,)).fetchone()
    if row is None:
        raise HTTPException(404)
    return {"body": row[0]}
