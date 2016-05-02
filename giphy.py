from giphypop import translate
from secure_config import giphy_api_key


class Giphy:
    api_key = giphy_api_key
    img = None

    def __init__(self, phrase):
        self.img = translate(phrase, self.api_key)

    def get_search_result(self):
        if self.img is None:
            return 'Soryan. Nothing found. :('
        else:
            return self.img.media_url
