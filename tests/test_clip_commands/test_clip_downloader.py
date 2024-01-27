import unittest
from unittest.mock import patch, mock_open, Mock, MagicMock
from taquitobot.clip_commands.clip_downloader.clip_downloader import download_video, extract_video_link, download_outplayed_clip_from_discord_message

class TestClipDownloader(unittest.TestCase):

    test_video_link = r'https://outplayed\.tv/media/test_video.mp4'
    expected_video_link = 'test_video.mp4'

    @patch('requests.get')
    @patch('builtins.open', new_callable=mock_open())
    def test_download_video_output(self, mock_open, mock_requests_get):
        mock_response = Mock()
        mock_response.iter_content.return_value = [b'some', b'data']
        mock_requests_get.return_value = mock_response

        output = download_video(self.test_video_link)
        self.assertEqual(output, self.expected_video_link)

    @patch('requests.get')
    @patch('builtins.open', new_callable=mock_open())
    def test_download_video_steps(self, mock_open, mock_requests_get):
        mock_response = Mock()
        mock_response.iter_content.return_value = [b'some', b'data']
        mock_requests_get.return_value = mock_response

        output = download_video(self.test_video_link)
        mock_open.assert_called_once_with(self.expected_video_link, 'wb')

    @patch('requests.get')
    def test_extract_video_link(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.text = """
                    <html>
                        <body>
                            <video src="https://example.com/test.mp4"></video>
                            <title>Highlight #GameTitle | Captured by #Outplayed</title>
                        </body>
                    </html>
                """
        mock_requests_get.return_value = mock_response

        mp4_link, game_title = extract_video_link('https://example.com/outplayed-clip')

        self.assertEqual(mp4_link, 'https://example.com/test.mp4')
        self.assertEqual(game_title, 'GameTitle')

    @patch('taquitobot.clip_commands.clip_downloader.clip_downloader.extract_video_link')
    @patch('taquitobot.clip_commands.clip_downloader.clip_downloader.download_video')
    def test_download_outplayed_clip_from_discord_message(self, mock_download_video, mock_extract_video_link):
        mock_extract_video_link.return_value = ('https://example.com/test.mp4', 'GameTitle')
        mock_download_video.return_value = 'test.mp4'

        video_file, video_title, game_title = download_outplayed_clip_from_discord_message(
            'Test Title\nhttps://outplayed.tv/media/MPYZkr'
        )

        self.assertEqual(video_file, 'test.mp4')
        self.assertEqual(video_title, 'Test Title')
        self.assertEqual(game_title, 'GameTitle')
