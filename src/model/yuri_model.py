from pydantic import BaseModel, Field


class YuriLoginType(BaseModel):
    password: str = Field(..., example='Password')
    email: str = Field(..., example='Email')
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "password": "itriTest",
                    "email": 'itriTest@gmail.com',
                }
            ]
        }
    }


class YuriCreateTrainRecordType(BaseModel):
    caregiverId: str = Field(..., example='User id')
    title: str = Field(..., example='Name of test')
    completeness: int = Field(..., example='Completeness')
    errorPrompt: list[str] = Field(..., example='Error during training')
    time: str = Field(..., example='Time')
    remark: str = Field('', example='Leave it empty')

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "caregiverId": "2024-07-29T11:50:35.479Z-17222538354797020755e-3691-49d3-b5bd-4248ee5b30bb",
                    "title": '左翻',
                    "completeness": 100,
                    "errorPrompt": ['Small error, not big deal'],
                    "time": '2025/01/01',
                    "remark": '',
                }
            ]
        }
    }