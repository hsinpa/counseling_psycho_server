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


@router.get("/audio_transcript")
async def get_record():
    audio_path = './assets/audio/en_conversation_02.mp3'
    definition_data = {
        "locales": ["en-US"],
        "diarization": {
            "maxSpeakers": 2,
            "enabled": True
        }
    }
    print(json.dumps(definition_data))
    with open(audio_path, "rb") as audio_file:
        form_data = {
            'audio':  ("audio_file.mp3", audio_file, "audio/mpeg"),
            'definition': (None, json.dumps(definition_data), "application/json")
        }
        headers = {'Ocp-Apim-Subscription-Key': ''}
        url = f'https://eastus.api.cognitive.microsoft.com/speechtotext/transcriptions:transcribe?api-version=2024-11-15'
        r = requests.post(url, headers=headers, files=form_data)
        return r.json()

