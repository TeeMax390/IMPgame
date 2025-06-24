# --- Module importieren ---
import pygame                     # Für das Spiel und die Grafiken
import sqlite3                    # Für die Speicherung der Highscores
import random                     # Für zufällige Kreispositionen
import time                       # (optional) Wird hier aber nicht direkt verwendet

# --- SQLite-Datenbank Setup ---
conn = sqlite3.connect('highscores.db')     # Verbindung zur Datenbank herstellen (Datei wird erstellt, falls nicht vorhanden)
cursor = conn.cursor()                      # Cursor-Objekt zum Ausführen von SQL-Befehlen

# Tabelle für Scores erstellen, falls sie noch nicht existiert
cursor.execute('''
CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,   # Automatisch erhöhte ID
    score INTEGER,                          # Punktzahl
    timestamp TEXT                          # Zeitpunkt des Scores
)
''')
conn.commit()  # Änderungen in der Datenbank speichern

# --- Pygame Setup ---
pygame.init()                                   # Pygame initialisieren
WIDTH, HEIGHT = 600, 400                        # Fenstergröße
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Fenster erstellen
pygame.display.set_caption("Kreise Klickspiel") # Fenstertitel

# Farben definieren (RGB)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# --- Spielvariablen ---
circle_radius = 30  # Radius des Kreises
circle_pos = [random.randint(circle_radius, WIDTH - circle_radius), 
              random.randint(circle_radius, HEIGHT - circle_radius)]  # Zufällige Startposition des Kreises

score = 0                                # Punktestand
font = pygame.font.SysFont(None, 36)     # Schriftart für den Text
game_time = 30                           # Gesamte Spielzeit in Sekunden
start_ticks = pygame.time.get_ticks()    # Startzeit (Millisekunden seit Spielstart)

running = True      # Haupt-Spielschleifen-Flag
game_over = False   # Status: Spiel vorbei?

# --- Funktion: Score in Datenbank speichern ---
def save_score(score):
    cursor.execute('INSERT INTO scores (score, timestamp) VALUES (?, datetime("now"))', (score,))
    conn.commit()

# --- Funktion: Text auf den Bildschirm zeichnen ---
def draw_text(text, x, y):
    img = font.render(text, True, WHITE)  # Text rendern
    screen.blit(img, (x, y))              # Text auf Bildschirm zeichnen

# --- Hauptspiel-Schleife ---
while running:
    screen.fill(BLACK)  # Bildschirm schwarz füllen (Hintergrund)

    # Zeitberechnung: vergangene Sekunden
    seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
    time_left = max(0, int(game_time - seconds_passed))  # Restzeit berechnen (max 0, kein Minus)

    # Ereignisse (Events) auslesen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Wenn das Fenster geschlossen wird
            running = False

        # Wenn die Maus geklickt wurde und das Spiel noch läuft
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mx, my = pygame.mouse.get_pos()  # Mausposition holen
            # Entfernung zwischen Klickpunkt und Mittelpunkt des Kreises berechnen
            dist = ((mx - circle_pos[0]) ** 2 + (my - circle_pos[1]) ** 2) ** 0.5
            if dist <= circle_radius:
                score += 1  # Punktzahl erhöhen
                # Kreis an neue zufällige Position verschieben
                circle_pos = [random.randint(circle_radius, WIDTH - circle_radius),
                              random.randint(circle_radius, HEIGHT - circle_radius)]

    # Wenn das Spiel noch läuft
    if not game_over:
        # Kreis zeichnen
        pygame.draw.circle(screen, RED, circle_pos, circle_radius)
        # Punktestand und Zeit anzeigen
        draw_text(f"Punkte: {score}", 10, 10)
        draw_text(f"Zeit: {time_left}s", 10, 50)

        # Wenn die Zeit abgelaufen ist, Spiel beenden
        if time_left <= 0:
            game_over = True
            save_score(score)  # Punktzahl speichern

    # Wenn das Spiel vorbei ist
    else:
        # Texte anzeigen
        draw_text("Spiel vorbei!", WIDTH//2 - 80, HEIGHT//2 - 30)
        draw_text(f"Dein Score: {score}", WIDTH//2 - 80, HEIGHT//2)
        draw_text("Fenster schließen zum Beenden", WIDTH//2 - 140, HEIGHT//2 + 30)

    pygame.display.flip()         # Bildschirm aktualisieren
    pygame.time.Clock().tick(60)  # Frame-Rate auf 60 FPS begrenzen

# --- Nach dem Spiel ---
pygame.quit()     # Pygame beenden
conn.close()      # Datenbankverbindung schließen