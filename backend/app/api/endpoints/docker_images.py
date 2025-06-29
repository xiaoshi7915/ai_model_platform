from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.crud import docker_images as crud
from app.models.user import User
from app.schemas.docker_image import DockerImage, DockerImageCreate, DockerImageUpdate

router = APIRouter()


@router.get("/", response_model=List[DockerImage])
def get_docker_images(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    name: Optional[str] = Query(None, description="按名称过滤"),
    tag: Optional[str] = Query(None, description="按标签过滤"),
    registry: Optional[str] = Query(None, description="按仓库过滤")
):
    """
    获取Docker镜像列表。
    可以通过名称、标签和仓库进行过滤。
    """
    return crud.get_docker_images(
        db=db, 
        skip=skip, 
        limit=limit, 
        name=name, 
        tag=tag, 
        registry=registry
    )


@router.post("/", response_model=DockerImage, status_code=status.HTTP_201_CREATED)
def create_docker_image(
    *,
    db: Session = Depends(get_db),
    docker_image_in: DockerImageCreate,
    current_user: User = Depends(get_current_user)
):
    """
    创建新的Docker镜像。
    """
    # 检查同名同标签的镜像是否已存在
    existing_image = crud.get_docker_image_by_name_and_tag(
        db=db, 
        name=docker_image_in.name, 
        tag=docker_image_in.tag
    )
    if existing_image:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"镜像 {docker_image_in.name}:{docker_image_in.tag} 已存在"
        )
    
    return crud.create_docker_image(
        db=db, 
        docker_image_in=docker_image_in, 
        created_by_id=current_user.id
    )


@router.get("/{docker_image_id}", response_model=DockerImage)
def get_docker_image(
    *,
    db: Session = Depends(get_db),
    docker_image_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    通过ID获取Docker镜像详情。
    """
    docker_image = crud.get_docker_image(db=db, id=docker_image_id)
    if not docker_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Docker镜像不存在"
        )
    return docker_image


@router.put("/{docker_image_id}", response_model=DockerImage)
def update_docker_image(
    *,
    db: Session = Depends(get_db),
    docker_image_id: int,
    docker_image_in: DockerImageUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    更新Docker镜像信息。
    """
    docker_image = crud.get_docker_image(db=db, id=docker_image_id)
    if not docker_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Docker镜像不存在"
        )
    
    # 如果更新了名称和标签，检查是否与其他镜像冲突
    if docker_image_in.name and docker_image_in.tag:
        existing_image = crud.get_docker_image_by_name_and_tag(
            db=db, 
            name=docker_image_in.name, 
            tag=docker_image_in.tag
        )
        if existing_image and existing_image.id != docker_image_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"镜像 {docker_image_in.name}:{docker_image_in.tag} 已存在"
            )
    
    return crud.update_docker_image(
        db=db, 
        db_obj=docker_image, 
        obj_in=docker_image_in
    )


@router.delete("/{docker_image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_docker_image(
    *,
    db: Session = Depends(get_db),
    docker_image_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    删除Docker镜像。
    """
    docker_image = crud.get_docker_image(db=db, id=docker_image_id)
    if not docker_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Docker镜像不存在"
        )
    
    # 检查是否有训练任务正在使用该镜像
    if crud.is_docker_image_in_use(db=db, docker_image_id=docker_image_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该Docker镜像正在被训练任务使用，无法删除"
        )
    
    crud.delete_docker_image(db=db, id=docker_image_id)
    return None 