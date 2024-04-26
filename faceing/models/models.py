from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


# Определение модели пользователя
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    is_admin = Column(Boolean, default=False)


# Определение модели администратора
class Administrator(Base):
    __tablename__ = 'administrators'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)



# Определение модели категории новостей
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


# Определение модели новости
class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    author = Column(String, nullable=False)
    publish_date = Column(DateTime, nullable=False, default=func.now())

    categories = relationship("Category", secondary="news_categories")


# Определение связующей таблицы между новостями и категориями
class NewsCategory(Base):
    __tablename__ = 'news_categories'

    news_id = Column(Integer, ForeignKey('news.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)


