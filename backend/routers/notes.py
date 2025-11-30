from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from backend.database import get_session
from backend.models import Note, User
from backend.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
)

class NoteCreate(BaseModel):
    title: str
    content: str
    folder: str = "General"

@router.post("/", response_model=Note)
def create_note(note_data: NoteCreate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    note = Note(
        title=note_data.title,
        content=note_data.content,
        folder=note_data.folder,
        user_id=current_user.id
    )
    session.add(note)
    session.commit()
    session.refresh(note)
    return note

@router.get("/", response_model=List[Note])
def get_notes(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    statement = select(Note).where(Note.user_id == current_user.id).order_by(Note.created_at.desc())
    results = session.exec(statement)
    return results.all()

@router.get("/folders", response_model=List[str])
def get_folders(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    statement = select(Note.folder).where(Note.user_id == current_user.id).distinct()
    results = session.exec(statement)
    folders = list(set([r for r in results.all()]))
    if "General" not in folders:
        folders.append("General")
    return sorted(folders)

@router.delete("/{note_id}")
def delete_note(note_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this note")
    
    session.delete(note)
    session.commit()
    return {"ok": True}
