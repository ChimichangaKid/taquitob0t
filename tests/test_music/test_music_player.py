import unittest
import pytest
from unittest.mock import Mock, patch
from taquitobot.music_commands.my_youtube.youtube_exceptions import SongException
from taquitobot.music_commands.music_commands import MusicPlayer


"""
Unit testing for discord bot is kind of difficult, so I have stuck to unit testing the helper functions and the classes
rather than the discord commands.
"""

class TestMusicCommands(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.bot = Mock()
        self.ctx = Mock()
        self.ctx.message.author.voice = Mock()
        self.ctx.voice.client = Mock()

        self.music_player = MusicPlayer(self.bot)

    def test_music_player_setup(self) -> None:
        self.assertEqual(self.music_player.bot, self.bot)
        self.assertEqual(self.music_player.is_playing, False)
        self.assertEqual(self.music_player.title_list, [])
        self.assertEqual(self.music_player.song_queue, [])
        self.assertEqual(self.music_player.voice, None)
        self.assertEqual(self.music_player.current_song, '')

    @patch('taquitobot.music_commands.music_commands.fetch_song', return_value={ 'entries': [{'title': 'Test Song', 'url': 'https://youtube.com/test'}]}, autospec=True)
    async def test_queue_song_successful(self, mock_fetch_song) -> None:
        output = await self.music_player.queue_song('Test Song')

        self.assertEqual(output, 'Test Song')
        self.assertEqual(self.music_player.title_list, ['Test Song'])
        self.assertEqual(self.music_player.song_queue, ['https://youtube.com/test'])

    @patch('taquitobot.music_commands.music_commands.fetch_song', return_value=None, autospec=True)
    async def test_queue_song_failure(self, mock_fetch_song) -> None:

        with pytest.raises(Exception) as se:
            await self.music_player.queue_song('Nonexistent Song')
        assert str(se.value) == "Unable to fetch song from YouTube."

if __name__ == "__main__":
    unittest.main()
    