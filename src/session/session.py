from requests.sessions import Session

from .exceptions import ConnectionError


class YouTubeSession():
    def __init__(self) -> None:
        self.session = Session()

    def get_content(self,
                    url):
        """
        Use the session to get the content of the asked url

        Parameters:
            - url: URL to get the content from
        """
        data = self.session.get(url)

        if data.status_code // 100 != 2:
            raise ConnectionError(f"Issue Retrieving Data [{data.reason}]")

        return data.content