import sys, pygame
from settings import *
from debug import debug
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.pencere = pygame.display.set_mode((genislik,yukseklik))
        pygame.display.set_caption('Zelda')
        self.clock = pygame.time.Clock()
        self.level = Level()

        # sound
        main_sound = pygame.mixer.Sound('audio/main.ogg')
        main_sound.set_volume(0.5)
        main_sound.play(loops = -1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()
            
            self.pencere.fill(su_renk)
            self.level.run()
            pygame.display.update()
            self.clock.tick(fps)

if __name__ == '__main__':
    game = Game()
    game.run()