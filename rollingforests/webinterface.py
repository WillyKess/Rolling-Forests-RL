from io import BytesIO
import base64
import numpy as np
from PIL import Image
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

class WebInterface:
    def __init__(self, game_url='https://rollingforests.rayhanadev.repl.co/', headless=False):
        self.game_url = game_url
        firefox_options = Options()
        firefox_options.headless = headless
        self._driver = Firefox(options=firefox_options, service_log_path="/dev/null", )
        self._driver.set_window_position(x=0, y=0)
        self._driver.set_window_size(960, 625)
        self._driver.get(game_url)

    def end(self):
        self._driver.close()

    def grab_screen(self):
        screen = np.asarray(Image.open(BytesIO(base64.b64decode(self._driver.get_screenshot_as_base64()))))
        return screen[..., :3]

    def go_left(self):
        self._driver.find_element_by_tag_name("body").send_keys(Keys.ARROW_LEFT)

    def go_right(self):
        self._driver.find_element_by_tag_name(
            "body").send_keys(Keys.ARROW_RIGHT)

    def jump(self):
        self._driver.find_element_by_tag_name("body").send_keys(Keys.SPACE)

    def pause(self):
        self._driver.find_element_by_tag_name("body").send_keys("P")
