import array
import math
import pygame
from .player import Player
from .platform import Platform
from .hazard import Hazard

# Game Engine

WHITE = (255, 255, 255)
BROWN = (150, 100, 60)
RED = (220, 60, 60)
GREEN = (0, 200, 0)

# Each difficulty changes gravity, jump strength and the level layout.
# (All three were checked to be beatable.)
DIFFICULTIES = {
    "easy":   {"gravity": 0.5, "jump": -13, "gap": 40, "hazard_w": 70},
    "medium": {"gravity": 0.6, "jump": -12, "gap": 60, "hazard_w": 100},
    "hard":   {"gravity": 0.7, "jump": -12, "gap": 80, "hazard_w": 100},
}


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.max_fall_speed = 15

        self.start_x, self.start_y = 40, height - 120
        self.player = Player(self.start_x, self.start_y)

        self.font = pygame.font.SysFont("Arial", 30)
        self.big_font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 32)
        self.load_sounds()

        self.difficulty = "medium"
        self.reset("medium")

    # ------------------------------------------------------------------
    # Sound
    # ------------------------------------------------------------------
    def make_sweep(self, f0, f1, duration, volume=0.3):
        """Generate a tone that slides from f0 Hz to f1 Hz."""
        freq, _, channels = pygame.mixer.get_init()
        n = int(freq * duration)
        buf = array.array("h")          # 16-bit signed samples
        phase = 0.0
        for i in range(n):
            t = i / n
            phase += 2 * math.pi * (f0 + (f1 - f0) * t) / freq
            sample = int(32767 * volume * (1 - t) * math.sin(phase))
            for _ in range(channels):
                buf.append(sample)
        return pygame.mixer.Sound(buffer=buf.tobytes())

    def load_sounds(self):
        self.sounds = {}
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.sounds["jump"] = self.make_sweep(300, 650, 0.15)
            self.sounds["goal"] = self.make_sweep(600, 1300, 0.35)
            self.sounds["die"] = self.make_sweep(450, 80, 0.5)
        except pygame.error:
            self.sounds = {}    # no audio device: the game just runs silently

    def play(self, name):
        sound = self.sounds.get(name)
        if sound:
            sound.play()

    # ------------------------------------------------------------------
    # Level / state setup
    # ------------------------------------------------------------------
    def build_level(self):
        cfg = DIFFICULTIES[self.difficulty]
        gap = cfg["gap"]
        self.gravity = cfg["gravity"]
        self.player.jump_strength = cfg["jump"]
        ground_y = self.height - 40

        p2_x = 160 + gap
        p3_x = p2_x + 140 + gap
        p4_x = p3_x + 120 + gap

        self.platforms = [
            Platform(0, ground_y, 160),
            Platform(p2_x, ground_y, 140),
            Platform(p3_x, ground_y - 60, 120),
            Platform(p4_x, ground_y, self.width - p4_x),
        ]
        self.hazards = [Hazard(p2_x + 20, ground_y - 14, cfg["hazard_w"])]
        self.goal_x = self.width - 60

    def reset(self, difficulty=None):
        if difficulty is not None:
            self.difficulty = difficulty
        self.build_level()
        self.player.x, self.player.y = self.start_x, self.start_y
        self.player.vx = 0
        self.player.vy = 0
        self.player.on_ground = False
        self.score = 0
        self.game_over = False

    def end_game(self):
        if not self.game_over:      # guard so the sound only plays once
            self.game_over = True
            self.play("die")

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------
    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        # ESC always exits (posts QUIT so the main loop closes normally)
        if event.key == pygame.K_ESCAPE:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            return

        # Game over screen: pick a difficulty to play again
        if self.game_over:
            if event.key == pygame.K_1:
                self.reset("easy")
            elif event.key == pygame.K_2:
                self.reset("medium")
            elif event.key == pygame.K_3:
                self.reset("hard")
            elif event.key == pygame.K_r:
                self.reset()          # same difficulty
            return

        if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
            if self.player.jump():    # True only on a real jump
                self.play("jump")

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.player.vx = 0
        if self.game_over:
            return
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.vx = -self.player.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.vx = self.player.speed

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------
    def update(self):
        if self.game_over:
            return

        # --- Movement ---
        self.player.vy = min(self.player.vy + self.gravity, self.max_fall_speed)
        self.player.x = max(0, self.player.x + self.player.vx)

        prev_bottom = self.player.y + self.player.height   # feet before moving
        self.player.y += self.player.vy
        new_bottom = self.player.y + self.player.height    # feet after moving
        self.player.on_ground = False

        # --- Platform collision (swept check, works at any fall speed) ---
        if self.player.vy >= 0:
            landing = None
            for platform in self.platforms:
                overlaps_x = (self.player.x < platform.x + platform.width and
                              self.player.x + self.player.width > platform.x)
                crossed_top = prev_bottom <= platform.y <= new_bottom

                if overlaps_x and crossed_top:
                    # If several were crossed this frame, take the highest one
                    if landing is None or platform.y < landing.y:
                        landing = platform

            if landing:
                self.player.y = landing.y - self.player.height
                self.player.vy = 0
                self.player.on_ground = True

        # --- Hazards ---
        for hazard in self.hazards:
            if self.player.rect().colliderect(hazard.rect()):
                self.end_game()
                return

        # --- Fell off the bottom ---
        if self.player.y > self.height:
            self.end_game()
            return

        # --- Goal ---
        if self.player.x >= self.goal_x:
            self.score += 1
            self.play("goal")
            self.player.x, self.player.y = self.start_x, self.start_y
            self.player.vy = 0

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------
    def render(self, screen):
        for platform in self.platforms:
            pygame.draw.rect(screen, BROWN, platform.rect())
        for hazard in self.hazards:
            pygame.draw.rect(screen, RED, hazard.rect())

        goal_rect = pygame.Rect(self.goal_x, 0, 6, self.height)
        pygame.draw.rect(screen, GREEN, goal_rect)

        pygame.draw.rect(screen, WHITE, self.player.rect())

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        diff_text = self.small_font.render(self.difficulty.upper(), True, WHITE)
        screen.blit(diff_text, (10, 45))

        if self.game_over:
            self.render_game_over(screen)

    def render_game_over(self, screen):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        cx, cy = self.width // 2, self.height // 2

        title = self.big_font.render("GAME OVER", True, (255, 60, 60))
        screen.blit(title, title.get_rect(center=(cx, cy - 90)))

        score = self.small_font.render(f"Final Score: {self.score}", True, WHITE)
        screen.blit(score, score.get_rect(center=(cx, cy - 40)))

        lines = [
            "Play again:",
            "1 - Easy     2 - Medium     3 - Hard",
            "R - Same difficulty     Esc - Exit",
        ]
        for i, line in enumerate(lines):
            surf = self.small_font.render(line, True, WHITE)
            screen.blit(surf, surf.get_rect(center=(cx, cy + 10 + i * 36)))