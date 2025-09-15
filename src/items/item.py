from typing import Optional

import json

from ..session.session import YouTubeSession

from ..common.filters import is_json_script, is_nonce_script
from .exceptions import SubClassMethod
from .constants import YoutubeTypes

import os
import sys

THIS_FOLDER = os.path.dirname(__file__)
AUTOMATIONS_FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(THIS_FOLDER)))

sys.path.append(AUTOMATIONS_FOLDER)

from BeautifulSoup.src.parser import MySoup
from BeautifulSoup.src.elements.filter import NodeFilter


class YouTubeItem():
    def __init__(self,
                 item_id: str,
                 item_type: YoutubeTypes,
                 session: Optional[YouTubeSession] = None,
                 read_data: bool = True):
        self.item_id = item_id
        self.item_type = item_type
        if session is None:
            session = YouTubeSession()

        self.session = session

        if read_data:
            self.read_data()

    def set_data(self,
                 data: dict):
        """
        Sets the parameters from the API response.

        Parameters:
            - data: Dictionary response gotten from the API
        """
        raise SubClassMethod(f"set_data Needs To Be Created For Each Class")

    def get_url(self):
        """
        Returns the URL to acces the item via web browser
        """
        raise SubClassMethod(f"get_url Needs To Be Created For Each Class")

    def read_data(self):
        """
        Asks the YouTube endpoint to set the playlist data.
        """
        content = self.session.get_content(self.get_url()).decode("utf-8")

        filter = NodeFilter("script", is_json_script, is_nonce_script)

        soup = MySoup(content)

        scripts = soup.find_all(filter)

        json_text = scripts[0]._text(True)
        json_text_start = json_text.find(" = ") + 3
        json_text = json_text[json_text_start:-1]

        data = json.loads(json_text)

        self.set_data(data)

    def get_attr(self, attr_name: str, reset_values: bool = False):
        """
        Get an attribute of the item.

        Parameters:
            - attr_name: Name of the attribute to retrieve
            - reset_values (Optional): If it should ask for the
                album information again
        """
        if reset_values:
            self.read_data()

        if not hasattr(self, attr_name):
            raise Exception(f"{self} Item Does Not Have A {attr_name} Attribute")

        return getattr(self, attr_name)

    def reload(self):
        """
        Asks the API for the data again
        """
        self.read_data()
