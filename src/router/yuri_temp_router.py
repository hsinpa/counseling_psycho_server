import json

import requests
from fastapi import APIRouter

from src.model.yuri_model import YuriLoginType, YuriCreateTrainRecordType, YuriGetTrainRecordType

router = APIRouter(prefix="/yuri", tags=["yuri"])


@router.post("/login")
async def login(login_type: YuriLoginType):
    headers = {'Content-Type': 'application/json'}
    r = requests.post('http://34.127.119.34:3000/UserDataBase/Login', headers=headers,
                      json=login_type.model_dump())

    return r.json()


@router.post("/upload_record/{org_id}/{token}")
async def upload_record(org_id: str, token: str, create_type: YuriCreateTrainRecordType):
    headers = {'Content-Type': 'application/json', 'Authorization': token}
    r = requests.post(f'http://34.127.119.34:3000/TrainingRecordsDatabase/{org_id}', headers=headers,
                      json=create_type.model_dump())

    return r.json()


@router.post("/get_record")
async def get_record(p_input: YuriGetTrainRecordType):
    headers = {'Authorization': p_input.token}
    url = f'http://34.127.119.34:3000/TrainingRecordsDatabase/{p_input.hospitalId}/searchByCaregiverId?caregiverId={p_input.caregiverId}'
    r = requests.get(url, headers=headers)
    return r.json()
