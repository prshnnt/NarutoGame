import pygame as pg


class Animator:
    """
    Handles frame-by-frame animation from a sprite sheet.
    Uses bounding box data loaded from a JSON file (like naruto.json).

    Expected bbox_data format:
    {
        "stance": [{"id": 0, "x": 8, "y": 25, "w": 34, "h": 50}, ...],
        "run":    [...],
        ...
    }
    """

    def __init__(self, sprite_sheet: pg.Surface, bbox_data: dict, fps: int = 10):
        self.sheet = sprite_sheet
        self.bbox_data = bbox_data  # {"animation_name": [frame_dicts]}
        self.fps = fps

        self.current_anim = None
        self.frames: list[pg.Surface] = []
        self.frame_index = 0
        self.timer = 0.0
        self.looping = True
        self.done = False  # True when a non-looping animation has finished
        self.facing = 1    # 1 = right, -1 = left (for flipping)

        # Cache extracted frames per animation
        self._frame_cache: dict[str, list[pg.Surface]] = {}

    def _extract_frames(self, anim_name: str) -> list[pg.Surface]:
        """Extract and cache frames for an animation."""
        if anim_name in self._frame_cache:
            return self._frame_cache[anim_name]

        frames = []
        for frame_data in self.bbox_data.get(anim_name, []):
            x, y, w, h = frame_data["x"], frame_data["y"], frame_data["w"], frame_data["h"]
            surface = pg.Surface((w, h), pg.SRCALPHA)
            surface.blit(self.sheet, (0, 0), (x, y, w, h))
            frames.append(surface)

        self._frame_cache[anim_name] = frames
        return frames

    def play(self, anim_name: str, loop: bool = True, reset: bool = True):
        """Switch to a new animation. If already playing it, does nothing unless reset=True."""
        if self.current_anim == anim_name and not reset:
            return

        self.current_anim = anim_name
        self.frames = self._extract_frames(anim_name)
        self.looping = loop
        self.done = False

        if reset:
            self.frame_index = 0
            self.timer = 0.0

    def set_frame(self, index: int):
        """Jump to a specific frame. Supports negative indices (e.g. -1 for last frame)."""
        if self.frames:
            self.frame_index = index % len(self.frames)

    def update(self, dt: float):
        """Advance animation timer and update frame index."""
        if not self.frames or self.done:
            return

        self.timer += dt
        frame_duration = 1.0 / self.fps

        if self.timer >= frame_duration:
            self.timer -= frame_duration
            self.frame_index += 1

            if self.frame_index >= len(self.frames):
                if self.looping:
                    self.frame_index = 0
                else:
                    self.frame_index = len(self.frames) - 1
                    self.done = True

    def draw(self, screen: pg.Surface, x: int, y: int):
        """Draw the current frame at (x, y), flipped based on facing direction."""
        if not self.frames:
            return

        frame = self.frames[self.frame_index]

        if self.facing == -1:
            frame = pg.transform.flip(frame, True, False)

        screen.blit(frame, (x, y))

    def get_current_frame_size(self) -> tuple[int, int]:
        """Returns (width, height) of current frame, useful for rect updates."""
        if self.frames:
            f = self.frames[self.frame_index]
            return f.get_width(), f.get_height()
        return (0, 0)