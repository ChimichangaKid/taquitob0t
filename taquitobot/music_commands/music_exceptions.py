# =============================================================================
#
# Title: music_exceptions.py
#
# Author: Aidan
#
# Description: File to describe all exceptions related to music requests.
#
# =============================================================================

# =============================================================================
#
#                                     Classes
#
# =============================================================================


class JoinException(Exception):
    """
    A JoinException is a subclass of an Exception to describe an issue with connecting to a discord voice channel.
    """
    pass