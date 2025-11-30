from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    
    notes: List["Note"] = Relationship(back_populates="user")
    scores: List["QuizScore"] = Relationship(back_populates="user")
    history: List["ChatHistory"] = Relationship(back_populates="user")
    topics: List["UserTopic"] = Relationship(back_populates="user")

class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    folder: str = Field(default="General")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="notes")

class QuizScore(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    topic: str
    score: int
    total_questions: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="scores")

class ChatHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    query: str
    response: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="history")

class UserTopic(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    topic: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="topics")
