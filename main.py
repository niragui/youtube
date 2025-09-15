import json

from src.session.session import YouTubeSession
from src.search.searcher import YouTubeSearcher
from src.items.video import YouTubeVideo


session = YouTubeSession()
video_id = "b7QlX3yR2xs"
video = YouTubeVideo(video_id, session)