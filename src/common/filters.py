JSON_PLAYER_START = "var ytInitialPlayerResponse"
JSON_SEARCHER_START = "var ytInitialData"



def is_nonce_script(attrs: dict):
    """
    Check if its a nonce script

    Parameters:
        - attrs: Attributes of the node
    """
    return "nonce" in attrs

def is_json_script(text: str):
    """
    Check if its the script of nonce

    Parameters:
        - text: Text of the node
    """
    return JSON_PLAYER_START in text or JSON_SEARCHER_START in text