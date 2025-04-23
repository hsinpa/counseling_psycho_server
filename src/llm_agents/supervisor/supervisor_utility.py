from src.model.supervisor_model import TranscriptSegment


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