from fastapi import APIRouter, Depends
from ..dependencies import get_db
from sqlalchemy.orm import Session
from ..db import models, schema

router = APIRouter(
    prefix="/institutions",
    tags=["institutions"],
)

@router.get("/getAllInstitutions")
async def get_all_institutions(db: Session = Depends(get_db)):
    return db.query(models.Institution).all()

@router.get("/getInstitutionById/{id}")
async def get_institution_by_id(id):
    return

@router.get("/getInstitutionByName/{name}")
async def get_institution_by_name(name):
    return

@router.get("/getInstitutionByState/{state}")
async def get_institution_by_state(state):
    return

