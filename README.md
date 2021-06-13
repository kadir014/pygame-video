# Pygame Video Player
`pygamevideo` module helps developer to embed videos into their Pygame display. Audio playback doesn't use `pygame.mixer`.

## Installing
```
pip install pygamevideo
```
or just copy-paste `pygamevideo.py` to your working directory

## Usage
```py
import pygame
from pygamevideo import Video

window = pygame.display.set_mode()

video = Video("video.mp4")

# start video
video.play()

# main loop
while True:
  ...

  # draw video to display surface
  # this function must be called every tick
  video.draw_to(window, (0, 0))

  # set window title to current duration of video as hour:minute:second
  t = video.current_time.format("%h:%m:%s")
  pygame.display.set_caption(t)
```

## Dependencies
- [pygame](https://pypi.org/project/pygame/)
- [numpy](https://pypi.org/project/numpy/)
- [opencv-python](https://pypi.org/project/opencv-python/)
- [ffpyplayer](https://pypi.org/project/ffpyplayer/)

## Reference

## `class Video(filepath)`
Pygame video player class

### Parameters
`filepath` : Filepath of the video source

### Methods & Attributes
`load(filepath)` : Load another video source

<br>

`release()` : Release resources

#### Related to playback control
`play(loop=True)` : Starts video playback
   - `loop` : Is video looped or not

<br>

`restart()` : Restarts already playing video

<br>

`stop()` : Stops video

<br>

`pause()` : Pauses video

<br>

`resume()` : Resumes video

<br>

`is_playing` : Whether the video is playing or not (bool)

<br>

`is_ended` : Whether the video has ended or not (bool)

<br>

`is_paused` : Whether the video is paused or not (bool)

<br>

`is_ready` : Whether the resources and video is ready to play (bool)

### Related to audio control
`mute()` : Mutes audio

<br>

`unmute()` : Unmutes audio

<br>

`has_audio()` : **NOT IMPLEMENTED**

<br>

`set_volume(volume)` : Sets audio volume
   - `volume` : Floating number between 0.0 and 1.0

<br>

`is_muted` : Whether the audio is muted or not (bool)

<br>

`volume` : Audio volume (float)

### Related to timing control
`duration` : Length of the video as [Time](#Time) object

<br>

`current_time` : Current time of the video as [Time](#Time) object

<br>

`remaining_time` : Remaining time till the end of the video as [Time](#Time) object

<br>

`total_frames` : Length of the video as frames (int)

<br>

`current_frame` : Current frame of the video (int)

<br>

`remaining_frames` : Remaining frames till the end of the video (int)

<br>

`seek_time(t)` : Jump into a specific time of the video
   - `t` : [Time](#Time) object
   - `t` : Representation of time in string, eg: "00:01:05:200" meaning 1 minute, 5 seconds and 200 milliseconds (str)
   - `t` : Milliseconds (int)

<br>

`seek_frame(frame)` : Jump into a specific frame of the video
- `frame` : Frame number (int)

### Related to resizing & frame dimensions
`get_size()` : Returns video size (tuple)

<br>

`get_width()` : Returns video width (int)

<br>

`get_height()` : Returns video height (int)

<br>

`set_size(size)` : Resizes video
   - `size` : New size (tuple)

<br>

`set_width(width)` : Resizes video
  - `width` : New width (int)

<br>

`set_height(height)` : Resizes video
   - `height` : New height (int)

<br>

`keep_aspect_ratio` : Keeps original aspect ratio while resizing the video (bool)

### Drawing the video
`draw_to(surface, pos)` : Draws the video onto the surface. This functions must be called every tick.
   - `surface` : Destination surface (pygame.Surface)
   - `pos` : Blitting position (tuple)

<br>

`get_frame()` : Returns the current video frame as pygame.Surface. This function is used by `draw_to` function, so use only one of both each tick


## `class Time`
Data class used to represent duration and such things by `Video` class
