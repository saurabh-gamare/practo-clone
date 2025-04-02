from fastapi import FastAPI, status, HTTPException

from database import engine, db_dependency, Base
from routers import auth, profile, appointments


app = FastAPI()
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(appointments.router)


""" 
Use this when not using albemic migrations.
Without migrations this line will create tables but this is not recommended on production
"""
# Base.metadata.create_all(bind=engine)

