from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router=APIRouter(prefix="/demo-auth", tags=["Auth"])
security= HTTPBasic()

@router.get("/basic-auth/")
def demo_basic_auth(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    return {
        "message":"hii",
        "username": credentials.username,
        "password": credentials.password,
    }