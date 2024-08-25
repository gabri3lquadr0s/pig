from fastapi import FastAPI
from .routers import admin
from .routers import courses
from .routers import exams
from .routers import institutions
from .routers import campus

app = FastAPI()

app.include_router(admin.router)
app.include_router(courses.router)
app.include_router(exams.router)
app.include_router(institutions.router)
app.include_router(campus.router)

