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

# =============================================================================
#
#                               Constant Declaration
#
# =============================================================================
current_dir = os.getcwd()
chrome_options = Options()
# chrome_options.add_experimental_option("detach", True) This will keep the tab open for debugging
chrome_options.add_argument("user-data-dir=taquitob0t/taquitobot/clip_commands/clip_uploader/selenium") 
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

DESCRIPTION_TEMPLATE = """
Valorant Gameplay Valorant highlights Valorant Clips Valorant Plays Valorant Montage Valorant Shorts,
Valorant Duelist Valorant Clutches Valorant Masters Valorant AI Valorant Phoenix Valorant Jett Valorant Yoru
Valorant Lineups Valorant Fast Plant Valorant Strategy Valorant Map Valorant Agent Valorant Rework
"""

# =============================================================================
#
#                                   Classes
#
# =============================================================================
class YouTubeUploader:

    def __init__(self, video_path, video_title):
        self.driver = webdriver.Chrome(options=chrome_options)
        self.video_path = video_path
        self.video_title = video_title + ' #valorant #outplay'

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
        description_box.send_keys(DESCRIPTION_TEMPLATE)

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
        time.sleep(50)
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
