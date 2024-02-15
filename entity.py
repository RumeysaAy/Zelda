import pygame
from math import sin 

class Entity(pygame.sprite.Sprite):
    def __init__(self, gruplar):
        super().__init__(gruplar)
        self.frame_index = 0
        self.animation_hiz = 0.15
        self.yon = pygame.math.Vector2()


    def move(self,hiz):
        # magnuitude(): vektorun uzunlugunu geri donderir
        if self.yon.magnitude() != 0:
            # Bir vektörün aynı yöndeki birim vektörünü hesaplamaya normalizasyon denir.
            self.yon = self.yon.normalize()
            self.hitbox.x += self.yon.x * hiz
            self.carpisma('yatay')
            self.hitbox.y += self.yon.y * hiz
            self.carpisma('dikey')
            self.rect.center = self.hitbox.center


    def carpisma(self,yon):
        if yon == 'yatay':
            for sprite in self.engeller_sprites:
                if sprite.hitbox.colliderect(self.hitbox): # carpisma/temas oldu mu
                    if self.yon.x > 0: # oyuncu saga dogru ilerliyor
                        self.hitbox.right = sprite.hitbox.left # ic ice gecmemeleri icin
                    if self.yon.x<0:
                        self.hitbox.left = sprite.hitbox.right


        if yon == 'dikey':
            for sprite in self.engeller_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.yon.y > 0: # oyuncu asagi dogru hareket eder
                        self.hitbox.bottom = sprite.hitbox.top # oyuncunun alt yuzeyinin noktasi: bottom
                    if self.yon.y<0:
                        self.hitbox.top = sprite.hitbox.bottom


    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0