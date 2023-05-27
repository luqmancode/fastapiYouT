from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

from .database import Base


class Post(Base):
    __tablename__ = "alchemy_posts"

    id = Column(Integer, primary_key = True, index = True, autoincrement = True)
    user_id = Column(Integer, ForeignKey("alchemy_users.id", ondelete = "CASCADE"), nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    is_published = Column(Boolean, server_default = 'TRUE')
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))

    owner_info = relationship("User")

class User(Base):
    __tablename__ = "alchemy_users"
    id = Column(Integer, primary_key = True, index = True, autoincrement = True)
    email = Column(String, unique = True, nullable = False)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))


class Vote(Base):
    __tablename__ = "alchemy_votes"
    post_id = Column(Integer, ForeignKey("alchemy_posts.id", ondelete = "CASCADE"), primary_key = True)
    user_id = Column(Integer, ForeignKey("alchemy_users.id", ondelete = "CASCADE"), primary_key = True)
