"""Run once to add sample students:  python seed.py"""
from app.database import Base, engine
from app import model  # noqa: F401
from app.seed import seed_if_empty

Base.metadata.create_all(bind=engine)
added = seed_if_empty()
print(f"Added {added} sample students." if added else "Table already has students, nothing added.")
