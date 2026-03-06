import pygame
import json
import sys

IMAGE_PATH = "spritesheet.png"
JSON_PATH = "frames.json"
SCALE = 3
FPS = 10

pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()

with open(JSON_PATH, "r") as f:
    data = json.load(f)

sheet = pygame.image.load(IMAGE_PATH).convert_alpha()

groups = list(data.keys())
group_index = 0
frame_index = 0
frames = data[groups[group_index]]

def get_frame(frame):
    rect = pygame.Rect(frame["x"], frame["y"], frame["w"], frame["h"])
    img = pygame.Surface((frame["w"], frame["h"]), pygame.SRCALPHA)
    img.blit(sheet, (0, 0), rect)
    img = pygame.transform.scale(img, (frame["w"]*SCALE, frame["h"]*SCALE))
    return img

timer = 0

running = True
while running:
    dt = clock.tick(60)
    timer += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                group_index = (group_index + 1) % len(groups)
                frames = data[groups[group_index]]
                frame_index = 0
            if event.key == pygame.K_LEFT:
                group_index = (group_index - 1) % len(groups)
                frames = data[groups[group_index]]
                frame_index = 0

    if timer > 1000 // FPS:
        frame_index = (frame_index + 1) % len(frames)
        timer = 0

    frame = get_frame(frames[frame_index])

    screen.fill((30, 30, 30))
    rect = frame.get_rect(center=(200, 150))
    screen.blit(frame, rect)

    pygame.display.set_caption(f"Animation: {groups[group_index]}  Frame: {frame_index}")
    pygame.display.flip()

pygame.quit()
sys.exit()