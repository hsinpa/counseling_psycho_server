import os

import boto3
import time
import json

from dotenv import load_dotenv


def transcribe_mp3(
        bucket_name,
        file_key,
        aws_access_key_id,
        aws_secret_access_key,
        region_name,
        language_code='en-US',
        max_speakers=2
):
    """
    Transcribe a single MP3 file with speaker diarization

    Parameters:
    - bucket_name: S3 bucket name
    - file_key: Path to MP3 file in the bucket
    - language_code: Language code (default 'en-US')
    - max_speakers: Maximum number of speakers to identify

    Returns:
    - Dictionary with transcript and job details
    """
    # Create Transcribe client
    transcribe = boto3.client('transcribe',
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key,
                              region_name=region_name
                              )

    # Create a unique job name
    job_name = f"transcribe-{int(time.time())}"

    # Construct S3 URI
    s3_uri = f"s3://{bucket_name}/{file_key}"
    print(f"Transcribing {s3_uri}")

    # Start transcription job with speaker diarization
    response = transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': s3_uri},
        MediaFormat='mp3',
        LanguageCode=language_code,
        Settings={
            'ShowSpeakerLabels': True,
            'MaxSpeakerLabels': max_speakers
        }
    )

    print(f"Started transcription job: {job_name}")

    # Wait for completion
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        job_status = status['TranscriptionJob']['TranscriptionJobStatus']

        if job_status == 'COMPLETED':
            print("Transcription completed successfully!")
            break
        elif job_status == 'FAILED':
            reason = status['TranscriptionJob'].get('FailureReason', 'Unknown')
            print(f"Transcription failed: {reason}")
            return None

        print(f"Status: {job_status} - waiting 30 seconds...")
        time.sleep(30)

    # Get the transcript URL
    transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']

    # Download the transcript
    import urllib.request
    with urllib.request.urlopen(transcript_uri) as response:
        transcript_json = json.loads(response.read())

    # Extract transcript text
    transcript_text = transcript_json['results']['transcripts'][0]['transcript']

    # Extract speaker labels if available
    speakers_segments = []
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

            speakers_segments.append({
                'speaker': speaker,
                'start_time': start_time,
                'end_time': end_time,
                'text': segment_text.strip()
            })

    return {
        'transcript': transcript_text,
        'speaker_segments': speakers_segments,
        'job_name': job_name
    }


# Example usage
if __name__ == "__main__":
    load_dotenv()

    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_DEFAULT_REGION")

    # Configure these variables with your values
    BUCKET_NAME = "audio-disk"
    FILE_KEY = "english_test_audio.mp3"
    LANGUAGE_CODE = "en-US"  # Change to your language if needed zh-TW en-US
    MAX_SPEAKERS = 2  # Change based on your audio file

    result = transcribe_mp3(
        bucket_name=BUCKET_NAME,
        file_key=FILE_KEY,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=secret_key,
        region_name=region,
        language_code=LANGUAGE_CODE,
        max_speakers=MAX_SPEAKERS
    )

    if result:
        print("\nSUMMARY TRANSCRIPT:")
        print("------------------")
        print(result['transcript'][:500] + "...")

        print("\nSPEAKER SEGMENTS:")
        print("------------------")
        for i, segment in enumerate(result['speaker_segments'][:5]):
            print(f"{segment['speaker']}: {segment['text']}")

        if len(result['speaker_segments']) > 5:
            print("... (more segments available)")

        # Save full results to files
        with open('transcript.txt', 'w') as f:
            f.write(result['transcript'])

        with open('transcript_with_speakers.json', 'w') as f:
            json.dump(result, f, indent=2)

        print("\nFull transcript saved to 'transcript.txt'")
        print("Full results with speaker segmentation saved to 'transcript_with_speakers.json'")
