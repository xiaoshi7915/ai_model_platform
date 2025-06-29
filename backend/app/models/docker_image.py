from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class DockerImage(Base):
    """Docker镜像数据库模型"""
    
    __tablename__ = "docker_images"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True, comment="镜像名称")
    tag = Column(String(100), nullable=False, index=True, comment="镜像标签")
    registry = Column(String(255), nullable=False, comment="镜像仓库地址")
    size = Column(Float, nullable=False, comment="镜像大小(MB)")
    description = Column(Text, nullable=True, comment="镜像描述")
    
    # 创建者信息
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_by = relationship("User", back_populates="docker_images")
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # 关联的训练任务
    training_jobs = relationship("TrainingJob", back_populates="docker_image")
    
    def __repr__(self):
        return f"<DockerImage {self.name}:{self.tag}>" 