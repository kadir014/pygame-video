# Pygame Video Player 📺
<p>
  <img src="https://img.shields.io/badge/python-3.9%2B-green">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg">
  <img src="https://img.shields.io/badge/version-2.0.0-orange">
</p>
This module provides a simple API to let developers use videos in their Pygame apps. Audio playback doesn't use `pygame.mixer`.

## Installing
```
pip install pygamevideo
```
or just copy-paste `pygamevideo.py` to your working directory.

## Usage
```py
import pygame
from pygamevideo import Video

pygame.init()
window = pygame.display.set_mode(...)

# Load the video from the specified dir
video = Video("video.mp4")

# Start the video
video.play()

# Main loop
while True:
  ...

  # Draw video to display surface
  # this function should be called every frame
  video.draw_to(window, (0, 0))

  # Update pygame display
  pygame.display.flip()
```

## Dependencies
- [Python](https://www.python.org/downloads/) 3.9+
- [Pygame Community Edition](https://github.com/pygame-community/pygame-ce) 2.20.0+
- [NumPy](https://pypi.org/project/numpy/)
- [OpenCV](https://pypi.org/project/opencv-python/)
- [FFPyPlayer](https://pypi.org/project/ffpyplayer/)

# API Reference
You can just use the docstrings as well.

## `class Video(filepath)`
Pygame video player class.

- ### Parameters
   `filepath` : Filepath of the video source.

- ### Attributes & Properties
   - `is_ready` : Is the video source loaded and ready to play?
   - `frame_width` : Default frame width in pixels.
   - `frame_height` : Default frame height in pixels.
   - `is_playing` : Is the video currently playing?
   - `is_paused` : Is the video currently paused?
   - `is_looped` : Is looping enabled?
   - `volume` : Volume of the audio.
   - `is_muted` : Is the audio muted?
   - `fps` : Framerate of the video.
   - `total_frames` : Total amount of frames of the video.
   - `duration` : Total duration of the video in milliseconds.
   - `current_time` : Current time into the video in milliseconds.
   - `remaining_time` : Remaining time left in the video in milliseconds.
   - `current_frame` : Current frame into the video.
   - `remaining_frames` : Remaining frames left in the video.
   - `current_time` : Current time into the video in milliseconds.

- ### Methods
   - `load(filepath: Union[str, os.PathLike])` : Load a video from file path. This method is also called implicitly when instantiated.
   - `reload()` : Reload the video from the same filepath.
   - `release()` : Release the resources used by the video player.
   - `play(loop: bool = False)` : Start playing the video.
   - `stop()` : Stop playing the video.
   - `pause()` : Pause the video.
   - `resume()` : Resume the video.
   - `toggle_pause()` : Switch between paused states.
   - `mute()` : Mute audio playback.
   - `unmute()` : Unmute audio playback.
   - `seek_time(timepoint: float)` : Seek into desired timepoint.
   - `seek_frame(frame: int)` : Seek into desired frame.
   - `get_frame()` : Advance the video and return the current frame. Must be called once per frame.
   - `draw_to(dest_surface: pygame.Surface, position: Coordinate)` : Blit the current video frame to the surface.

# License
[MIT](LICENSE) © Kadir Aksoy