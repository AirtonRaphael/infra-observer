from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from models import Host
from schema import HostBase, HostSchema, HostCreateSchema
from utils import validate_url
from config.database import get_session
from custom_queue import get_queue, RabbitMQ

router = APIRouter()


@router.post('/', response_model=HostSchema)
async def add_host(new_host: HostCreateSchema, session: Session = Depends(get_session), queue: RabbitMQ = Depends(get_queue)):
    host = get_host_op(session, label=new_host.label)
    if host:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Host already exists.")

    url = validate_url(new_host.url)
    host = Host(label=new_host.label, url=url)

    session.add(host)
    session.commit()
    session.refresh(host)

    queue.publish("host.add", new_host.model_dump_json())

    return host


@router.get('/', response_model=List[HostSchema])
async def list_hosts(session: Session = Depends(get_session)):
    return session.query(Host).all()


@router.get('/{host_id}', response_model=HostSchema)
async def get_host(host_id: int, session: Session = Depends(get_session)):
    host = get_host_op(session, host_id=host_id)
    if not host:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, details="Host not founded.")

    return host


@router.put('/{host_id}', response_model=HostSchema)
async def update_host(host_id: int, new_host: HostBase, session: Session = Depends(get_session)):
    host = get_host_op(session, host_id=host_id)
    if not host:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, details="Host not founded.")

    host.label = new_host.label
    host.url = validate_url(new_host.url)

    session.commit()
    session.refresh(host)

    return host


@router.delete('/{host_id}')
async def delete_host(host_id: int, session: Session = Depends(get_session)):
    session.query(Host).filter_by(idhost=host_id).delete()
    session.commit()

    return


def get_host_op(session: Session, host_id: int = 0, label: str = '') -> Host:
    if host_id:
        return session.query(Host).filter_by(idhost=host_id).first()
    if label:
        return session.query(Host).filter_by(label=label).first()

