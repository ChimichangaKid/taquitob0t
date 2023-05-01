#Taquitobot

GitHub codebase for a personal discord bot to play music. 

###Version 1.0.0

###Commands
Commands are followed by a "$" prefix

####Play (aliases 'p', 'P')
Queues a song to be played on the bot next, if no songs are playing immediately play the queued song. Songs queued are played in a FIFO order.

####Pause
Pauses the current track if the track is playing otherwise resume the track.

####Leave (aliases 'disconnect', 'l', 'L')
Disconnects the bot from the current discord channel if possible.

####Skip (aliases 's', 'S')
Skips the current song that is playing and plays the next song in queue if possible.

####Queue (aliases 'q', 'Q')
Shows the current songs that are in queue
