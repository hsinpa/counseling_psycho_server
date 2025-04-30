import re
import uuid

from src.model.supervisor_model import TranscriptSegment

def text_to_transcript_segment(txt_content: str) -> list[TranscriptSegment]:
    segments = [seg.strip() for seg in txt_content.split("\n\n") if seg.strip()]

    processed_segments: list[TranscriptSegment] = []
    for segment in segments:
        # Simplified regex - just look for t or p at start, ignore number details
        match = re.match(r"^([tp])\d*:\s*(.*)", segment, re.IGNORECASE | re.DOTALL)

        if match:
            segment_type = match.group(1).lower()  # Normalize to uppercase
            content = match.group(2).strip()

            speaker_id = 'spk_0' if segment_type.startswith('t') else 'spk_1'

            processed_segments.append(
                TranscriptSegment(id=str(uuid.uuid4()), speaker=speaker_id, start_time='', end_time='', text=content)
            )
        else:
            processed_segments.append(
                TranscriptSegment(
                    id=str(uuid.uuid4()),
                    speaker='spk_0',
                    start_time="",
                    end_time="",
                    text=segment,
                )
            )
    return processed_segments


def transcript_segment_to_text(segments: list[TranscriptSegment]):
    full_text = ''
    t_count = 0
    p_count = 0

    for index, segment in enumerate(segments):
        label = ''
        if segment.speaker == 'spk_0':
            t_count += 1

            if t_count == 1:
                label = f'Therapist (T-{t_count})'
            else:
                label = f"T-{t_count}"
        else:
            p_count += 1

            if p_count == 1:
                label = f'Patient (P-{p_count})'
            else:
                label = f'P-{p_count}'

        full_text += f'{label}: {segment.text}\n'

    return full_text
