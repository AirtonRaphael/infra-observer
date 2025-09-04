from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models import Host
from schema import HostSchema, HostCreateSchema
from utils import validate_url, endpoint_exists
from config.database import get_session

router = APIRouter()


@router.post('/hosts', response_model=HostSchema)
def add_host(new_host: HostCreateSchema, session: Session = Depends(get_session)):
    url = validate_url(new_host.url)
    if not url:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="URL is not in a valid format.")

    if not endpoint_exists(url):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to connect to the URL.")

    host = Host(label=new_host.label, url=new_host.url)

    session.add(host)
    session.commit()
    session.refresh(host)

    return host
