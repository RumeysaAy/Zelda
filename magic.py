import pygame
from settings import *
from random import randint

class MagicPlayer:
    def __init__(self,animation_player):
        self.animation_player = animation_player
        self.sounds = {
            'heal':pygame.mixer.Sound('audio/heal.wav'),
            'flame':pygame.mixer.Sound('audio/Fire.wav')
        }

    def heal(self,player,guc,zarar,gruplar):
        if player.enerji >= zarar:
            self.sounds['heal'].play()
            player.saglik += guc
            player.enerji -= zarar
            if player.saglik >= player.ozellikler['saglik']:
                player.saglik = player.ozellikler['saglik']
            self.animation_player.create_particles('aura',player.rect.center,gruplar)
            self.animation_player.create_particles('heal',player.rect.center,gruplar)

    def flame(self,player,zarar,gruplar):
        if player.enerji >= zarar:
            player.enerji -= zarar
            self.sounds['flame'].play()

            if player.durumlar.split('_')[0] == 'right':
                yon = pygame.math.Vector2(1,0)
            elif player.durumlar.split('_')[0] == 'left':
                yon = pygame.math.Vector2(-1,0)
            elif player.durumlar.split('_')[0] == 'up':
                yon = pygame.math.Vector2(0,-1)
            else:
                yon = pygame.math.Vector2(0,1)

            
            for i in range(1,6):
                if yon.x: # yatay
                    offest_x = (yon.x * i) * kaya_boyut
                    x = player.rect.centerx + offest_x + randint(-kaya_boyut // 3, kaya_boyut // 3)
                    y = player.rect.centery + randint(-kaya_boyut // 3, kaya_boyut // 3)
                    self.animation_player.create_particles('flame',(x,y),gruplar)
                else: # dikey
                    offest_y = (yon.y * i) * kaya_boyut
                    x = player.rect.centerx + randint(-kaya_boyut // 3, kaya_boyut // 3)
                    y = player.rect.centery + offest_y + randint(-kaya_boyut // 3, kaya_boyut // 3)
                    self.animation_player.create_particles('flame',(x,y),gruplar)