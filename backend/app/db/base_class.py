from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """
    SQLAlchemy 模型的基类
    
    提供了表名自动生成和 id 主键
    """
    
    id: Any
    __name__: str
    
    # 根据类名自动生成表名
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() 