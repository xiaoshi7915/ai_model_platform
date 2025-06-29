from typing import List, Optional, Dict, Any, Union

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.docker_image import DockerImage
from app.models.training_job import TrainingJob
from app.schemas.docker_image import DockerImageCreate, DockerImageUpdate


def get_docker_image(db: Session, id: int) -> Optional[DockerImage]:
    """
    通过ID获取Docker镜像
    """
    return db.query(DockerImage).filter(DockerImage.id == id).first()


def get_docker_image_by_name_and_tag(
    db: Session, name: str, tag: str
) -> Optional[DockerImage]:
    """
    通过名称和标签获取Docker镜像
    """
    return db.query(DockerImage).filter(
        DockerImage.name == name,
        DockerImage.tag == tag
    ).first()


def get_docker_images(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    name: Optional[str] = None,
    tag: Optional[str] = None,
    registry: Optional[str] = None
) -> List[DockerImage]:
    """
    获取Docker镜像列表，支持过滤
    """
    query = db.query(DockerImage)
    
    # 应用过滤条件
    if name:
        query = query.filter(DockerImage.name.ilike(f"%{name}%"))
    if tag:
        query = query.filter(DockerImage.tag.ilike(f"%{tag}%"))
    if registry:
        query = query.filter(DockerImage.registry.ilike(f"%{registry}%"))
    
    # 排序和分页
    return query.order_by(DockerImage.created_at.desc()).offset(skip).limit(limit).all()


def create_docker_image(
    db: Session, docker_image_in: DockerImageCreate, created_by_id: int
) -> DockerImage:
    """
    创建新的Docker镜像
    """
    db_obj = DockerImage(
        name=docker_image_in.name,
        tag=docker_image_in.tag,
        registry=docker_image_in.registry,
        size=docker_image_in.size,
        description=docker_image_in.description,
        created_by_id=created_by_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_docker_image(
    db: Session, db_obj: DockerImage, obj_in: Union[DockerImageUpdate, Dict[str, Any]]
) -> DockerImage:
    """
    更新Docker镜像
    """
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    
    for field in update_data:
        if field in update_data and hasattr(db_obj, field):
            setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_docker_image(db: Session, id: int) -> None:
    """
    删除Docker镜像
    """
    db_obj = db.query(DockerImage).get(id)
    if db_obj:
        db.delete(db_obj)
        db.commit()


def is_docker_image_in_use(db: Session, docker_image_id: int) -> bool:
    """
    检查Docker镜像是否正在被训练任务使用
    """
    # 检查是否有正在运行的训练任务使用该镜像
    return db.query(TrainingJob).filter(
        and_(
            TrainingJob.docker_image_id == docker_image_id,
            TrainingJob.status.in_(["pending", "running", "paused"])
        )
    ).count() > 0 