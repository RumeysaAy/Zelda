import pygame
from kullanici_arayuzu import Kullanici_Arayuzu
from magic import MagicPlayer
from particles import AnimationPlayer
from settings import *
from kaya import Kaya
from player import Player
from debug import debug
from support import *
from random import choice,randint
from silah import Silah
from dusman import Dusman
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False
        
        self.visible_sprites = Camera()
        self.engeller_sprites = pygame.sprite.Group()

        self.simdi_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group() # saldiriya acik


        self.harita_olustur()

        # kullanici arayuzu ui
        self.kullanici_arayuzu =Kullanici_Arayuzu()
        self.upgrade = Upgrade(self.player)

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def harita_olustur(self):
        layouts = {
            'sinirlar': import_csv_layout('map/map_FloorBlocks.csv'),
            'cimenler': import_csv_layout('map/map_Grass.csv'),
            'nesneler':import_csv_layout('map/map_Objects.csv'),
            'entities':import_csv_layout('map/map_Entities.csv')
        }

        resimler = {
            'cimenler':import_folder('resimler/grass'),
            'objects':import_folder('resimler/objects'),
        }

        # style = sinirlar, layout = import_csv_layout('map/map_FloorBlocks.csv')
        for style,layout in layouts.items():
            for satir_index,satir in enumerate(layout):
                for sutun_index,sutun in enumerate(satir):
                    if sutun != '-1': # -1 disindaki yerler engeldir, gorunmez kayalar
                        x = sutun_index * kaya_boyut
                        y = satir_index * kaya_boyut
                        if style == 'sinirlar':
                            Kaya((x,y),[self.engeller_sprites],'invisible')

                        if style == 'cimenler':
                            random_grass_image = choice(resimler['cimenler'])
                            Kaya(
                                (x,y),
                                [self.visible_sprites,self.engeller_sprites,self.attackable_sprites],
                                'cimen',
                                random_grass_image)
                        
                        if style == 'nesneler':
                            surf =resimler['objects'][int(sutun)]
                            Kaya((x,y),[self.visible_sprites,self.engeller_sprites],'obje',surf)

                        if style == 'entities':
                            if sutun == '394':
                                self.player = Player((x,y),
                                [self.visible_sprites],
                                self.engeller_sprites,
                                self.create_attack,
                                self.destroy_attack,
                                self.create_magic)
                            else:
                                if sutun == '390':
                                    monster_name = 'bamboo'
                                elif sutun == '391':
                                    monster_name = 'spirit' # hayalet
                                elif sutun == '392':
                                    monster_name = 'raccoon' 
                                else:
                                    monster_name = 'squid' # murekkep baligi

                                Dusman(
                                    monster_name,
                                    (x,y),
                                    [self.visible_sprites,self.attackable_sprites],
                                    self.engeller_sprites,
                                    self.player_verilen_hasar,
                                    self.trigger_death_particles,
                                    self.add_exp)
                

    def create_attack(self):
        self.simdi_attack = Silah(self.player, [self.visible_sprites,self.attack_sprites])


    def create_magic(self,style,guc,zarar):
        if style == 'heal':
            self.magic_player.heal(self.player,guc,zarar,[self.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player,zarar,[self.visible_sprites,self.attack_sprites])


    def destroy_attack(self):
        if self.simdi_attack:
            self.simdi_attack.kill() # silahlarin temizlenmesi icin, haritada kalmamasi icin
        self.simdi_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                carpisma_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                # Dokill argümanı bir bool. True olarak ayarlanırsa, çarpışan tüm Sprite'lar Gruptan kaldırılacaktır.
                # spritecollide: Başka bir hareketli grafikle kesişen bir gruptaki hareketli grafikleri bulun.
                if carpisma_sprites:
                    for hedef_sprite in carpisma_sprites:
                        if hedef_sprite.sprite_type == 'cimen':
                            konum = hedef_sprite.rect.center
                            offset = pygame.math.Vector2(0,75)
                            for leaf in range(randint(3,6)):
                                self.animation_player.cimen_olustur_particles(konum - offset,[self.visible_sprites])
                            hedef_sprite.kill()
                        else:
                            hedef_sprite.get_hasar(self.player,attack_sprite.sprite_type)
    
    def player_verilen_hasar(self,miktar,attack_type):
        if self.player.vulnerable:
            self.player.saglik -= miktar
            self.player.vulnerable = False
            self.player.zarar_zamani = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])
    
    def trigger_death_particles(self,konum,particle_type):
        self.animation_player.create_particles(particle_type,konum,self.visible_sprites)
    
    def add_exp(self,miktar):
        self.player.exp += miktar

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def run(self):
        self.visible_sprites.draw(self.player)
        self.kullanici_arayuzu.display(self.player)

        if self.game_paused: # display upgrade menu
            self.upgrade.display()
        else: # run the game
            self.visible_sprites.update()
            self.visible_sprites.dusman_update(self.player)
            self.player_attack_logic()



class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.genisligin_yarisi = self.display_surface.get_size()[0] // 2
        self.yuksekligin_yarisi = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # zemini olusturma
        self.zemin_surf = pygame.image.load("resimler/ground.png").convert()
        self.zemin_rect = self.zemin_surf.get_rect(topleft = (0,0))

    def draw(self,player):
        
        # oyuncu ile birlikte haritanın hareket etmesini saglamaya calısıyorum
        self.offset.x = player.rect.centerx - self.genisligin_yarisi
        self.offset.y = player.rect.centery - self.yuksekligin_yarisi
        
        # zemini cizme
        zemin_offset_pos = self.zemin_rect.topleft - self.offset
        self.display_surface.blit(self.zemin_surf,zemin_offset_pos)
        
        # oyuncunun ust kismi kayanin altinda kalmasini engellemek için spritelari y ye gore siralama
        for sprite in sorted(self.sprites(),key=lambda sprite: sprite.rect.centery):
            # offset_rect artik dikdortgen degildir, konumdur
            offset_pos = sprite.rect.topleft - self.offset # topleft: yukarinin sol kosesi
            # blit: resmi bir yüzey üzerine yerleştirmeye yarıyor.
            self.display_surface.blit(sprite.image,offset_pos)

    def dusman_update(self,player):
        # hasattr() yöntemi, bir nesne verilen adlandırılmış özniteliğe sahipse true, yoksa false döndürür.
        dusman_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'dusman']
        for dusman in dusman_sprites:
            dusman.dusman_update(player)