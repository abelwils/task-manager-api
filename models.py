from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime


# 👤 USER TABLE
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user")  # user / admin

    # Relationship (1 user → many tasks)
    tasks = relationship("Task", back_populates="owner")


# 📌 TASK TABLE
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    # 🟡 Priority (low / medium / high)
    priority = Column(String, default="medium")

    # 📅 Due date
    due_date = Column(DateTime, nullable=True)

    # ✅ Completed status
    completed = Column(Boolean, default=False)

    # 🕒 Created time
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # 🔗 Foreign key (User → Task)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Relationship
    owner = relationship("User", back_populates="tasks")