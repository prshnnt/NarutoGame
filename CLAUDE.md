# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

2D platformer / fighter inspired by Naruto. Pygame (`pygame-ce`) on Python 3.12. No test framework, no linter, no build step. Single entrypoint: `main.py`.

## Run

```bash
.venv/Scripts/python main.py        # Windows
# or with uv:
uv run main.py
```

`test_bb.py` is a standalone sprite-sheet viewer (run directly), not a test file.

## Dependencies

Managed by `uv` (`uv.lock`, `pyproject.toml`). Runtime deps: `pygame-ce`, `pydantic`, `bs4`, `httpx`, `requests`, `colorama`. Install with `uv sync`.

## High-level Architecture

Custom entity-component-style layer system. No ECS framework — hand-rolled with abstract base classes and inheritance.

### Game loop (`main.py`)

`Game` holds a `dict[MainScenes, BaseScene]`, an `action` dict (booleans for each input), and a `Clock`. Each frame: `handle_events` translates pygame events into the `action` dict → `active_scene.handle_action(action)` → `update(dt)` → `draw()`.

### Scenes (`Scenes/`)

`BaseScene` owns a `layers` dict — `background`, `world`, `effects`, `ui` — each a list of `GameObject`. Update/draw/handle_action iterate layers in fixed order. Concrete scenes: `MenuScene`, `OptionScene`, `GameScene`. Scene switching via `Game.change_scene()` which calls `on_exit`/`on_enter`.

### Core (`core/`)

- `config.py` — single source of constants: window size (960x500), FPS (60), physics (GRAVITY, JUMP_FORCE, RUN_SPEED, PLAYER_SPEED), `TILE_SIZE`, `MainScenes` enum, `ALLOWED_KEYS`, color palette, `width_percent`/`height_percent` helpers.
- `AssetLoader.py` — JSON-driven level/player loading. `load_level` builds parallax background + tiled ground from `assets/levels/level1.json`. `load_player` reads `assets/player/naruto.json` (sprite path + bounding box) and instantiates the player. **Hardcoded scale `{x:2.2, y:2.2}` lives in `load_player` — see comment, should move to JSON.**
- `Camera.py` — centers on target X/Y, clamps to world bounds. `apply(rect)` translates world coords to screen (X-only currently).
- `GameObject.py` — ABC with `rect`, `image`, `update(scene)`, `draw(scene)`, `handle_action(action)`.
- `SpriteSheetLoader.py` — module-level functions (note: `AssetLoader` has its own copies; this module appears unused by the main game).

### Entities (`entities/`)

`Entity` (ABC) → `Player`, `Enemy`. Shared: `position`, `velocity`, `rect`, `health=100`, `invincible`, `alive`, `facing` (1 right / -1 left), `in_air`, `attack_hitbox`, `attack_damage=10`, `hitbox_duration=200ms`, state machine dict.

- `Entity.collide_with_platforms(platforms)` — axis-separated AABB resolution (X then Y). Sets `in_air=False` on landing.
- `Entity.create_hitbox(w, h, offset_x)` — places hitbox in front of entity based on `facing`. Expires via `update_hitbox(dt)`.
- `Entity.check_hit(target)` — AABB intersection between own hitbox and target rect.
- `Entity.take_damage(amount)` — only if not invincible and alive; sets `alive=False` at 0 HP. **No death state transition wired up yet.**

`Player` adds: `is_gaurding` (sic), `attack_queue: list[str]` (max 2, FIFO), state names `idle/run/jump/fall/guard/landing/hit/b/b_forward/b_up/b_down/y/y_forward`. `handle_input` queues attacks while in attack state, otherwise transitions immediately. `on_hit_interrupt()` clears queue → `hit` state. `is_in_attack_state()` matches by class name.

`Enemy` adds: AI state with `aggro_range=300`, `attack_range=50`, `is_attacking` flag, `attack_damage=10`. `set_target(player)` → `update_ai` runs on a randomized timer (0.5–2.0s) and feeds synthetic actions into `handle_input`. Currently has only `b` attack in its state dict; no Y-attack, no hit reaction state.

### States (`States/`)

`BaseState` with `enter/exit/handle_action/update`. Concrete: `IdleState`, `RunState`, `JumpState`, `FallState`, `GuardState`, `LandingState`, `HitState`, plus the six attack states in `BAttackState.py` (`BAttackState`, `BForwardState`, `BUpState`, `BDownState`, `YAttackState`, `YForwardState`).

`DeadState.py` and `DownState.py` exist on disk but are not exported in `States/__init__.py`.

Attack-state pattern: `enter` plays the animation group and calls `create_hitbox(...)`; `update` checks `animator.animation_finished` — if a queue exists, calls `process_next_attack()`, else `change_state("idle")`. Y-attack states set `attack_damage=20` on enter and reset to 10 on finish.

### Animator (`Animator/`)

`Base.Animator` holds `frames: dict[group_name, list[Surface]]`, `frame_index`, `prev_time`, `animation_finished` flag. `play(group)` switches group and resets index. `update_frame()` default loops index; `animation_finished` is set when wrapping. `draw()` flips horizontally when `player.facing == -1`.

`NarutoAnimator` overrides `should_update_frame` to 150ms cadence and `update_frame` for per-group behavior: `jump/fall/landing` freeze on frame 0, `guard` steps 0→1→2, attack groups (`b/b_forward/b_up/b_down/y/y_forward`) play once and clamp on the last frame (sets `animation_finished=True`).

**Note:** `Base.Animator.draw(scene)` exists but `NarutoAnimator.update` does not call draw — the player `Entity.draw` delegates to `self.animator.draw(scene)`, but `NarutoAnimator` doesn't override `draw`. The base `draw` is used; verify when adding visuals.

### Components (`Components/`)

UI/world renderers implementing `GameObject`: `Button` (hover + click callback, optional `choice` toggle), `Text`, `ParallaxBackground` (X-tile based on `camera.rect.x * speed`), `Ground` (tile, uses random of 3 sections from source image when given).

## Combat Flow (current)

1. `GameScene.update` ticks player and enemies.
2. `Entity.update` calls `state.update`, resolves collisions, ticks hitbox timer.
3. Attack state creates hitbox on enter. While alive, hitbox collides with targets.
4. `GameScene.update` runs two loops: enemy hits player (one hit per attack — hitbox nulled on contact), player hits each enemy (one hit per attack).
5. If player is mid-attack when hit, `on_hit_interrupt()` clears queue and transitions to `hit` state.

## Known Incomplete Work (from prior session memory)

- Enemy attack visuals / state expansion (only `b` in enemy state dict).
- Hitbox-vs-target resolution for multi-hit attack sequences (currently nulled after first contact).
- `DeadState` not wired up — `take_damage` flips `alive=False` but no state transition.
- Hardcoded player scale `2.2` in `AssetLoader.load_player`.

## Conventions

- States use `enter/exit/handle_action/update` — keep that signature.
- Attack states **must** end via `animator.animation_finished` check in `update`, not via input.
- Player-only logic (e.g. `attack_queue`) should be guarded with `hasattr` when called from a base class context (see `BAttackState`).
- New scenes: subclass `BaseScene`, populate layers in `on_enter`.
- New entities: subclass `Entity`, define `change_state` and `handle_input`.
- Spell-check: `is_gaurding` is intentional in code; don't silently rename.
