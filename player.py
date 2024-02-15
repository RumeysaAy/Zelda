import pygame
from settings import *
from support import import_folder
from entity import Entity

class Player(Entity):
    def __init__(self,konum,gruplar,engeller_sprites,create_attack,destroy_attack,create_magic):
        super().__init__(gruplar)
        self.image = pygame.image.load('resimler/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = konum)
        self.hitbox = self.rect.inflate(-6,hitbox_offset['player'])

        # resimler
        self.import_player_assets()
        self.durumlar = 'down'

        self.attacking = False
        # 400 milisaniyede bir ates etsin
        self.attack_cooldown = 400
        self.attack_time = None

        self.engeller_sprites = engeller_sprites

        # silah
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack # saldirinin/attack in tukenmesi
        self.silah_index = 3
        self.silah = list(silah_verileri.keys())[self.silah_index]
        self.silah_degistirilebilir_mi = True
        self.silah_degistirme_zamani = None
        self.cooldowna_gecis_suresi = 200

        #magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.magic_degistirilebilir_mi = True
        self.magic_degistirme_zamani = None

        # ozellikler
        self.ozellikler = {'saglik':100,'enerji':60,'attack':10,'magic':4,'hiz':5}
        self.max_ozellikler = {'saglik':300,'enerji':140,'attack':20,'magic':10,'hiz':10}
        self.upgrade_zarar = {'saglik':100,'enerji':100,'attack':100,'magic':100,'hiz':100}
        self.saglik = self.ozellikler['saglik'] * 0.5
        self.enerji = self.ozellikler['enerji'] * 0.8
        self.exp = 5000 # deneyim
        self.hiz = self.ozellikler['hiz']

        # hasar zamani
        self.vulnerable = True
        self.zarar_zamani = None
        self.dokunulmazlik_suresi = 500

        # sesler
        self.silah_attack_sound = pygame.mixer.Sound('audio/sword.wav')
        self.silah_attack_sound.set_volume(0.9)


    def import_player_assets(self):
        character_path = 'resimler/player/'
        self.animations = {
            'up':[], 'down':[], 'left':[], 'right':[],
            'right_idle':[], 'left_idle':[], 'up_idle':[], 'down_idle':[],
            'right_attack':[], 'left_attack':[], 'up_attack':[], 'down_attack':[]
        }
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)


    def input(self):
        # attack sirasinda hareket etmesin
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # hareket etmek için girisler
            if keys[pygame.K_UP]:
                self.yon.y = -1
                self.durumlar = 'up'
            elif keys[pygame.K_DOWN]:
                self.yon.y = 1
                self.durumlar = 'down'
            else:
                self.yon.y = 0

            if keys[pygame.K_RIGHT]:
                self.yon.x = 1
                self.durumlar = 'right'
            elif keys[pygame.K_LEFT]:
                self.yon.x = -1
                self.durumlar = 'left'
            else:
                self.yon.x = 0


            # saldiri ile sihir ayni anda yapilamaz
            # saldiri icin girisler
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.silah_attack_sound.play()

            # sihirler icin girisler
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                guc = list(magic_data.values())[self.magic_index]['guc'] + self.ozellikler['magic']
                zarar = list(magic_data.values())[self.magic_index]['zarar']
                self.create_magic(style,guc,zarar)

            # silah icin
            if keys[pygame.K_q] and self.silah_degistirilebilir_mi:
                self.silah_degistirilebilir_mi = False
                self.silah_degistirme_zamani = pygame.time.get_ticks()
                if self.silah_index < len(list(silah_verileri.keys()))-1:
                    self.silah_index += 1
                else:
                    self.silah_index = 0
                self.silah = list(silah_verileri.keys())[self.silah_index]

            # magic icin
            if keys[pygame.K_e] and self.magic_degistirilebilir_mi:
                self.magic_degistirilebilir_mi = False
                self.magic_degistirme_zamani = pygame.time.get_ticks()
                if self.magic_index < len(list(magic_data.keys()))-1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0
                self.magic = list(magic_data.keys())[self.magic_index]


    def get_durumlar(self):

        # idle durum
        if self.yon.x == 0 and self.yon.y == 0:
            if not 'idle' in self.durumlar  and not 'attack' in self.durumlar:
                self.durumlar = self.durumlar + '_idle'

        if self.attacking:
            self.yon.x =0
            self.yon.y =0
            if not 'attack' in self.durumlar:
                if 'idle' in self.durumlar:
                    self.durumlar = self.durumlar.replace('_idle','_attack')
                else:
                    self.durumlar = self.durumlar + '_attack'
        else:
            # attack durumunda kalmasini engellendi
            if 'attack' in self.durumlar:
                self.durumlar = self.durumlar.replace('_attack','')


    def cooldown(self): # cooldown/bekleme suresinde attack yapilamaz
        simdiki_zaman = pygame.time.get_ticks()

        if self.attacking:
            if simdiki_zaman - self.attack_time >= self.attack_cooldown + silah_verileri[self.silah]['cooldown']:
                self.attacking = False
                self.destroy_attack()

        if not self.silah_degistirilebilir_mi:
            if simdiki_zaman - self.silah_degistirme_zamani >= self.cooldowna_gecis_suresi:
                self.silah_degistirilebilir_mi = True

        if not self.magic_degistirilebilir_mi:
            if simdiki_zaman - self.magic_degistirme_zamani >= self.cooldowna_gecis_suresi:
                self.magic_degistirilebilir_mi = True

        if not self.vulnerable:
            if simdiki_zaman - self.zarar_zamani >= self.dokunulmazlik_suresi:
                self.vulnerable = True


    def animate(self):
        animation = self.animations[self.durumlar]

        self.frame_index += self.animation_hiz
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # dusman vurusundan sonra oyuncunun titrer
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(225)


    def get_full_silah_hasar(self):
        temel_hasar = self.ozellikler['attack']
        silah_hasar = silah_verileri[self.silah]['hasar']
        return temel_hasar + silah_hasar

    def get_full_magic_hasar(self):
        temel_hasar = self.ozellikler['magic']
        magic_hasar = magic_data[self.magic]['guc']
        return temel_hasar + magic_hasar

    def get_value_by_index(self,index):
        return list(self.ozellikler.values())[index]

    def get_cost_by_index(self,index):
        return list(self.upgrade_zarar.values())[index]

    def enerji_recovery(self):
        if self.enerji < self.ozellikler['enerji']:
            self.enerji += 0.01 * self.ozellikler['magic']
        else:
            self.enerji = self.ozellikler['enerji']

    def update(self):
        self.input()
        self.cooldown()
        self.get_durumlar()
        self.animate()
        self.move(self.ozellikler['hiz'])
        self.enerji_recovery()