from app.database.database import Base
from sqlalchemy import Column,Integer,ForeignKey

class Like(Base):
    __tablename__ = "Likes"
    
    post_id = Column(Integer,ForeignKey("Posts.id",ondelete="CASCADE"),primary_key=True)
    user_id = Column(Integer,ForeignKey("Users.id",ondelete="CASCADE"),primary_key=True)