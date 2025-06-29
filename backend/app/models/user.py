from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class User(Base):
    """用户数据库模型"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # 关系
    docker_images = relationship("DockerImage", back_populates="created_by")
    datasets = relationship("Dataset", back_populates="created_by")
    models = relationship("Model", back_populates="created_by")
    training_jobs = relationship("TrainingJob", back_populates="created_by")
    applications = relationship("Application", back_populates="created_by")
    evaluation_tasks = relationship("EvaluationTask", back_populates="created_by")
    
    def __repr__(self):
        return f"<User {self.username}>" 