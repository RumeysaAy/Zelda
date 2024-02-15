from calendar import month_name
import pygame
from settings import *
from entity import Entity
from support import *

class Dusman(Entity):
    def __init__(self, monster_name,konum, gruplar,engeller_sprites,player_verilen_hasar,trigger_death_particles,add_exp):
        super().__init__(gruplar)
        self.sprite_type = 'dusman'

        # resimler
        self.import_resimler(monster_name)
        self.durumlar = 'idle'
        self.image = self.animations[self.durumlar][self.frame_index]
        
        # hareket
        self.rect = self.image.get_rect(topleft = konum)
        self.hitbox = self.rect.inflate(0,-10)
        self.engeller_sprites = engeller_sprites

        # ozellikler
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.saglik = monster_info['saglik']
        self.exp = monster_info['exp']
        self.hiz =monster_info['hiz']
        self.hasar =monster_info['hasar']
        self.direnc = monster_info['direnc']
        self.attack_yaricapi = monster_info['attack_yaricapi']
        self.farketme_yaricapi = monster_info['farketme_yaricapi']
        self.attack_type = monster_info['attack_type']

        # oyuncu saldirisi
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.player_verilen_hasar = player_verilen_hasar
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp
        
        # yenilmezlik
        self.vulnerable = True
        self.vurus_zamani = None
        self.yenilmezlik_suresi = 300

        # sesler
        self.death_sound = pygame.mixer.Sound('audio/death.wav')
        self.hit_sound = pygame.mixer.Sound('audio/hit.wav')
        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
        self.death_sound.set_volume(0.9)
        self.hit_sound.set_volume(0.9)
        self.attack_sound.set_volume(0.9)



    def import_resimler(self,name):
        self.animations = {'idle':[],'move':[],'attack':[]}
        main_path = f'resimler/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)


    def get_oyuncu_mesafe_yonu(self,player):
        dusman_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        mesafe = (player_vec - dusman_vec).magnitude()
        if mesafe > 0:
            yon = (player_vec - dusman_vec).normalize()
        else:
            yon = pygame.math.Vector2()


        return (mesafe,yon)

    
    def get_durumlar(self,player):
        mesafe = self.get_oyuncu_mesafe_yonu(player)[0]

        if mesafe <= self.attack_yaricapi and self.can_attack:
            if self.durumlar != 'attack':
                self.frame_index = 0
            self.durumlar = 'attack'
        elif mesafe <= self.farketme_yaricapi:
            self.durumlar = 'move'
        else:
            self.durumlar = 'idle'
    

    def actions(self,player):
        if self.durumlar == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.player_verilen_hasar(self.hasar,self.attack_type)
            self.attack_sound.play()
        elif self.durumlar == 'move':
            self.yon = self.get_oyuncu_mesafe_yonu(player)[1]
        else:
            self.yon = pygame.math.Vector2()


    def animate(self):
        animation = self.animations[self.durumlar]
        self.frame_index += self.animation_hiz
        if self.frame_index >= len(animation):
            if self.durumlar == 'attack':
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)

        else:
            self.image.set_alpha(255)

    def cooldown(self):
        simdiki_zaman = pygame.time.get_ticks()
        if not self.can_attack:
            simdiki_zaman = pygame.time.get_ticks()
            if simdiki_zaman - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        
        if not self.vulnerable:
            if simdiki_zaman - self.vurus_zamani >= self.yenilmezlik_suresi:
                self.vulnerable = True


    def get_hasar(self,player,attack_type):
        if self.vulnerable:
            self.hit_sound.play()
            self.yon = self.get_oyuncu_mesafe_yonu(player)[1]
            if attack_type == 'silah':
                self.saglik -= player.get_full_silah_hasar()
            else: # magic hasar
                self.saglik -= player.get_full_magic_hasar()
            self.vurus_zamani = pygame.time.get_ticks()
            self.vulnerable = False

 
    def check_death(self):
        if self.saglik <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.center,self.monster_name)
            self.add_exp(self.exp)
            self.death_sound.play()

    def hit_reaction(self):
        if not self.vulnerable:
            self.yon *= -self.direnc


    def update(self):
        self.hit_reaction()
        self.move(self.hiz)
        self.animate()
        self.cooldown()
        self.check_death()


    def dusman_update(self,player):
        self.get_durumlar(player)
        self.actions(player)