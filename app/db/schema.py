from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

# ENUMS
class Degree(str, Enum):
    Bacharelado = "Bacharelado"
    Mestrado = "Mestrado"
    Doutorado = "Doutorado"
    Tecnologo = "Tecnologo"

class Shift(str, Enum):
    Matutino = "Matutino"
    Vespertino = "Vespertino"
    Noturno = "Noturno"
    Integral = "Integral"

class CategoryInst(str, Enum):
    Privada = 'Privada'
    Publica = 'Pública'
    PrivadaSemFins = 'Privada Sem Fins Lucrativos'

# SCHEMAS
class InstitutionBase(BaseModel):
    name: str
    acronym: str
    categoryInst: CategoryInst
    score_IGC: Optional[int] = 0
    score_CI: Optional[int] = 0
    score_CIEAD: Optional[int] = 0
    description: Optional[str] = None
    site: Optional[str] = None
    uf: Optional[str] = None

class InstitutionCreate(InstitutionBase):
    pass

class Institution(InstitutionBase):
    id: int
    campuses: List['Campus'] = []

    class Config:
        orm_mode = True

class CampusBase(BaseModel):
    name: str
    city: Optional[str] = None
    institution_id: int

class CampusCreate(CampusBase):
    pass

class Campus(CampusBase):
    id: int
    courses: List['Course'] = []

    class Config:
        orm_mode = True

class CourseBase(BaseModel):
    title: str
    code_from_institution: Optional[str] = None
    campus_id: int
    description: Optional[str] = None
    vacancies_semester_1: Optional[int] = None
    vacancies_semester_2: Optional[int] = None
    degree: Degree
    shift: Shift
    price: Optional[float] = 0.0

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int
    examScores: List['ExamScore'] = []
    enemScores: List['EnemScore'] = []
    categories: List['Category'] = []

    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    title: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    courses: List[Course] = []

    class Config:
        orm_mode = True

class ExamBase(BaseModel):
    name: str
    org: Optional[str] = None
    site: Optional[str] = None

class ExamCreate(ExamBase):
    pass

class Exam(ExamBase):
    id: int
    examScores: List['ExamScore'] = []
    institutions: List[Institution] = []

    class Config:
        orm_mode = True

class ExamScoreBase(BaseModel):
    year: int
    course: int
    bestScore: float
    lowestScore: float
    allScores: Optional[dict] = None
    exam: int

class ExamScoreCreate(ExamScoreBase):
    pass

class ExamScore(ExamScoreBase):
    id: int

    class Config:
        orm_mode = True

class EnemScoreBase(BaseModel):
    year: int
    course: int
    bestScore: float
    lowestScore: float
    allScores: Optional[dict] = None

class EnemScoreCreate(EnemScoreBase):
    pass

class EnemScore(EnemScoreBase):
    id: int

    class Config:
        orm_mode = True
