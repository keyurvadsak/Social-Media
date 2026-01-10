from app.database.database import Base
from sqlalchemy import Column,Integer,TIMESTAMP,String,ForeignKey,LargeBinary

class Posts(Base):
    __tablename__ = "Posts"
    id = Column(Integer,primary_key=True,autoincrement=True)
    image = Column(LargeBinary,nullable=False)
    text = Column(String,nullable=False)
    caption = Column(String,nullable=False)
    owner_id = Column(Integer,ForeignKey(column="Users.id",ondelete="CASCADE"),nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default="now()")
    
    