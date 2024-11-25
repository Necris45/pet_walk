from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session

router = APIRouter()


@router.get('/ping')
async def pong():
    return {'ping': 'pong!'}
