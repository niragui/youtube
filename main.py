import json

from src.session.session import YouTubeSession
from src.search.searcher import YouTubeSearcher


session = YouTubeSession()
searcher = YouTubeSearcher(session)

data = searcher.search("Taylor Swift")

print(data)