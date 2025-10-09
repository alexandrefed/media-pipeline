"""
Raw YouTube Transcript Extractor - Zero Processing
Extracts raw VTT segments exactly as YouTube provides them
"""

import json
import re
from typing import List, Dict
from urllib.parse import parse_qs, urlparse
from datetime import datetime

import yt_dlp


class RawTranscriptExtractor:
    """Extracts raw transcript segments with absolutely no processing."""
    
    def __init__(self):
        """Initialize the extractor with yt-dlp options."""
        self.ydl_opts = {
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en'],
            'skip_download': True,
            'quiet': True,
            'no_warnings': True,
        }
    
    def extract_video_id(self, url: str) -> str:
        """Extract video ID from YouTube URL."""
        parsed_url = urlparse(url)
        
        if parsed_url.hostname in ['youtu.be']:
            return parsed_url.path[1:]
        elif parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
            if parsed_url.path == '/watch':
                return parse_qs(parsed_url.query)['v'][0]
            elif parsed_url.path.startswith('/embed/'):
                return parsed_url.path.split('/')[2]
        
        raise ValueError(f"Could not extract video ID from URL: {url}")
    
    def extract_video_metadata(self, url: str) -> Dict:
        """Extract basic video metadata."""
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                
                # Parse the published date
                upload_date_str = info.get('upload_date', '')
                if upload_date_str:
                    published_date = datetime.strptime(upload_date_str, '%Y%m%d')
                else:
                    published_date = datetime.now()
                
                return {
                    'id': info['id'],
                    'url': url,
                    'title': info.get('title', ''),
                    'channel_name': info.get('uploader', ''),
                    'channel_id': info.get('channel_id', ''),
                    'published_date': published_date.isoformat(),
                    'duration_seconds': info.get('duration', 0),
                    'view_count': info.get('view_count', 0),
                    'like_count': info.get('like_count'),
                    'description': info.get('description', ''),
                    'thumbnail_url': info.get('thumbnail', '')
                }
            except Exception as e:
                raise Exception(f"Failed to extract metadata: {str(e)}")
    
    def extract_raw_segments(self, url: str) -> List[Dict]:
        """Extract raw VTT segments with absolutely no processing."""
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                
                # Get automatic subtitles first, fall back to manual
                subtitles = info.get('automatic_captions', {}).get('en', [])
                if not subtitles:
                    subtitles = info.get('subtitles', {}).get('en', [])
                
                if not subtitles:
                    raise Exception("No English subtitles available")
                
                # Find the best subtitle format (prefer vtt)
                subtitle_info = None
                for sub in subtitles:
                    if sub.get('ext') == 'vtt':
                        subtitle_info = sub
                        break
                if not subtitle_info:
                    subtitle_info = subtitles[0]  # Take the first available
                
                # Download subtitle content
                subtitle_url = subtitle_info['url']
                subtitle_content = ydl.urlopen(subtitle_url).read().decode('utf-8')
                
                return self._parse_raw_vtt(subtitle_content)
                
            except Exception as e:
                raise Exception(f"Failed to extract transcript: {str(e)}")
    
    def _parse_raw_vtt(self, vtt_content: str) -> List[Dict]:
        """Parse VTT content into raw segments with ZERO processing."""
        raw_segments = []
        lines = vtt_content.split('\n')
        
        i = 0
        segment_index = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for timestamp lines (format: 00:00:00.000 --> 00:00:03.000)
            if '-->' in line:
                timestamp_match = re.match(
                    r'(\d{2}):(\d{2}):(\d{2})\.(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})\.(\d{3})',
                    line
                )
                
                if timestamp_match:
                    # Parse start time
                    start_h, start_m, start_s, start_ms = map(int, timestamp_match.groups()[:4])
                    start_time = start_h * 3600 + start_m * 60 + start_s + start_ms / 1000
                    
                    # Parse end time
                    end_h, end_m, end_s, end_ms = map(int, timestamp_match.groups()[4:])
                    end_time = end_h * 3600 + end_m * 60 + end_s + end_ms / 1000
                    
                    # Collect ALL text lines until next timestamp or end
                    text_lines = []
                    i += 1
                    while i < len(lines) and '-->' not in lines[i]:
                        text_line = lines[i].strip()
                        if text_line and not text_line.startswith('WEBVTT'):
                            # Keep HTML tags and everything - NO processing
                            text_lines.append(text_line)
                        i += 1
                    
                    # Create raw segment - NO filtering, NO merging
                    raw_segment = {
                        'segment_index': segment_index,
                        'start_time': start_time,
                        'end_time': end_time,
                        'duration': end_time - start_time,
                        'text_lines': text_lines,  # Keep as separate lines
                        'raw_text': ' '.join(text_lines) if text_lines else '',  # Also joined version
                        'timestamp_line': line  # Keep original timestamp line
                    }
                    
                    raw_segments.append(raw_segment)
                    segment_index += 1
                    
                    continue
            
            i += 1
        
        return raw_segments
    
    def extract_and_save_raw(self, url: str) -> str:
        """Extract raw transcript and save to JSON file."""
        print(f"Extracting raw transcript from: {url}")
        
        # Extract metadata
        metadata = self.extract_video_metadata(url)
        print(f"✅ Video: {metadata['title']}")
        print(f"✅ Channel: {metadata['channel_name']}")
        print(f"✅ Duration: {metadata['duration_seconds']} seconds")
        
        # Extract raw segments
        raw_segments = self.extract_raw_segments(url)
        print(f"✅ Extracted {len(raw_segments)} raw segments")
        
        # Create output data
        output_data = {
            'extraction_timestamp': datetime.now().isoformat(),
            'metadata': metadata,
            'raw_segments': raw_segments,
            'total_segments': len(raw_segments)
        }
        
        # Save to file
        output_file = f"raw_segments_{metadata['id']}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"✅ Raw segments saved to: {output_file}")
        
        # Show sample segments
        print(f"\n📋 Sample Raw Segments (first 5):")
        for i, segment in enumerate(raw_segments[:5]):
            print(f"\n{i+1}. Index: {segment['segment_index']}")
            print(f"   Time: {segment['start_time']:.3f}s → {segment['end_time']:.3f}s (duration: {segment['duration']:.3f}s)")
            print(f"   Text Lines: {segment['text_lines']}")
            print(f"   Raw Text: {segment['raw_text']}")
            print(f"   Timestamp: {segment['timestamp_line']}")
        
        return output_file


def main():
    """Extract raw transcript from YouTube video."""
    extractor = RawTranscriptExtractor()
    
    # Get URL from user
    url = input("Enter YouTube video URL: ").strip()
    if not url:
        print("No URL provided, exiting.")
        return
    
    try:
        output_file = extractor.extract_and_save_raw(url)
        print(f"\n🎉 Raw extraction complete! Check {output_file} for full structure.")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()