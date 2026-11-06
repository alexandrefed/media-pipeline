from faster_whisper import WhisperModel
from pathlib import Path
import json

base = Path('workspace/videos/20261007--dee80886--sprint--matt-ganzak--october-7-live-call')
base.mkdir(parents=True, exist_ok=True)
audio = Path('workspace/audio/sprint-dee80886-oct7-full-16k.mp3')
metadata = {
    'video_id': 'dee80886-bd00-4089-a69e-48dbe9151a07',
    'platform': 'sprint',
    'title': 'October 7: Live Call - AI Native Services, Software & The Community',
    'channel': 'Matt Ganzak / The Sprint',
    'url': 'https://sprint.mattganzak.com/live/dee80886-bd00-4089-a69e-48dbe9151a07',
    'upload_date': '20261007',
    'duration_seconds': 5744,
    'content_type': 'live-call-recording',
    'transcription_source': 'Cloudflare Stream audio downloaded from authenticated Sprint page; transcribed with faster-whisper large-v3-turbo',
}
(base / 'metadata.json').write_text(json.dumps(metadata, indent=2))

print('loading model', flush=True)
try:
    model = WhisperModel('large-v3-turbo', device='cuda', compute_type='int8')
except Exception as e:
    print(f'cuda failed, using cpu: {e}', flush=True)
    model = WhisperModel('large-v3-turbo', device='cpu', compute_type='int8')

print(f'transcribing {audio}', flush=True)
segments, info = model.transcribe(
    str(audio),
    vad_filter=True,
    vad_parameters=dict(min_silence_duration_ms=500),
    beam_size=5,
)
raw = []
txt = []

def fmt(sec):
    sec = int(sec)
    h = sec // 3600
    m = (sec % 3600) // 60
    s = sec % 60
    return f'{h:02d}:{m:02d}:{s:02d}'

for seg in segments:
    text = seg.text.strip()
    line = f'[{fmt(seg.start)} - {fmt(seg.end)}] {text}'
    raw.append({'start': seg.start, 'end': seg.end, 'text': text})
    txt.append(line)
    if len(raw) % 100 == 0:
        print(f'segments {len(raw)} at {fmt(seg.end)}', flush=True)

transcript = '\n'.join(txt).strip() + '\n'
(base / 'transcript_segments.json').write_text(json.dumps(raw, indent=2, ensure_ascii=False))
(base / 'transcript_raw.txt').write_text(transcript)
(base / 'transcript_enhanced.txt').write_text(transcript)
print(f'done {base.resolve()} segments {len(raw)} language {info.language} duration {info.duration}', flush=True)
