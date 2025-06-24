import pygame 
import sqlite3
import random
import time

# --- SQLite Setup ---
conn = sqlite3.connect('highscores.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    score INTEGER,
    timestamp TEXT
)
''')
conn.commit()

# --- Pygame Setup ---
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kreise Klickspiel")

# Farben
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Spielvariablen
circle_radius = 30
circle_pos = [random.randint(circle_radius, WIDTH - circle_radius), random.randint(circle_radius, HEIGHT - circle_radius)]
score = 0
font = pygame.font.SysFont(None, 36)
game_time = 30  # Sekunden
start_ticks = pygame.time.get_ticks()  # Startzeit

running = True
game_over = False

def save_score(score):
    cursor.execute('INSERT INTO scores (score, timestamp) VALUES (?, datetime("now"))', (score,))
    conn.commit()

def draw_text(text, x, y):
    img = font.render(text, True, WHITE)
    screen.blit(img, (x, y))

while running:
    screen.fill(BLACK)
   
    seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
    time_left = max(0, int(game_time - seconds_passed))
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
       
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mx, my = pygame.mouse.get_pos()
            dist = ((mx - circle_pos[0]) ** 2 + (my - circle_pos[1]) ** 2) ** 0.5
            if dist <= circle_radius:
                score += 1
                # Neuer Kreis an neuer Position
                circle_pos = [random.randint(circle_radius, WIDTH - circle_radius), random.randint(circle_radius, HEIGHT - circle_radius)]
   
    if not game_over:
        pygame.draw.circle(screen, RED, circle_pos, circle_radius)
        draw_text(f"Punkte: {score}", 10, 10)
        draw_text(f"Zeit: {time_left}s", 10, 50)
       
        if time_left <= 0:
            game_over = True
            save_score(score)
   
    else:
        draw_text("Spiel vorbei!", WIDTH//2 - 80, HEIGHT//2 - 30)
        draw_text(f"Dein Score: {score}", WIDTH//2 - 80, HEIGHT//2)
        draw_text("Fenster schließen zum Beenden", WIDTH//2 - 140, HEIGHT//2 + 30)
   
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
conn.close()