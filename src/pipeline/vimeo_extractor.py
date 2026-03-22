"""
Vimeo Audio/Transcript Extractor - Conference Video Processing
Extracts audio (MP3) or subtitles from Vimeo videos using browser cookie authentication
"""

import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import yt_dlp


class VimeoTranscriptExtractor:
    """Extracts audio or transcript segments from Vimeo videos."""

    def __init__(self, browser: str = "chrome"):
        """
        Initialize the extractor with yt-dlp options.

        Args:
            browser: Browser to extract cookies from ('chrome', 'firefox', 'edge', 'safari')
        """
        self.browser = browser
        self.ydl_opts = {
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitleslangs": ["en"],
            "skip_download": True,
            "quiet": True,
            "no_warnings": True,
            "cookiesfrombrowser": (browser,),  # Use browser cookies for authentication
        }

    def download_audio(self, url: str, output_dir: str = ".") -> str:
        """
        Download audio from Vimeo video as MP3.

        Args:
            url: Vimeo video URL
            output_dir: Directory to save the MP3 file

        Returns:
            Path to the downloaded MP3 file
        """
        video_id = self.extract_video_id(url)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Configure yt-dlp for audio download
        audio_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "outtmpl": str(output_path / f"vimeo_{video_id}.%(ext)s"),
            "quiet": False,
            "no_warnings": False,
            "cookiesfrombrowser": (self.browser,),
        }

        with yt_dlp.YoutubeDL(audio_opts) as ydl:
            try:
                print("🎵 Downloading audio from Vimeo video...")
                ydl.download([url])

                # Return the MP3 file path
                mp3_file = output_path / f"vimeo_{video_id}.mp3"
                if mp3_file.exists():
                    return str(mp3_file)
                else:
                    raise Exception(f"MP3 file not found at expected location: {mp3_file}")

            except Exception as e:
                raise Exception(f"Failed to download audio: {str(e)}") from e

    def extract_video_id(self, url: str) -> str:
        """
        Extract video ID from Vimeo URL.

        Examples:
            https://vimeo.com/1133050369 -> 1133050369
            https://vimeo.com/1133050369?fl=pl&fe=vl -> 1133050369
            https://player.vimeo.com/video/1133050369 -> 1133050369
        """
        parsed_url = urlparse(url)

        # Standard vimeo.com URLs
        if "vimeo.com" in parsed_url.hostname:
            # Remove query parameters and extract the ID
            path = parsed_url.path.strip("/")

            # Handle player.vimeo.com/video/ID format
            if "video/" in path:
                video_id = path.split("video/")[-1].split("/")[0]
            else:
                # Standard vimeo.com/ID format
                video_id = path.split("/")[0]

            # Remove any non-numeric characters
            video_id = re.sub(r"[^\d]", "", video_id)

            if video_id:
                return video_id

        raise ValueError(f"Could not extract video ID from URL: {url}")

    def extract_video_metadata(self, url: str) -> dict:
        """Extract basic video metadata from Vimeo."""
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)

                # Parse the published date
                upload_date_str = info.get("upload_date", "")
                if upload_date_str:
                    try:
                        published_date = datetime.strptime(upload_date_str, "%Y%m%d")
                    except ValueError:
                        published_date = datetime.now()
                else:
                    published_date = datetime.now()

                return {
                    "id": info.get("id", self.extract_video_id(url)),
                    "url": url,
                    "title": info.get("title", ""),
                    "channel_name": info.get("uploader", ""),
                    "channel_id": info.get("uploader_id", ""),
                    "published_date": published_date.isoformat(),
                    "duration_seconds": info.get("duration", 0),
                    "view_count": info.get("view_count", 0),
                    "like_count": info.get("like_count"),
                    "description": info.get("description", ""),
                    "thumbnail_url": info.get("thumbnail", ""),
                }
            except Exception as e:
                raise Exception(f"Failed to extract metadata: {str(e)}") from e

    def extract_raw_segments(self, url: str) -> list[dict]:
        """Extract raw VTT segments with absolutely no processing."""
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)

                # Try automatic captions first, fall back to manual subtitles
                subtitles = info.get("automatic_captions", {}).get("en", [])
                if not subtitles:
                    subtitles = info.get("subtitles", {}).get("en", [])

                if not subtitles:
                    raise Exception(
                        "No English subtitles available. "
                        "This video may not have captions, or may require authentication."
                    )

                # Find the best subtitle format (prefer vtt)
                subtitle_info = None
                for sub in subtitles:
                    if sub.get("ext") == "vtt":
                        subtitle_info = sub
                        break
                if not subtitle_info:
                    subtitle_info = subtitles[0]  # Take the first available

                # Download subtitle content
                subtitle_url = subtitle_info["url"]
                subtitle_content = ydl.urlopen(subtitle_url).read().decode("utf-8")

                return self._parse_raw_vtt(subtitle_content)

            except Exception as e:
                raise Exception(f"Failed to extract transcript: {str(e)}") from e

    def _parse_raw_vtt(self, vtt_content: str) -> list[dict]:
        """Parse VTT content into raw segments with ZERO processing."""
        raw_segments = []
        lines = vtt_content.split("\n")

        i = 0
        segment_index = 0

        while i < len(lines):
            line = lines[i].strip()

            # Look for timestamp lines (format: 00:00:00.000 --> 00:00:03.000)
            if "-->" in line:
                timestamp_match = re.match(
                    r"(\d{2}):(\d{2}):(\d{2})\.(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})\.(\d{3})",
                    line,
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
                    while i < len(lines) and "-->" not in lines[i]:
                        text_line = lines[i].strip()
                        if text_line and not text_line.startswith("WEBVTT"):
                            # Keep HTML tags and everything - NO processing
                            text_lines.append(text_line)
                        i += 1

                    # Create raw segment - NO filtering, NO merging
                    raw_segment = {
                        "segment_index": segment_index,
                        "start_time": start_time,
                        "end_time": end_time,
                        "duration": end_time - start_time,
                        "text_lines": text_lines,  # Keep as separate lines
                        "raw_text": (
                            " ".join(text_lines) if text_lines else ""
                        ),  # Also joined version
                        "timestamp_line": line,  # Keep original timestamp line
                    }

                    raw_segments.append(raw_segment)
                    segment_index += 1

                    continue

            i += 1

        return raw_segments

    def extract_and_save_raw(self, url: str) -> str:
        """Extract raw transcript and save to JSON file."""
        print(f"🎬 Extracting raw transcript from Vimeo: {url}")
        print(f"🔐 Using {self.browser.title()} browser cookies for authentication")

        # Extract metadata
        try:
            metadata = self.extract_video_metadata(url)
            print(f"✅ Video: {metadata['title']}")
            print(f"✅ Channel: {metadata['channel_name']}")
            print(f"✅ Duration: {metadata['duration_seconds']} seconds")
        except Exception as e:
            print(f"⚠️  Metadata extraction warning: {e}")
            # Use fallback metadata
            video_id = self.extract_video_id(url)
            metadata = {
                "id": video_id,
                "url": url,
                "title": "Unknown",
                "channel_name": "Unknown",
                "published_date": datetime.now().isoformat(),
                "duration_seconds": 0,
            }

        # Extract raw segments
        try:
            raw_segments = self.extract_raw_segments(url)
            print(f"✅ Extracted {len(raw_segments)} raw segments")
        except Exception as e:
            raise Exception(
                f"Failed to extract transcript: {str(e)}\n\n"
                f"💡 Troubleshooting tips:\n"
                f"   1. Make sure you're logged into Vimeo in {self.browser.title()}\n"
                f"   2. Try opening the video in {self.browser.title()} first\n"
                f"   3. Check if the video has captions enabled\n"
                f"   4. Try a different browser (--browser firefox/chrome/edge)"
            ) from e

        # Create output data
        output_data = {
            "extraction_timestamp": datetime.now().isoformat(),
            "metadata": metadata,
            "raw_segments": raw_segments,
            "total_segments": len(raw_segments),
            "source_platform": "vimeo",
        }

        # Save to file
        output_file = f"raw_segments_vimeo_{metadata['id']}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2)

        print(f"✅ Raw segments saved to: {output_file}")

        # Show sample segments
        print("\n📋 Sample Raw Segments (first 3):")
        for i, segment in enumerate(raw_segments[:3]):
            print(f"\n{i+1}. Index: {segment['segment_index']}")
            print(f"   Time: {segment['start_time']:.3f}s → {segment['end_time']:.3f}s")
            print(f"   Text: {segment['raw_text'][:100]}...")

        return output_file


def main():
    """Extract raw transcript from Vimeo video."""
    import sys

    # Parse command line arguments
    browser = "chrome"  # default
    url = None

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--browser" and i + 1 < len(args):
            browser = args[i + 1]
            i += 2
        else:
            url = args[i]
            i += 1

    if not url:
        print("Usage: python vimeo_extractor.py <vimeo_url> [--browser chrome|firefox|edge|safari]")
        print("\nExample:")
        print("  python vimeo_extractor.py https://vimeo.com/1133050369")
        print("  python vimeo_extractor.py https://vimeo.com/1133050369 --browser firefox")
        return

    extractor = VimeoTranscriptExtractor(browser=browser)

    try:
        output_file = extractor.extract_and_save_raw(url)
        print(f"\n🎉 Raw extraction complete! Check {output_file} for full structure.")
        print("\n💡 Next steps:")
        print("   1. Use the existing text reconstruction tools to create readable transcript")
        print("   2. Manually enhance the transcript in Claude Code")
        print("   3. Use manual_chunker.py to create high-quality chunks")
        print("   4. Store in MCP KB with store_in_mcp_kb.py")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
