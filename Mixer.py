import pygame
import time

def playsound(soundfile, vol):
    """Play sound through default mixer channel in blocking manner.
       This will load the whole sound into memory before playback
    """    
    pygame.init()
    pygame.mixer.init()
    sound = pygame.mixer.Sound(soundfile)
    sound.set_volume(vol)
    clock = pygame.time.Clock()
    sound.play()
    # if pygame.mixer.get_busy():
    #     sound.stop()
    # while pygame.mixer.get_busy():
    #     # print("Playing... - func => playsound")
    #     clock.tick(1000)
 
def playmusic(soundfile, vol):
    """Stream music with mixer.music module in blocking manner.
       This will stream the sound from disk while playing.
    """
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    pygame.mixer.music.load(soundfile)
    pygame.mixer.music.set_volume(vol)
    pygame.mixer.music.play()
    # if pygame.mixer.get_busy():
    #     pygame.mixer.music.stop()
    # while pygame.mixer.music.get_busy():
    #     # print("Playing... - func => playingmusic")
    #     clock.tick(1000)
         
 
def stopmusic():
    """stop currently playing music"""
    pygame.mixer.music.stop()
 
def getmixerargs():
    pygame.mixer.init()
    freq, size, chan = pygame.mixer.get_init()
    return freq, size, chan
 
 
def initMixer():
    BUFFER = 8192  # audio buffer size, number of samples since pygame 1.8.
    FREQ, SIZE, CHAN = getmixerargs()
    pygame.mixer.init(FREQ, SIZE, CHAN, BUFFER)
 
 
'''You definitely need test mp3 file (a.mp3 in example) in a directory, say under 'C:\\Temp'
   * To play wav format file instead of mp3, 
      1) replace a.mp3 file with it, say 'a.wav'
      2) In try except clause below replace "playmusic()" with "playsound()"
     
'''