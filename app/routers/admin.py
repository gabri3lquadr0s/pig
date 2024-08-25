from fastapi import APIRouter
from dataGathering.sisumec import main
from ..dependencies import get_db
from sqlalchemy.orm import Session
from ..db import models, schema
import asyncio

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

#THIS PLACE HERE WILL BE THE LINKS FOR EXECUTING THE QUERYS FOR INFO
#STILL HAVE TO MAKE THE SCRAPPERS

@router.get("/sisumec")
async def sisumec():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())