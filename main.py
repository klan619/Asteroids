import pygame
import sys
import os
from constants import *
from logger import log_state
from player import Player
from asteroidfield import AsteroidField
from asteroid import Asteroid
from logger import log_event
from shot import Shot

state = "MENU"

def main():

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()

    timer = pygame.time.Clock()

    dt = 0

    score = 0

    lives = 3

    HIGHSCORE_FILE = "highscore.txt"

    def load_high_score():
        if not os.path.exists(HIGHSCORE_FILE):
            return 0
        with open(HIGHSCORE_FILE, "r") as f:
            try:
                return int(f.read())
            except ValueError:
                return 0
            
    def save_high_score(new_high_score):
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(new_high_score))


    high_score = load_high_score()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.font.init()
    font = pygame.font.SysFont("monospace", 35)


    def draw_menu():
        screen.fill((0, 0, 0))
        title_surf = font.render("ASTEROIDS", True, (255, 255, 255))
        high_score_surf = font.render(f"High Score: {high_score}", True, (255, 215, 0))
        start_surf = font.render("Press 'Enter' to Start", True, (0, 255, 0))
        exit_surf = font.render("Press 'Escape' to Quit", True, (255, 0, 0))
        screen.blit(title_surf, (SCREEN_WIDTH/2 - title_surf.get_width()/2, 150))
        screen.blit(high_score_surf, (SCREEN_WIDTH/2 - high_score_surf.get_width()/2, 250))
        screen.blit(start_surf, (SCREEN_WIDTH/2 - start_surf.get_width()/2, 400))
        screen.blit(exit_surf, (SCREEN_WIDTH/2 - exit_surf.get_width()/2, 450))
        controls = [
            "",
            "CONTROLS:",
            "Rotate: A / D   OR   Left & Right Arrow Keys",
            "Thrust: W / S   OR   Up & Down Arrow Keys",
            "Shoot: Space",
        ]

        for i, line in enumerate(controls):
            ctrl_surf = font.render(line, True, (200, 200, 200))
            x = SCREEN_WIDTH/2 - ctrl_surf.get_width()/2
            y = 500 + (i * 50) 
            screen.blit(ctrl_surf, (x, y))

        pygame.display.flip()

    def handle_menu_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    global state
                    state = "GAME"
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()

    def reset_game():
        nonlocal score, lives, player
        global state

        score = 0

        lives = 3

        for sprite in updatable:
            sprite.kill()

        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        AsteroidField()

        state = "MENU"
    
    
    while True:

        dt = timer.tick(60) / 1000

        if state == "MENU":
            handle_menu_events()
            draw_menu()
            continue
        elif state == "GAME":

            log_state()
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_high_score(high_score)
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        save_high_score(high_score)
                        reset_game()
        
            screen.fill("black")

            updatable.update(dt)

            for obj in asteroids:
                if player.collides_with(obj):
                    log_event("player_hit")
                    if lives > 1:
                        lives -= 1
                        player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                        player.velocity = pygame.Vector2(0, 0)
                        for a in asteroids:
                            a.kill()

                    else:
                        save_high_score(high_score)
                        reset_game()

            for asteroid in asteroids:
                for shot in shots:
                    if shot.collides_with(asteroid):
                        log_event("asteroid_shot")
                        if asteroid.radius <= ASTEROID_MIN_RADIUS:
                            score += 250
                        else:
                            score += 100
                        if score > high_score:
                            high_score = score

                        asteroid.split()
                        shot.kill()

            

            for thing in drawable:
                thing.draw(screen)
                score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
                screen.blit(score_surface, (10, 10))
                lives_surface = font.render(f"Lives: {lives}", True, (255, 255, 255))
                screen.blit(lives_surface, (10, 50))
                high_score_surface = font.render(f"High Score: {high_score}", True, (255, 215, 0))
                x_pos = SCREEN_WIDTH - high_score_surface.get_width() - 10
                screen.blit(high_score_surface, (x_pos, 10))


            pygame.display.flip()
        

if __name__ == "__main__":
    main()
