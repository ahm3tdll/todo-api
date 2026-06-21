from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base

class Todo(Base):
    __tablename__ = "todos"  # PostgreSQL'deki tablo adı

    id = Column(Integer, primary_key=True, index=True)  # otomatik artan id
    title = Column(String(200))  # maksimum 200 karakter
    description = Column(String(500), nullable=True)  # boş olabilir
    completed = Column(Boolean, default=False)  # başlangıçta tamamlanmamış
    user_id = Column(Integer, ForeignKey("users.id"))