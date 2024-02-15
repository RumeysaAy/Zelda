import pygame

class Silah(pygame.sprite.Sprite):
    def __init__(self, player, gruplar):
        super().__init__(gruplar)
        self.sprite_type = 'silah'
        yon = player.durumlar.split('_')[0] # left_idle -> left, idle

        # resimler
        full_path = f'resimler/weapons/{player.silah}/{yon}.png'
        self.image = pygame.image.load(full_path).convert_alpha()
        
        # silahi yerlestirme: oyuncunun yonune gore silah tutulacak
        if yon == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))
            # oyuncunun orta-sag konumu = silahin sol-orta konumu + 0,16 (y ekseninde 16 piksel asagi indirdim)
        elif yon == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16))
        elif yon == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,0))
            # silahi sola dogru 10 piksel kaydirdim
        else:
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10,0))