from time import perf_counter
from datetime import timedelta

import pygame

from pygamevideo import Video


pygame.init()
window = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

font18 = pygame.font.SysFont("Arial", 18)
font14 = pygame.font.SysFont("Arial", 14)


start = perf_counter()
video = Video("bunny.mp4")
elapsed = perf_counter() - start

video.play(loop=True)


titlebar_surf = pygame.Surface((1280, 35)).convert()
titlebar_surf.set_alpha(180)

control_surf = pygame.Surface((1280, 50)).convert()
control_surf.set_alpha(180)

pygame.draw.rect(control_surf, (100, 100, 100), (153, 22, 1100, 4), 0)


while True:
    clock.tick(0)
    pygame.display.set_caption(f"Pygame Video Player @{round(clock.get_fps())}FPS")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit(0)

    window.fill((25, 18, 41))

    video.draw_to(window, (0, 0))

    t = timedelta(milliseconds=video.current_time)
    h, rem = divmod(t.seconds, 3600)
    m, s = divmod(rem, 60)
    time_formatted = f"{str(h).zfill(2)}:{str(m).zfill(2)}:{str(s).zfill(2)}"

    t = timedelta(milliseconds=video.duration)
    h, rem = divmod(t.seconds, 3600)
    m, s = divmod(rem, 60)
    total_time = f"{str(h).zfill(2)}:{str(m).zfill(2)}:{str(s).zfill(2)}"

    window.blit(titlebar_surf, (0, 0))
    window.blit(font18.render(f"{video.filepath}     {round(video.fps, 2)}FPS     {video.total_frames} frames     {video.frame_width}x{video.frame_height}     Loaded in {round(elapsed * 1000, 1)}ms", True, (255, 255, 255)), (10, 7))

    window.blit(control_surf, (0, 720 - 50))
    window.blit(font14.render(f"{time_formatted} / {total_time}", True, (255, 255, 255)), (5, 720 - 32))

    percentage = video.current_frame / video.total_frames
    x = percentage * 1100

    pygame.draw.rect(window, (156, 135, 250), (153, 720 - 50 + 22, x, 4), 0)

    pygame.draw.circle(window, (255, 255, 255), (153 + x, 720 - 50 + 24), 7, 0)

    pygame.display.flip()