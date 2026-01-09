from app.database.database import Base
from sqlalchemy import Column,Integer,TIMESTAMP,String,ForeignKey,text

class Posts(Base):
    __tablename__ = "Posts"
    id = Column(Integer,primary_key=True,autoincrement=True)
    caption = Column(String,nullable=False)
    owner_id = Column(Integer,ForeignKey(column="Users.id",ondelete="CASCADE"),nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default="now()")
    
    