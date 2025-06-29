from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class TrainingJob(Base):
    """训练任务数据库模型"""
    
    __tablename__ = "training_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True, comment="任务名称")
    description = Column(Text, nullable=True, comment="任务描述")
    
    # 训练配置
    model_type = Column(String(100), nullable=False, comment="模型类型")
    hyperparameters = Column(JSON, nullable=True, comment="超参数")
    training_script = Column(Text, nullable=True, comment="训练脚本")
    
    # 资源配置
    gpu_count = Column(Integer, nullable=False, default=1, comment="GPU数量")
    cpu_count = Column(Integer, nullable=False, default=4, comment="CPU数量")
    memory = Column(Float, nullable=False, default=16.0, comment="内存大小(GB)")
    
    # 状态信息
    status = Column(String(50), nullable=False, default="pending", comment="任务状态")
    progress = Column(Float, nullable=False, default=0.0, comment="训练进度")
    error_message = Column(Text, nullable=True, comment="错误信息")
    
    # 关联的Docker镜像
    docker_image_id = Column(Integer, ForeignKey("docker_images.id"), nullable=False)
    docker_image = relationship("DockerImage", back_populates="training_jobs")
    
    # 关联的数据集
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    dataset = relationship("Dataset", back_populates="training_jobs")
    
    # 关联的模型（训练结果）
    model_id = Column(Integer, ForeignKey("models.id"), nullable=True)
    model = relationship("Model", back_populates="training_job")
    
    # 创建者信息
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_by = relationship("User", back_populates="training_jobs")
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=True, comment="开始时间")
    finished_at = Column(DateTime(timezone=True), nullable=True, comment="完成时间")
    
    def __repr__(self):
        return f"<TrainingJob {self.name}>" 