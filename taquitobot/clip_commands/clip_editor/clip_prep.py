"""
clip_prep.py

Class implementation to parse the video footage and find the information about
timings as well as audio selection to separate the process from the editor.
This class will contain all the information required for editing the video.

Attributes:

TODO:

Versioning:
    Author: Aidan (ChimichangaKid)
    Date: 2024-07-25
    Version: 1.0.0

Notes:
    
"""

class ClipPrepAbstract:

    def __init__(self, game_title: str) -> None:
        self._game_title = game_title
        self._highlight_time = self._find_highlight_time()

    def _choose_random_song(self, music_folder: str) -> str:
        """
        Helper function to get a random song form the specified folder.

        Args:
            music_folder (str):
        """
        ...

    def _find_highlight_time(self) -> float:
        ...


class ClipPrepValorant(ClipPrepAbstract):

    def __init__(self, game_title: str) -> None:
        super().__init__(game_title)
    
    def _find_highlight_time(self) -> float:
        return super()._find_highlight_time()

class ClipPrepLeagueOfLegends(ClipPrepAbstract):

    def __init__(self, game_title: str) -> None:
        super().__init__(game_title)
    
    def _find_highlight_time(self) -> float:
        return super()._find_highlight_time()
