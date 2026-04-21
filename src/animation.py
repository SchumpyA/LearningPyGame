import pygame
import sys
import math
import random

pygame.init()

# -----------------------------
# Screen
# -----------------------------
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# -----------------------------
# World (bottom of screen = floor)
# -----------------------------
FLOOR_Y = HEIGHT

# -----------------------------
# Mouse interaction
# -----------------------------
dragging_ball = None
mouse_offset_x = 0
mouse_offset_y = 0

# -----------------------------
# Planets (gravity wells)
# -----------------------------
planets = [
    {"x": 250, "y": 120, "r": 18, "mass": 6000, "t": 0},
    {"x": 650, "y": 150, "r": 22, "mass": 8000, "t": 1}
]

# -----------------------------
# Balls
# -----------------------------
balls = [
    {
        "name": "rubber",
        "x": 200, "y": 100,
        "vx": 2, "vy": 0,
        "radius": 32,
        "impact": 0,
        "t": 0,
        "gravity": 0.5,
        "bounce": 0.85,
        "metal": False,
        "particles": False,
        "slime": False,
    },
    {
        "name": "metal",
        "x": 450, "y": 100,
        "vx": -2, "vy": 0,
        "radius": 36,
        "impact": 0,
        "t": 0,
        "gravity": 0.5,
        "bounce": 0.35,
        "metal": True,
        "particles": True,
        "slime": False,
    },
    {
        "name": "slime",
        "x": 700, "y": 100,
        "vx": 1, "vy": 0,
        "radius": 42,
        "impact": 0,
        "t": 0,
        "gravity": 0.3,
        "bounce": 0.15,
        "metal": False,
        "particles": False,
        "slime": True,
    }
]

particles = []
ground_slime = []

# -----------------------------
# Helpers
# -----------------------------
def dist(a, b, x, y):
    return math.hypot(a - x, b - y)

def clamp(x, a, b):
    return max(a, min(b, x))

def apply_planet_gravity(ball):
    for p in planets:
        dx = p["x"] - ball["x"]
        dy = p["y"] - ball["y"]
        d2 = dx*dx + dy*dy + 50

        force = p["mass"] / d2

        ball["vx"] += dx * force * 0.01
        ball["vy"] += dy * force * 0.01

# -----------------------------
# Main loop
# -----------------------------
running = True
while running:
    clock.tick(60)

    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in balls:
                if dist(mx, my, b["x"], b["y"]) < b["radius"]:
                    dragging_ball = b
                    mouse_offset_x = b["x"] - mx
                    mouse_offset_y = b["y"] - my
                    break

        if event.type == pygame.MOUSEBUTTONUP:
            dragging_ball = None

    # -----------------------------
    # Trails
    # -----------------------------
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.set_alpha(30)
    fade.fill((0, 0, 0))
    screen.blit(fade, (0, 0))

    # -----------------------------
    # Move planets
    # -----------------------------
    for p in planets:
        p["t"] += 0.01
        p["x"] += math.sin(p["t"]) * 0.3

    # -----------------------------
    # Update balls
    # -----------------------------
    for b in balls:

        # -------------------------
        # Dragging
        # -------------------------
        if b == dragging_ball:
            prev_x, prev_y = b["x"], b["y"]

            b["x"] = mx + mouse_offset_x
            b["y"] = my + mouse_offset_y

            b["vx"] = (b["x"] - prev_x) * 0.6
            b["vy"] = (b["y"] - prev_y) * 0.6

            continue

        # -------------------------
        # Physics
        # -------------------------
        b["vy"] += b["gravity"]
        apply_planet_gravity(b)

        b["x"] += b["vx"]
        b["y"] += b["vy"]

        b["vx"] *= 0.999
        b["vy"] *= 0.999

        b["vx"] += random.uniform(-0.01, 0.01)

        # -------------------------
        # Walls
        # -------------------------
        if b["x"] - b["radius"] <= 0:
            b["x"] = b["radius"]
            b["vx"] *= -1

        if b["x"] + b["radius"] >= WIDTH:
            b["x"] = WIDTH - b["radius"]
            b["vx"] *= -1

        # -------------------------
        # FLOOR = bottom of screen
        # -------------------------
        if b["y"] + b["radius"] >= FLOOR_Y:
            b["y"] = FLOOR_Y - b["radius"]

            impact = abs(b["vy"])
            b["impact"] = impact

            if b["particles"] and impact > 2:
                for _ in range(8):
                    particles.append([
                        b["x"], b["y"],
                        random.uniform(-3, 3),
                        random.uniform(-6, -2)
                    ])

            if b["slime"]:
                ground_slime.append((b["x"], FLOOR_Y - 2))

            b["vy"] *= -b["bounce"]

            if abs(b["vy"]) < 0.5:
                b["vy"] = 0

        b["impact"] *= 0.85
        b["t"] += 0.03

    # -----------------------------
    # Particles
    # -----------------------------
    for p in particles:
        p[0] += p[2]
        p[1] += p[3]
        p[3] += 0.2

    particles = [p for p in particles if p[1] < HEIGHT]

    # -----------------------------
    # Draw planets
    # -----------------------------
    for p in planets:
        pygame.draw.circle(screen, (80, 120, 255), (int(p["x"]), int(p["y"])), p["r"])

    # -----------------------------
    # slime ground trail
    # -----------------------------
    for s in ground_slime[-400:]:
        pygame.draw.circle(screen, (80, 200, 140), (int(s[0]), int(s[1])), 3)

    # -----------------------------
    # Draw balls
    # -----------------------------
    for b in balls:

        stretch = min(b["impact"] * 0.03, 0.35)

        w = int(b["radius"] * (1 + stretch))
        h = int(b["radius"] * (1 - stretch))

        if b["metal"]:
            speed = abs(b["vx"]) + abs(b["vy"])
            shade = clamp(120 + int(speed * 4), 80, 255)
            col = (shade, shade, shade)

        elif b["slime"]:
            col = (
                int(120 + 80 * math.sin(b["t"])),
                220,
                140
            )
        else:
            col = (
                int(127 + 127 * math.sin(b["t"])),
                80,
                int(127 + 127 * math.cos(b["t"]))
            )

        pygame.draw.ellipse(
            screen,
            col,
            (int(b["x"] - w//2), int(b["y"] - h//2), w, h)
        )

    # -----------------------------
    # particles
    # -----------------------------
    for p in particles:
        pygame.draw.circle(screen, (200, 200, 200), (int(p[0]), int(p[1])), 3)

    pygame.display.flip()

pygame.quit()
sys.exit()