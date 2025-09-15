from .constants import YouTubeSearchTypes


class SearchItem():
    def __init__(self,
                 item_id: str,
                 item_class: YouTubeSearchTypes) -> None:
        self.item_id = item_id
        self.item_class = item_class
    
    