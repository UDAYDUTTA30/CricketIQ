from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import os

DATABASE_URL = "sqlite:///./data/database/cricketiq.db"

# Ensure database directory exists
os.makedirs(os.path.dirname(DATABASE_URL.replace("sqlite:///", "")), exist_ok=True)

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Match(Base):
    __tablename__ = "matches"

    id = Column(String, primary_key=True, index=True) # Usually the cricsheet filename/match ID
    city = Column(String, index=True, nullable=True)
    date = Column(String, index=True) # Store as string YYYY-MM-DD for simplicity
    match_type = Column(String)
    team1 = Column(String, index=True)
    team2 = Column(String, index=True)
    toss_winner = Column(String)
    toss_decision = Column(String)
    winner = Column(String, index=True, nullable=True)
    win_by_runs = Column(Integer, nullable=True)
    win_by_wickets = Column(Integer, nullable=True)
    player_of_match = Column(String, nullable=True)
    venue = Column(String, index=True)

    deliveries = relationship("Delivery", back_populates="match", cascade="all, delete-orphan")


class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(String, ForeignKey("matches.id"), index=True)
    inning = Column(Integer, index=True)
    over = Column(Integer)
    ball = Column(Integer)
    batter = Column(String, index=True)
    bowler = Column(String, index=True)
    non_striker = Column(String)
    runs_batter = Column(Integer)
    runs_extras = Column(Integer)
    runs_total = Column(Integer)
    player_dismissed = Column(String, nullable=True)
    dismissal_kind = Column(String, nullable=True)
    extras_type = Column(String, nullable=True) # e.g. wides, noballs, legbyes, byes

    match = relationship("Match", back_populates="deliveries")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
