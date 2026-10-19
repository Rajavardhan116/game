"""
Database Models for Unique Character Quest
------------------------------------------
Defines schemas for SQLite persistence using SQLAlchemy ORM.
Stores player stats, match results, achievements, and room history.
"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Player(Base):
    __tablename__ = "players"

    id = Column(String(50), primary_key=True)
    player_name = Column(String(50), unique=True, nullable=False, index=True)
    total_games = Column(Integer, default=0)
    total_score = Column(Integer, default=0)
    highest_score = Column(Integer, default=0)
    total_correct = Column(Integer, default=0)
    total_questions = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    matches = relationship("MatchResult", back_populates="player", cascade="all, delete-orphan")
    achievements = relationship("PlayerAchievement", back_populates="player", cascade="all, delete-orphan")


class MatchResult(Base):
    __tablename__ = "match_results"

    id = Column(String(50), primary_key=True)
    player_name = Column(String(50), ForeignKey("players.player_name"), nullable=False, index=True)
    mode = Column(String(20), nullable=False)  # classic, speed, puzzle, multiplayer
    difficulty = Column(String(20), nullable=False)
    score = Column(Integer, nullable=False)
    accuracy = Column(Float, default=0.0)
    questions_answered = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    levels_completed = Column(Integer, default=0)
    match_result = Column(String(20), nullable=False)  # WON, LOST, COMPLETED
    duration_seconds = Column(Float, default=0.0)
    completed_at = Column(DateTime, default=datetime.utcnow, index=True)

    player = relationship("Player", back_populates="matches")


class Achievement(Base):
    __tablename__ = "achievements"

    code = Column(String(50), primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    icon = Column(String(50), default="🏆")
    points = Column(Integer, default=50)

    unlocked_by = relationship("PlayerAchievement", back_populates="achievement")


class PlayerAchievement(Base):
    __tablename__ = "player_achievements"

    id = Column(String(50), primary_key=True)
    player_name = Column(String(50), ForeignKey("players.player_name"), nullable=False)
    achievement_code = Column(String(50), ForeignKey("achievements.code"), nullable=False)
    unlocked_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("player_name", "achievement_code", name="uq_player_achievement"),
    )

    player = relationship("Player", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="unlocked_by")
