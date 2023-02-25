from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, Column, String, Integer, Float, Date, ForeignKey, BOOLEAN
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ReportUploadModel(db.Model):
    __tablename__ = 'reportuploads'
    id = db.Column(db.Integer, primary_key=True)
    pdf_number = db.Column(db.String(64), unique=True, index=True)
    pdf_name = db.Column(db.String(64))
    pdf_origin_name = db.Column(db.String(64))

class UserModel(db.Model):
    __tablename__ = 'temp_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String(100), nullable=False)
    pwd = Column(String(100), nullable=False)
    name = Column(String(100), default='用户')

    def to_json(self):
        dict = self.__dict__

        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict