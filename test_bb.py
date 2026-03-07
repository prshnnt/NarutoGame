import pygame
import json
import sys

IMAGE_PATH = "assets/images/Naruto.png"
JSON_PATH = "assets/bounding_box/naruto.json"
SCALE = 3
FPS = 10

pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()

with open(JSON_PATH, "r") as f:
    data = json.load(f)

sheet = pygame.image.load(IMAGE_PATH).convert_alpha()

groups = list(data.keys())
group_index = 10 # till g5 done !
frame_index = 0
frames = data[groups[group_index]]

def get_frame(frame):
    rect = pygame.Rect(frame["x"], frame["y"], frame["w"], frame["h"])
    img = pygame.Surface((frame["w"], frame["h"]), pygame.SRCALPHA)
    img.set_colorkey((0,64,128))
    img.blit(sheet, (0, 0), rect)
    img = img.convert_alpha(img)
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
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_RIGHT:
                group_index = (group_index + 1) % len(groups)
                frames = data[groups[group_index]]
                frame_index = 0
            if event.key == pygame.K_LEFT:
                group_index = (group_index - 1) % len(groups)
                frames = data[groups[group_index]]
                frame_index = 0

    if timer > 5000 // FPS:
        frame_index = (frame_index + 1) % len(frames)
        timer = 0

    frame = get_frame(frames[frame_index])

    screen.fill((30, 30, 30))
    rect = frame.get_rect()
    screen.blit(frame, rect)

    pygame.display.set_caption(f"Animation: {groups[group_index]}  Frame: {frame_index}")
    pygame.display.flip()

pygame.quit()
sys.exit()