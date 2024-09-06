import asyncio
import json

import requests


class MQTT_Record_Upload:
    def login(email: str, password: str):
        headers = {'Content-Type': 'application/json'}
        r = requests.post('http://34.127.119.34:3000/UserDataBase/Login', headers=headers,
                          json={'email': email, 'password': password})

        return r.json()

    def __init__(self, id: str, hospitalId: str, user_name: str, token: str):
        self._id = id
        self._hospital_id = hospitalId
        self._user_name = user_name
        self._token = token

    def bulk_upload(self):
        # Load JSON
        with open("./MQTT_Record.json", encoding='utf-8') as f:
            mqtt_record_json = json.load(f)

            for record in mqtt_record_json:
                self.upload(record)

    def upload(self, single_record: dict):
        data_object = {
            'caregiverId': self._id,
            'title': single_record['title'],
            'completeness': 100 if single_record['is_complete'] else 0,
            'errorPrompt': single_record['errorPrompt'],
            'time': single_record['time'],
            'remark': single_record['remark'],
        }
        headers = {'Content-Type': 'application/json', 'Authorization': self._token}
        r = requests.post(f'http://34.127.119.34:3000/TrainingRecordsDatabase/{self._hospital_id}', headers=headers,
                          json=data_object)

        print(r.json())

        return r.json()


if __name__ == '__main__':
    login_result = MQTT_Record_Upload.login(email='itriTest@gmail.com', password='itriTest')
    print(login_result)

    token = login_result['token']
    id = login_result['data']['id']
    hospitalId = login_result['data']['hospitalId']
    name = login_result['data']['name']

    recorder = MQTT_Record_Upload(id=id, hospitalId=hospitalId, user_name=name, token=token)
    recorder.bulk_upload()
