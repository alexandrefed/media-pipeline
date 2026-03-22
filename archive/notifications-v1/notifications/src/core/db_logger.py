"""
Database Logger for AI Knowledge Base
Integrates local processing pipeline with n8n workflows and PostgreSQL database
"""

import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class VideoInsight:
    """Represents an extractable insight from a video"""
    text: str
    type: str = "concept"  # protocol, concept, technique, tip, warning, tool_usage, strategy
    context: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    timestamp_start: Optional[int] = None
    timestamp_end: Optional[int] = None
    quality_score: float = 0.7
    priority: str = "medium"  # low, medium, high, critical
    actionable: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        # Remove None values
        return {k: v for k, v in data.items() if v is not None}


@dataclass
class VideoMetadata:
    """Represents video metadata"""
    video_id: str
    title: str
    channel_name: str
    url: str
    channel_id: Optional[str] = None
    duration_seconds: Optional[int] = None
    pipeline_type: str = "ai_tools"  # ai_tools or sports
    tags: Optional[List[str]] = None
    total_chunks: int = 0
    insights: Optional[List[VideoInsight]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}

        # Convert insights to dict
        if self.insights:
            data['insights'] = [
                insight.to_dict() if isinstance(insight, VideoInsight) else insight
                for insight in self.insights
            ]

        return data


class KnowledgeBaseLogger:
    """
    Logger for AI Knowledge Base system
    Sends video insights to n8n workflows and tracks processing
    """

    def __init__(
        self,
        webhook_url: str = "https://n8n.vecia.fr/webhook/video-processed",
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize the logger

        Args:
            webhook_url: n8n webhook URL for video processing
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.webhook_url = webhook_url
        self.timeout = timeout
        self.verify_ssl = verify_ssl

    def store_video_insights(
        self,
        video_metadata: VideoMetadata,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Store video and insights in the knowledge base via n8n webhook

        Args:
            video_metadata: VideoMetadata object with video info and insights
            dry_run: If True, print payload without sending

        Returns:
            Response from n8n webhook or dry run result

        Example:
            >>> logger = KnowledgeBaseLogger()
            >>>
            >>> insights = [
            ...     VideoInsight(
            ...         text="Use the HTTP Request node to call external APIs",
            ...         type="tip",
            ...         category="n8n",
            ...         tags=["workflow", "http"],
            ...         quality_score=0.85,
            ...         priority="high"
            ...     )
            ... ]
            >>>
            >>> video = VideoMetadata(
            ...     video_id="ABC123",
            ...     title="n8n Tutorial",
            ...     channel_name="IndyDevDan",
            ...     url="https://youtube.com/watch?v=ABC123",
            ...     pipeline_type="ai_tools",
            ...     total_chunks=15,
            ...     insights=insights
            ... )
            >>>
            >>> result = logger.store_video_insights(video)
        """
        payload = video_metadata.to_dict()

        if dry_run:
            print("DRY RUN - Would send payload:")
            print(json.dumps(payload, indent=2))
            return {"dry_run": True, "payload": payload}

        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=self.timeout,
                verify=self.verify_ssl,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            return {
                "success": True,
                "status_code": response.status_code,
                "response": response.json() if response.content else {},
                "video_id": video_metadata.video_id
            }

        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "video_id": video_metadata.video_id
            }

    def load_from_analysis_json(
        self,
        analysis_file: Path,
        video_id: str,
        url: str
    ) -> VideoMetadata:
        """
        Load video metadata from analysis JSON file

        Args:
            analysis_file: Path to analysis JSON file
            video_id: YouTube video ID
            url: YouTube video URL

        Returns:
            VideoMetadata object

        Example:
            >>> logger = KnowledgeBaseLogger()
            >>> video = logger.load_from_analysis_json(
            ...     Path("workspace/analysis/ABC123_analysis.json"),
            ...     "ABC123",
            ...     "https://youtube.com/watch?v=ABC123"
            ... )
            >>> result = logger.store_video_insights(video)
        """
        with open(analysis_file, 'r') as f:
            data = json.load(f)

        # Extract basic metadata
        title = data.get('title', 'Unknown Title')
        channel = data.get('channel', 'Unknown Channel')
        pipeline_type = data.get('pipeline_type', 'ai_tools')

        # Extract insights
        insights = []
        insights_data = data.get('insights', [])

        for insight_data in insights_data:
            insight = VideoInsight(
                text=insight_data.get('text', ''),
                type=insight_data.get('type', 'concept'),
                context=insight_data.get('context'),
                category=insight_data.get('category'),
                tags=insight_data.get('tags', []),
                timestamp_start=insight_data.get('timestamp_start'),
                timestamp_end=insight_data.get('timestamp_end'),
                quality_score=insight_data.get('quality_score', 0.7),
                priority=insight_data.get('priority', 'medium'),
                actionable=insight_data.get('actionable', True)
            )
            insights.append(insight)

        # Create video metadata
        video = VideoMetadata(
            video_id=video_id,
            title=title,
            channel_name=channel,
            url=url,
            pipeline_type=pipeline_type,
            tags=data.get('tags', []),
            total_chunks=len(data.get('chunks', [])),
            insights=insights
        )

        return video


class DirectDatabaseLogger:
    """
    Direct database logger for cases where you want to bypass n8n
    Requires psycopg2 and direct database access
    """

    def __init__(
        self,
        connection_string: str = None,
        host: str = "vecia_aidb",
        port: int = 5433,
        database: str = "aidb",
        user: str = "ai_admin",
        password: str = None,
        schema: str = "ai_kb"
    ):
        """
        Initialize direct database connection

        Args:
            connection_string: Full PostgreSQL connection string
            host: Database host (default: vecia_aidb)
            port: Database port (default: 5433)
            database: Database name (default: aidb)
            user: Database user (default: ai_admin)
            password: Database password
            schema: Schema name (default: ai_kb)
        """
        try:
            import psycopg2
            from psycopg2.extras import Json
            self.psycopg2 = psycopg2
            self.Json = Json
        except ImportError:
            raise ImportError(
                "psycopg2 is required for direct database access. "
                "Install it with: uv add psycopg2-binary"
            )

        if connection_string:
            self.conn_string = connection_string
        else:
            if not password:
                raise ValueError("Password is required for database connection")
            self.conn_string = (
                f"postgresql://{user}:{password}@{host}:{port}/{database}"
            )

        self.schema = schema
        self.conn = None

    def connect(self):
        """Establish database connection"""
        if not self.conn or self.conn.closed:
            self.conn = self.psycopg2.connect(self.conn_string)
        return self.conn

    def close(self):
        """Close database connection"""
        if self.conn and not self.conn.closed:
            self.conn.close()

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

    def store_video(self, video: VideoMetadata) -> int:
        """
        Store video metadata directly in database

        Args:
            video: VideoMetadata object

        Returns:
            Number of rows affected

        Example:
            >>> with DirectDatabaseLogger(password="your_password") as db:
            ...     rows = db.store_video(video_metadata)
        """
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    INSERT INTO {self.schema}.kb_videos (
                        video_id, title, channel_name, channel_id, url,
                        duration_seconds, pipeline_type, content_tags,
                        processing_status, total_chunks, total_insights,
                        processed_at
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (video_id) DO UPDATE SET
                        title = EXCLUDED.title,
                        total_chunks = EXCLUDED.total_chunks,
                        total_insights = EXCLUDED.total_insights,
                        processed_at = EXCLUDED.processed_at
                    """,
                    (
                        video.video_id,
                        video.title,
                        video.channel_name,
                        video.channel_id,
                        video.url,
                        video.duration_seconds,
                        video.pipeline_type,
                        video.tags or [],
                        'completed',
                        video.total_chunks,
                        len(video.insights) if video.insights else 0,
                        datetime.now()
                    )
                )
                conn.commit()
                return cur.rowcount

    def store_insights(self, video_id: str, insights: List[VideoInsight]) -> int:
        """
        Store insights directly in database

        Args:
            video_id: YouTube video ID
            insights: List of VideoInsight objects

        Returns:
            Number of rows affected

        Example:
            >>> with DirectDatabaseLogger(password="your_password") as db:
            ...     rows = db.store_insights("ABC123", insights)
        """
        with self.connect() as conn:
            with conn.cursor() as cur:
                rows = 0
                for insight in insights:
                    cur.execute(
                        f"""
                        INSERT INTO {self.schema}.kb_insights (
                            video_id, insight_text, insight_type, context,
                            category, tags, timestamp_start, timestamp_end,
                            quality_score, priority_level, actionable,
                            next_review_date
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                        """,
                        (
                            video_id,
                            insight.text,
                            insight.type,
                            insight.context,
                            insight.category,
                            insight.tags or [],
                            insight.timestamp_start,
                            insight.timestamp_end,
                            insight.quality_score,
                            insight.priority,
                            insight.actionable,
                            datetime.now().date() + timedelta(days=1)
                        )
                    )
                    rows += cur.rowcount
                conn.commit()
                return rows

    def get_pending_reviews(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get insights due for review

        Args:
            limit: Maximum number of insights to return

        Returns:
            List of insight dictionaries

        Example:
            >>> with DirectDatabaseLogger(password="your_password") as db:
            ...     reviews = db.get_pending_reviews(limit=5)
            ...     for review in reviews:
            ...         print(review['insight_text'])
        """
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT * FROM {self.schema}.v_insights_due_for_review
                    LIMIT %s
                    """,
                    (limit,)
                )
                columns = [desc[0] for desc in cur.description]
                return [dict(zip(columns, row)) for row in cur.fetchall()]


# CLI Helper Functions

def create_video_from_cli_args(
    video_id: str,
    title: str,
    channel: str,
    url: str,
    pipeline_type: str = "ai_tools",
    **kwargs
) -> VideoMetadata:
    """
    Create VideoMetadata from CLI arguments

    Args:
        video_id: YouTube video ID
        title: Video title
        channel: Channel name
        url: Video URL
        pipeline_type: Pipeline type (ai_tools or sports)
        **kwargs: Additional keyword arguments

    Returns:
        VideoMetadata object
    """
    return VideoMetadata(
        video_id=video_id,
        title=title,
        channel_name=channel,
        url=url,
        pipeline_type=pipeline_type,
        **kwargs
    )


def send_to_knowledge_base(
    video_id: str,
    analysis_file: Path,
    url: str,
    webhook_url: str = "https://n8n.vecia.fr/webhook/video-processed",
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Convenience function to send analysis to knowledge base

    Args:
        video_id: YouTube video ID
        analysis_file: Path to analysis JSON
        url: YouTube video URL
        webhook_url: n8n webhook URL
        dry_run: If True, print without sending

    Returns:
        Result dictionary

    Example:
        >>> result = send_to_knowledge_base(
        ...     "ABC123",
        ...     Path("workspace/analysis/ABC123_analysis.json"),
        ...     "https://youtube.com/watch?v=ABC123"
        ... )
        >>> print(f"Success: {result['success']}")
    """
    logger = KnowledgeBaseLogger(webhook_url=webhook_url)
    video = logger.load_from_analysis_json(analysis_file, video_id, url)
    return logger.store_video_insights(video, dry_run=dry_run)


if __name__ == "__main__":
    # Example usage
    print("Database Logger Module")
    print("=" * 50)
    print("\nExample 1: Using webhook (recommended)")
    print("-" * 50)
    print("""
    from db_logger import KnowledgeBaseLogger, VideoMetadata, VideoInsight

    logger = KnowledgeBaseLogger()

    insights = [
        VideoInsight(
            text="Use the HTTP Request node to call external APIs",
            type="tip",
            category="n8n",
            tags=["workflow", "http"],
            quality_score=0.85,
            priority="high"
        )
    ]

    video = VideoMetadata(
        video_id="ABC123",
        title="n8n Tutorial",
        channel_name="IndyDevDan",
        url="https://youtube.com/watch?v=ABC123",
        insights=insights
    )

    result = logger.store_video_insights(video)
    """)

    print("\nExample 2: Load from analysis JSON")
    print("-" * 50)
    print("""
    from pathlib import Path
    from db_logger import send_to_knowledge_base

    result = send_to_knowledge_base(
        video_id="ABC123",
        analysis_file=Path("workspace/analysis/ABC123_analysis.json"),
        url="https://youtube.com/watch?v=ABC123"
    )
    """)

    print("\nExample 3: Direct database access (advanced)")
    print("-" * 50)
    print("""
    from db_logger import DirectDatabaseLogger

    with DirectDatabaseLogger(password="your_password") as db:
        # Store video
        db.store_video(video)

        # Store insights
        db.store_insights(video.video_id, insights)

        # Get pending reviews
        reviews = db.get_pending_reviews(limit=5)
    """)
