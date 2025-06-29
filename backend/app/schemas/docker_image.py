from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator


# 共享属性
class DockerImageBase(BaseModel):
    """Docker镜像基础模式"""
    name: str = Field(..., description="镜像名称", min_length=2, max_length=255)
    tag: str = Field(..., description="镜像标签", min_length=1, max_length=100)
    registry: str = Field(..., description="镜像仓库地址", max_length=255)
    size: float = Field(..., description="镜像大小(MB)", gt=0)
    description: Optional[str] = Field(None, description="镜像描述")
    
    @validator('name')
    def name_must_be_valid(cls, v):
        if '/' in v and not v.startswith('localhost:') and not any(x in v for x in ['.', ':']):
            raise ValueError('镜像名称格式不正确')
        return v
    
    @validator('tag')
    def tag_must_be_valid(cls, v):
        if ':' in v:
            raise ValueError('标签不应包含冒号')
        return v


# 创建请求
class DockerImageCreate(DockerImageBase):
    """创建Docker镜像的请求模式"""
    pass


# 更新请求
class DockerImageUpdate(BaseModel):
    """更新Docker镜像的请求模式"""
    name: Optional[str] = Field(None, description="镜像名称", min_length=2, max_length=255)
    tag: Optional[str] = Field(None, description="镜像标签", min_length=1, max_length=100)
    registry: Optional[str] = Field(None, description="镜像仓库地址", max_length=255)
    size: Optional[float] = Field(None, description="镜像大小(MB)", gt=0)
    description: Optional[str] = Field(None, description="镜像描述")
    
    @validator('name')
    def name_must_be_valid(cls, v):
        if v is None:
            return v
        if '/' in v and not v.startswith('localhost:') and not any(x in v for x in ['.', ':']):
            raise ValueError('镜像名称格式不正确')
        return v
    
    @validator('tag')
    def tag_must_be_valid(cls, v):
        if v is None:
            return v
        if ':' in v:
            raise ValueError('标签不应包含冒号')
        return v


# 数据库模型
class DockerImageInDBBase(DockerImageBase):
    """数据库中的Docker镜像模式"""
    id: int
    created_by_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


# API响应
class DockerImage(DockerImageInDBBase):
    """API响应的Docker镜像模式"""
    created_by_username: Optional[str] = None 