from typing import Optional

import datetime

import json

import os
import sys

from .item import YouTubeItem
from .constants import YoutubeTypes
from ..session.session import YouTubeSession


THIS_FOLDER = os.path.dirname(__file__)
AUTOMATIONS_FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(THIS_FOLDER)))

sys.path.append(AUTOMATIONS_FOLDER)

from BeautifulSoup.src.parser import MySoup
from BeautifulSoup.src.elements.filter import NodeFilter

BASE_URL = "https://www.youtube.com/watch"


class YouTubeVideo(YouTubeItem):
    def __init__(self,
                 video_id: str,
                 session: Optional[YouTubeSession] = None,
                 read_data: bool = True) -> None:
        self._title = ""
        self._channel_id = ""
        self._channel_name = ""

        self._image = ""

        self._release_date = None
        self._views = 0
        self._likes = 0

        self._duration = 0

        #self._qualities = []
        #self._available_countries = []

        self._category = ""
        super().__init__(video_id, YoutubeTypes.VIDEO, session, read_data)

    def set_data(self,
                 data: dict):
        """
        Given the API response, sets the items

        Parameters:
            - data: API Dictionary response
        """
        video_details = data.get("videoDetails", {})
        micro_format = data.get("microformat", {})
        micro_format = micro_format.get("playerMicroformatRenderer", {})

        self._title = video_details.get("title", "")
        self._channel_id = video_details.get("channelId", "")
        self._channel_name = video_details.get("author", "")

        self._views = int(video_details.get("viewCount", "0"))

        images = video_details.get("thumbnail", {})
        images = images.get("thumbnails", [])

        self._image = ""
        if len(images) > 0:
            last_image = images[-1]
            self._image = last_image["url"]

        self._likes = int(micro_format.get("likeCount", "0"))
        self._duration = int(micro_format.get("lengthSeconds", "0"))
        release_date = micro_format.get("publishDate", None)
        if release_date:
            self._release_date = datetime.datetime.fromisoformat(release_date)
            self._release_date = self._release_date.astimezone(datetime.timezone.utc)

        self._category = micro_format.get("category", "")

    def get_url(self):
        """
        Returns the url of the video
        """
        return f"{BASE_URL}?v={self.item_id}"

    def get_title(self, reset_values: bool = False):
        """
        Get the title of the playlist.

        Parameters:
            - reset_values (Optional): If it should ask for the
                playlist information again
        """
        return self.get_attr("_title", reset_values)

    @property
    def title(self):
        """
        Get the title of the playlist.
        """
        return self._title

    def get_author(self, reset_values: bool = False):
        """
        Get the author of the playlist.

        Parameters:
            - reset_values (Optional): If it should ask for the
                playlist information again
        """
        return self.get_attr("_channel_name", reset_values)

    @property
    def author(self):
        """
        Get the author of the playlist.
        """
        return self._channel_name

    def get_likes(self, reset_values: bool = False):
        """
        Get the likes of the playlist.

        Parameters:
            - reset_values (Optional): If it should ask for the
                playlist information again
        """
        return self.get_attr("_likes", reset_values)

    @property
    def likes(self):
        """
        Get the likes of the playlist.
        """
        return self._likes

    def get_views(self, reset_values: bool = False):
        """
        Get the views of the playlist.

        Parameters:
            - reset_values (Optional): If it should ask for the
                playlist information again
        """
        return self.get_attr("_views", reset_values)

    @property
    def views(self):
        """
        Get the views of the playlist.
        """
        return self._views

    def get_image(self, reset_values: bool = False):
        """
        Get the image of the playlist.

        Parameters:
            - reset_values (Optional): If it should ask for the
                playlist information again
        """
        return self.get_attr("_image", reset_values)

    @property
    def image(self):
        """
        Get the image of the playlist.
        """
        return self._image

    def get_release_date(self, reset_values: bool = False):
        """
        Get the release_date of the playlist.

        Parameters:
            - reset_values (Optional): If it should ask for the
                playlist information again
        """
        return self.get_attr("_release_date", reset_values)

    @property
    def release_date(self):
        """
        Get the release_date of the playlist.
        """
        return self._release_date
    
    def get_channel_url(self):
        """
        Get the URL of the channel
        """
        return f"https://www.youtube.com/channel/{self._channel_id}"