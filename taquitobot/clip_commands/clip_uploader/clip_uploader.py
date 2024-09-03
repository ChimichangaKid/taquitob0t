# =============================================================================
#
# Title: clip_uploader.py
#
# Author: Aidan
#
# Description: Script to upload videos to youtube under The Garchive account.
#
# =============================================================================

# =============================================================================
#
#                                     Imports
#
# =============================================================================
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType


# =============================================================================
#
#                               Constant Declaration
#
# =============================================================================
current_dir = os.getcwd()
FILE_PATH = os.path.abspath(__file__)
FOLDER_PATH = os.path.dirname(FILE_PATH)
DATA_RELATIVE_PATH = "selenium"
DATA_PATH = os.path.join(FOLDER_PATH, DATA_RELATIVE_PATH)

chrome_options = Options()
# chrome_options.add_experimental_option("detach", True) # This will keep the tab open for debugging
chrome_options.add_argument(f"user-data-dir={DATA_PATH}") 
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')



# =============================================================================
#
#                                   Classes
#
# =============================================================================
class YouTubeUploader:

    def __init__(self, video_path, video_title, game_title):
        self.driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=chrome_options)
        self.video_path = video_path
        self.game_title = game_title
        self.video_title = video_title + f' #{game_title} #{game_title}Clip #{game_title}Guides #{game_title}Funny'
        self.video_title = self.video_title[:100]
        self.DESCRIPTION_TEMPLATE = f"""
{game_title} Gameplay {game_title} highlights {game_title} Clips {game_title} Plays {game_title} Montage {game_title} Shorts
{game_title} Duelist {game_title} Clutches {game_title} Masters {game_title} AI {game_title} Phoenix {game_title} Jett {game_title} Yoru
{game_title} Lineups {game_title} Fast Plant {game_title} Strategy {game_title} Map {game_title} Agent {game_title} Rework {game_title} Streamer
{game_title} Goat {game_title} Sentinels {game_title} Duelists {game_title} Speedrun {game_title} Champions {game_title} Best Moments 
{game_title} High Elo {game_title} Aim {game_title} Vandal Mr Big Meteors DigDaddyDavid {game_title} Cracked {game_title} Funny Moments
{game_title} jester {game_title} skibidi modded {game_title} {game_title} Jumpscare Tenz xQc Faker Golden Freddy {game_title} new update
Mr Beast Tyler1 InnoTurtle Laplace's Demon No Hud Crown Royale {game_title} Worlds {game_title} prize {game_title} cheats {game_title} hacks
{game_title} radiant {game_title} glitches {game_title} patch notes {game_title} replay system {game_title} free new skins {game_title} bobs
{game_title} pros {game_title} fnaf {game_title} asmr {game_title} lofi beats Valorant Outlaw Valorant New gun Valorant Kuronami Bundle
"""
        self.DESCRIPTION_TEMPLATE = self.DESCRIPTION_TEMPLATE[:5000]

    def upload_video_to_YT(self):
        """
        Uploads the video to youtube that was provided, should be a #shorts video.
        :return: A string that is a link to the uploaded video.
        """
        self.driver.get('https://www.youtube.com')

        self.driver.implicitly_wait(7)
        
        # Click first upload button
        upload_button = self.driver.find_element(By.XPATH, '//yt-icon[contains(@class, "style-scope ytd-topbar-menu-button-renderer")]')
        upload_button.click()
        
        self.driver.implicitly_wait(7)

        # Click second button to get to video manager page
        upload_button_2 = self.driver.find_element(By.XPATH,'//tp-yt-paper-item[.//yt-formatted-string[contains(text(), "Upload video")]]')
        upload_button_2.click()
        
        self.driver.implicitly_wait(7)

        # Add the file to youtube
        print('uploading file')
        file_input = self.driver.find_element(By.XPATH,'//input[@type="file"]')
        file_path = os.path.join(current_dir, self.video_path)
        file_input.send_keys(file_path)

        time.sleep(5)
        # Add title
        print('adding title')
        textbox_element = self.driver.find_element(By.XPATH, '//div[@id="textbox" and contains(@class, "ytcp-social-suggestions-textbox")]')
        textbox_element.clear()
        textbox_element.send_keys(self.video_title) 

        self.driver.implicitly_wait(4)

        # Add description
        time.sleep(3)
        description_box = self.driver.find_element(By.XPATH, '//div[@aria-label="Tell viewers about your video (type @ to mention a channel)"]')
        description_box.clear()
        description_box.send_keys(self.DESCRIPTION_TEMPLATE)

        time.sleep(3)
        # Click the 'not made for kids button'
        print('selecting not made for kids')
        not_made_for_kids_button = self.driver.find_element(By.XPATH, '//tp-yt-paper-radio-button[@name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]')
        not_made_for_kids_button.click()

        time.sleep(5)
        self.driver.implicitly_wait(7)
        # Skip through all the other tabs
        print('skipping through the other tabs')
        next_button = self.driver.find_element(By.XPATH, '//ytcp-button[@id="next-button"]')
        next_button.click()
        self.driver.implicitly_wait(3)
        print('skipped tab 1')
        next_button.click()
        self.driver.implicitly_wait(3)
        print('skipped tab 2')
        next_button.click()
        print('skipped tab 3')
        self.driver.implicitly_wait(7)
        
        # make video public
        print('making video public')
        public_button = self.driver.find_element(By.XPATH, '//tp-yt-paper-radio-button[@name="PUBLIC"]')
        public_button.click()
        time.sleep(40)
        self.driver.implicitly_wait(10)
        # Get the link to the new video
        print('getting link')
        link_element = self.driver.find_element(By.XPATH, '//a[contains(@class, "style-scope ytcp-video-info")]')
        link_url = link_element.get_attribute('href')
        print(f'Youtube link is: {link_url}')
        

        self.driver.implicitly_wait(10)
        # publish the video
        print('publishing video')
        publish_button = self.driver.find_element(By.XPATH, '//ytcp-button[@id="done-button"]')
        publish_button.click()

        time.sleep(3)
        
        self.driver.implicitly_wait(7)
        self.driver.quit()

        return link_url
    

    def delete_old_video(self):
        """
        Function to remove the local instance of the video when done.
        """
        if os.path.exists(self.video_path):
            os.remove(self.video_path)
            print(f'Deleted {self.video_path}')
