import json
import os
from enum import Enum
import boto3
from fastapi import UploadFile, File, Form
import urllib.request
from src.model.supervisor_model import TranscribeProgressEnum, TranscribeStatus, TranscriptSegment, TranscriptData


class BotoClientEnum(str, Enum):
    transcribe='transcribe'
    s3 = 's3'

class BotoHelper:
    def __init__(self):
        pass

    def upload_to_s3(self, file: UploadFile, file_byte: bytes, bucket:str, key: str):
        s3_client = self._create_client(BotoClientEnum.s3)

        # Upload file to S3
        s3_client.put_object(
            Body=file_byte,
            Bucket=bucket,
            Key=key,
            ContentType=file.content_type
        )

        return f"https://{bucket}.s3.amazonaws.com/{key}"


    def request_transcribe(self, session_id: str, langcode: str, bucket:str, key: str):
        boto_client = self._create_client(BotoClientEnum.transcribe)

        # Create a unique job name
        job_name = f"{session_id}"

        # Construct S3 URI
        s3_uri = f"s3://{bucket}/{key}"
        print(f"Transcribing {s3_uri}")

        response = boto_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': s3_uri},
            MediaFormat='ogg',
            LanguageCode=langcode,
            Settings={
                'ShowSpeakerLabels': True,
                'MaxSpeakerLabels': 2
            }
        )
        return response

    def retrieve_transcribe(self, transcript_uri: str) -> TranscriptData:
        speakers_segments: list[TranscriptSegment] = []

        with urllib.request.urlopen(transcript_uri) as response:
            transcript_json = json.loads(response.read())

        # Extract transcript text
        transcript_text = transcript_json['results']['transcripts'][0]['transcript']

        # Extract speaker labels if available
        if 'speaker_labels' in transcript_json['results']:
            segments = transcript_json['results']['speaker_labels']['segments']

            for segment in segments:
                speaker = segment['speaker_label']
                start_time = segment['start_time']
                end_time = segment['end_time']

                # Find items with same time stamps to get the text
                segment_text = ""
                for item in transcript_json['results'].get('items', []):
                    if 'start_time' in item and 'end_time' in item:
                        if (float(item['start_time']) >= float(start_time) and
                                float(item['end_time']) <= float(end_time)):
                            segment_text += item['alternatives'][0]['content'] + " "

                speakers_segments.append(
                    TranscriptSegment(
                        speaker=speaker,
                        start_time=start_time,
                        end_time=end_time,
                        text=segment_text.strip()
                    )
                )

        return TranscriptData(full_text=transcript_text, segments=speakers_segments)

    def get_transcribe_status(self, job_name: str) -> tuple[TranscribeProgressEnum, str | None]:
        """
        job_name should be session_id
        """
        boto_client = self._create_client(BotoClientEnum.transcribe)

        status = boto_client.get_transcription_job(TranscriptionJobName=job_name)

        print('status', status)
        job_status = status['TranscriptionJob']['TranscriptionJobStatus']

        if job_status == 'COMPLETED':
            transcript_uri: str = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
            return  TranscribeProgressEnum.complete, transcript_uri
        elif job_status == 'FAILED':
            return TranscribeProgressEnum.fail, None

        return TranscribeProgressEnum.in_progress, None

    @staticmethod
    def _create_client(client_name: BotoClientEnum):
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        region = os.getenv("AWS_DEFAULT_REGION")

        return boto3.client(client_name,
                                  aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=secret_key,
                                  region_name=region)