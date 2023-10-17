from typing import Union

import time
import os
import atexit

import pygame
import numpy
import cv2
from ffpyplayer.player import MediaPlayer


__version__ = "2.0.0"


class Video:
    """
    Pygame video player.
    """

    def __init__(self, filepath: Union[str, os.PathLike]) -> None:
        """
        Parameters
        ----------
        @param filepath File path to the video to load.
        """

        self.is_ready = False
        self.load(filepath)

        # Release before exiting interpreter to prevent segfault
        atexit.register(self.release)

    def __repr__(self) -> str:
        return f"<{__name__}.{self.__class__.__name__}(frame#{self.current_frame})>"
    
    def __del__(self) -> None:
        self.release()

    def load(self, filepath: Union[str, os.PathLike]) -> None:
        """
        Load a video from file path.
        This method is also called implicitly when instantiated.

        Parameters
        ----------
        @param filepath File path to the video to load.
        """

        filepath = str(filepath)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"No such file or directory: '{filepath}'")

        self.filepath = filepath

        self.is_playing = False
        self.is_paused = False
        self.is_looped = False

        self.draw_frame = 0
        self.start_time = 0
        self.__start_time = 0

        self.__volume = 1.0
        self.is_muted = False
        self.__volume_before_mute = 1.0

        self.__vidcap = cv2.VideoCapture(self.filepath)
        ff_opts = {"fast": True, "framedrop": True, "paused": True}
        self.__ff = MediaPlayer(self.filepath, ff_opts=ff_opts)

        self.fps = self.__vidcap.get(cv2.CAP_PROP_FPS)

        self.total_frames = int(self.__vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

        self.frame_width = int(self.__vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.__vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.frame_surf = pygame.Surface((self.frame_width, self.frame_height)).convert()

        self.is_ready = True

    def reload(self) -> None:
        """ Reload the video from the same filepath. """

        self.release()
        self.load(self.filepath)

    def release(self) -> None:
        """ Release the resources used by the video player. """

        if self.is_ready:
            self.__vidcap.release()
            self.__ff.close_player()
            self.is_ready = False

    # Control methods

    def play(self, loop: bool = False) -> None:
        """
        Start playing the video.

        Parameters
        ----------
        @param loop Whether to loop or not when the video playback ends.
        """

        if self.is_ready and not self.is_playing:
            self.is_playing = True
            self.is_looped = loop

            self.seek_frame(0)
            self.draw_frame = 0
            self.start_time = time.time()
            self.__start_time = time.time()

            self.__ff.set_pause(False)

    def stop(self) -> None:
        """
        Stop playing the video.
        """

        self.is_playing = False
        self.is_paused = False
        self.__ff.set_pause(True)

    def pause(self) -> None:
        """ Pause the video. """

        if self.is_playing:
            self.is_paused = True
            self.__ff.set_pause(True)

    def resume(self) -> None:
        """ Resume the video. """

        if self.is_playing:
            self.is_paused = False
            self.__ff.set_pause(False)

    def toggle_pause(self) -> None:
        """ Switch between paused states. """

        if self.is_playing:
            if self.is_paused: self.resume()
            else: self.pause()

    # Audio methods

    def mute(self) -> None:
        """ Mute audio playback. """
        # MediaPlayer.set_mute doesn't work!
        self.is_muted = True
        self.__volume_before_mute = self.volume
        self.__ff.set_volume(0.0)

    def unmute(self) -> None:
        """ Unmute audio playback. """
        self.is_muted = False
        self.__ff.set_volume(self.__volume_before_mute)

    @property
    def volume(self) -> float:
        """ Volume of the audio playback. """
        return self.__volume
    
    @volume.setter
    def volume(self, value: float) -> None:
        self.__volume = value
        if not self.is_muted:
            self.__ff.set_volume(value)

    # Duration methods & properties

    @property
    def duration(self) -> float:
        """ Total duration of the video in milliseconds. """
        return (self.total_frames / self.fps) * 1000

    @property
    def current_time(self) -> float:
        """ Current time into the video in milliseconds. """
        if not self.is_ready or not self.is_playing: return 0
        return self.__vidcap.get(cv2.CAP_PROP_POS_MSEC)

    @property
    def remaining_time(self) -> float:
        """ Remaining time left in the video in milliseconds. """
        return self.duration - self.current_time

    @property
    def current_frame(self) -> int:
        """ Current frame into the video. """
        return self.__vidcap.get(cv2.CAP_PROP_POS_FRAMES)

    @property
    def remaining_frames(self) -> int:
        """ Remaining frames left in the video. """
        return self.frame_count - self.current_frame

    def seek_time(self, timepoint: float) -> None:
        """
        Seek into desired timepoint.

        Parameters
        ----------
        @param time Time in milliseconds to seek to.
        """

        self.start_time = self.__start_time + timepoint / 1000
        self.draw_frame = int((time.time() - self.start_time) * self.fps)
        self.__vidcap.set(cv2.CAP_PROP_POS_MSEC, timepoint)
        self.__ff.seek(timepoint / 1000, relative=False)

    def seek_frame(self, frame: int) -> None:
        """
        Seek into desired frame.

        Parameters
        ----------
        @param frame Frame number to seek to.
        """
        self.seek_time((frame / self.fps) * 1000)

    # Process & draw video

    def get_frame(self) -> pygame.Surface:
        """
        Advance the video and return the current frame.
        Must be called once per frame.
        """

        if not self.is_playing or not self.is_ready:
            return self.frame_surf

        elapsed_frames = int((time.time() - self.start_time) * self.fps)

        if self.draw_frame >= elapsed_frames:
            return self.frame_surf

        else:
            target_frames = elapsed_frames - self.draw_frame
            self.draw_frame += target_frames

            if not self.is_paused:
                for _ in range(target_frames):
                    success, frame = self.__vidcap.read()

                    if not success:
                        if self.is_looped:
                            self.seek_frame(0)
                            return self.frame_surf

                        else:
                            self.stop()
                            return self.frame_surf

                pygame.pixelcopy.array_to_surface(
                    self.frame_surf,
                    numpy.flip(numpy.rot90(frame[::-1]))
                )

            return self.frame_surf

    def draw_to(self,
            dest_surface: pygame.Surface,
            position: Union[tuple[float, float], pygame.Vector2, pygame.Rect]
            ) -> None:
        """
        Blit the current video frame to the surface.

        Parameters
        ----------
        @param dest_surface Destination surface to draw the video on.
        @param position Position to draw the video frame at.
        """

        frame = self.get_frame()

        dest_surface.blit(frame, position)
