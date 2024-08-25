from sqlalchemy import Column, ForeignKey, Integer, String, JSON, Enum, Float, Table, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from .db import Base
import enum


metadata = Base.metadata

#ENUMS
class Degree(enum.Enum):
    Bacharelado = "Bacharelado"
    Mestrado = "Mestrado"
    Doutorado = "Doutorado"
    Tecnologo = "Tecnologo"

class Shift(enum.Enum):
    Matutino = "Matutino"
    Vespertino = "Vespertino"
    Noturno = "Noturno"
    Integral = "Integral"

class CategoryInst(enum.Enum):
    Privada = 'Privada'
    Publica = 'Pública'
    PrivadaSemFins = 'Privada Sem Fins Lucrativos'

#TABLES
class Institution(Base):
    __tablename__ = 'institutions'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    acronym = Column(String, unique=True)
    categoryInst = Column(Enum(CategoryInst))
    score_IGC = Column(Integer, default=0)
    score_CI = Column(Integer, default=0)
    score_CIEAD = Column(Integer, default=0)
    description = Column(String)
    site = Column(String)
    uf = Column(String)

    campuses = relationship('Campus', backref='institution', cascade="all, delete-orphan")

class Campus(Base):
    __tablename__ = 'campus'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    city = Column(String)
    institution_id = Column(Integer, ForeignKey('institutions.id'))

    courses = relationship('Course', backref='campus', cascade="all, delete-orphan")

class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    code_from_institution = Column(String)
    campus_id = Column(Integer, ForeignKey('campus.id'))
    description = Column(String)
    vacancies_semester_1 = Column(Integer)
    vacancies_semester_2 = Column(Integer)
    degree = Column(Enum(Degree))
    shift = Column(Enum(Shift))
    price = Column(Float, default=0.0)

    examScores = relationship('ExamScore', backref='course_exams')
    enemScores = relationship('EnemScore', backref='course_enem')
    categories = relationship('Category', secondary='category_course', backref='course')

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)

class Exam(Base):
    __tablename__ = 'exam'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    org = Column(String)
    site = Column(String)

    examScores = relationship('ExamScore', backref='score_exam')
    institutions = relationship('Institution', secondary='institution_exam', backref='exams')

class ExamScore(Base):
    __tablename__ = 'examScore'

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    course = Column(Integer, ForeignKey('course.id'))
    bestScore = Column(Float)
    lowestScore = Column(Float)
    allScores = Column(JSON)
    exam = Column(Integer, ForeignKey('exam.id'))

class EnemScore(Base):
    __tablename__ = 'enemScore'

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    course = Column(Integer, ForeignKey('course.id'))
    bestScore = Column(Float)
    lowestScore = Column(Float)
    allScores = Column(JSON)

#RELATION TABLES

category_course = Table(
    'category_course',
    Base.metadata,
    Column('category_id', Integer, ForeignKey('category.id')),
    Column('course_id', Integer, ForeignKey('course.id'))
)

institution_exam = Table(
    'institution_exam',
    Base.metadata,
    Column('institution_id', Integer, ForeignKey('institutions.id')),
    Column('exam_id', Integer, ForeignKey('exam.id'))
)

