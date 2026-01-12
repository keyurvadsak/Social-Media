from app.database.database import Base
from sqlalchemy import Column,Integer,ForeignKey,String



class Comment(Base):
    __tablename__ = "Comments"
    id = Column(Integer,autoincrement=True,primary_key=True)
    post_id = Column(Integer,ForeignKey("Posts.id",ondelete="CASCADE"),nullable=False)
    user_id = Column(Integer,ForeignKey("Users.id",ondelete="CASCADE"),nullable=False)
    Comment_Text = Column(String,nullable=False)
    post_owner_id = Column(Integer,nullable=False)