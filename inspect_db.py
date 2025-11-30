from sqlmodel import Session, select, create_engine
from backend.models import User, UserTopic, QuizScore

sqlite_file_name = "studybuddy.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)

with Session(engine) as session:
    print("--- Users ---")
    users = session.exec(select(User)).all()
    for u in users:
        print(f"ID: {u.id}, Username: {u.username}")

    print("\n--- User Topics ---")
    topics = session.exec(select(UserTopic)).all()
    for t in topics:
        print(f"User: {t.user_id}, Topic: {t.topic}, Time: {t.timestamp}")

    print("\n--- Quiz Scores ---")
    scores = session.exec(select(QuizScore)).all()
    for s in scores:
        print(f"User: {s.user_id}, Topic: {s.topic}, Score: {s.score}, Time: {s.timestamp}")
