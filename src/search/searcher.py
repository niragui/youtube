from typing import Optional, List

import json

from ..session.session import YouTubeSession
from ..common.filters import is_json_script, is_nonce_script

from .constants import YouTubeSearchTypes
from .search_video import SearchVideo

import os
import sys

THIS_FOLDER = os.path.dirname(__file__)
AUTOMATIONS_FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(THIS_FOLDER)))

sys.path.append(AUTOMATIONS_FOLDER)

from BeautifulSoup.src.parser import MySoup
from BeautifulSoup.src.elements.filter import NodeFilter

BASE_URL = "https://www.youtube.com/results"

SEARCH_PARAM = "search_query"
TYPE_PARAM = "sp"

VIDEO_TYPE = "videoRenderer"
TRANSFORMER = {}
TRANSFORMER[VIDEO_TYPE] = SearchVideo


class YouTubeSearcher():
    def __init__(self,
                 session: Optional[YouTubeSession]) -> None:
        if session is None:
            session = YouTubeSession()

        self.session = session

    def get_items(self,
                  data: dict):
        """
        Parse the search API response into items

        Parameters:
            - data: Search API response
        """

        items = data.get("contents", {})
        items = items.get("twoColumnSearchResultsRenderer", {})
        items = items.get("primaryContents", {})
        items = items.get("sectionListRenderer", {})
        items = items.get("contents", [{}])
        items = items[0].get("itemSectionRenderer", {})
        items = items.get("contents", [])

        return items

    def parse_response(self,
                       data: List[dict]):
        """
        Parse the response into a list of class items

        Parameters:
            - data: API response to parse
        """
        responses = []
        for item in data:
            if not isinstance(item, dict):
                continue

            if len(item) == 0:
                continue

            main_key = list(item.keys())[0]

            creator = TRANSFORMER.get(main_key, None)
            if creator is None:
                continue

            responses.append(creator(item[main_key]))

        return responses

    def search(self,
               search_term: str,
               search_type: Optional[YouTubeSearchTypes] = None):
        """
        Returns a list with ID and Type of the items found.

        Parameters:
            - search_term: Term to search
            - search_type: Type to to search. If None, all types will be searched.
        """
        url = f"{BASE_URL}?{SEARCH_PARAM}={search_term}"
        if search_type:
            url += f"&{TYPE_PARAM}={search_type.value}"

        content = self.session.get_content(url).decode("utf-8")

        filter = NodeFilter("script", is_json_script, is_nonce_script)

        soup = MySoup(content)

        scripts = soup.find_all(filter)

        json_text = scripts[0]._text(True)
        json_text_start = json_text.find(" = ") + 3
        json_text = json_text[json_text_start:-1]

        data = json.loads(json_text)

        items = self.get_items(data)

        return self.parse_response(items)