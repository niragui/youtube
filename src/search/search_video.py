from .search_item import SearchItem
from .constants import YouTubeSearchTypes


class SearchVideo(SearchItem):
    def __init__(self,
                 data: dict) -> None:
        item_id = data["videoId"]
        search_type = YouTubeSearchTypes.VIDEO

        super().__init__(item_id, search_type)

        self.title = ""
        self.author = ""
        self.author_id = ""

        self.duration = ""
        self.views = 0

        self.set_data(data)

    def set_data(self,
                 data: dict):
        """
        Set the class data from the API response data

        Parameters:
            - data: Dictionary of the API data response
        """
        title_data = data.get("title", {})
        runs = title_data.get("runs", [{}])
        title_run = runs[0]

        self.title = title_run.get("text", "")

        author_data = data.get("ownerText", {})
        runs = author_data.get("runs", [{}])
        author_run = runs[0]

        self.author = author_run.get("text", "")

        author_browse = author_run.get("browseEndpoint", {})
        self.author_id = author_browse.get("browseId", "")

        duration_text = data.get("lengthText", {})
        self.duration = duration_text.get("simpleText", "")

        views_text = data.get("viewCountText", {})
        views_text = views_text.get("simpleText", "")
        views_text = views_text.split(" ")[0]
        views_text = views_text.replace(",", "").replace(".", "")

        if views_text.isdigit():
            self.views = int(views_text)

    def __repr__(self) -> str:
        return f"SearchVideo(ID: {self.item_id} | Name: {self.title} | Author: {self.author})"

    def __str__(self) -> str:
        return f"SearchVideo(ID: {self.item_id} | Name: {self.title} | Author: {self.author})"