from os import readlink
from turtle import color
import pygame
from settings import *
from player import *

class Kullanici_Arayuzu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(ui_font, ui_font_size)
        
        # bar
        self.saglik_bar_rect = pygame.Rect(10,10,saglik_bar_genisligi,bar_yuksekligi) # 10,10 : sol ust
        self.enerji_bar_rect = pygame.Rect(10,34,enerji_bar_genisligi,bar_yuksekligi)

        self.silah_resimleri = []
        for silah in silah_verileri.values():
            path = silah['resim']
            silah = pygame.image.load(path).convert_alpha()
            self.silah_resimleri.append(silah)

        self.magic_resimleri = []
        for magic in magic_data.values():
            path = magic['resim']
            magic = pygame.image.load(path).convert_alpha()
            self.magic_resimleri.append(magic)

    def show_bar(self,suan,max_miktar,bg_rect,renk):
        # draw background/arka plan
        pygame.draw.rect(self.display_surface,ui_bg_renk,bg_rect)

        # ozellikleri pixele donusturme
        oran = suan/max_miktar # su anki miktar ile max miktar esitse oran 1
        guncel_genislik = bg_rect.width * oran # 1*200 den 200 pixele ceviririz
        guncel_rect =bg_rect.copy()
        guncel_rect.width = guncel_genislik

        # draw bar
        pygame.draw.rect(self.display_surface,renk,guncel_rect)
        pygame.draw.rect(self.display_surface,ui_kenar_renk,bg_rect,3)

    def show_exp(self,exp):
        text_surf = self.font.render(str(int(exp)),False,text_color) # kenar yumusatma:false cunku pixel resimde olmamali
        x= self.display_surface.get_size()[0] -20
        y= self.display_surface.get_size()[1] -20
        text_rect = text_surf.get_rect(bottomright = (x,y))

        pygame.draw.rect(self.display_surface,ui_bg_renk,text_rect.inflate(20,20))
        self.display_surface.blit(text_surf,text_rect)
        pygame.draw.rect(self.display_surface,ui_kenar_renk,text_rect.inflate(20,20),3)
    
    def secim_kutusu(self,left,top,degisti):
        bg_rect = pygame.Rect(left,top,item_box_size,item_box_size)
        pygame.draw.rect(self.display_surface,ui_bg_renk,bg_rect)
        if degisti:
            pygame.draw.rect(self.display_surface,ui_kenar_renk_active,bg_rect,3)
        else:
            pygame.draw.rect(self.display_surface,ui_kenar_renk,bg_rect,3)
        
        return bg_rect

    def silah_overlay(self,silah_index,degisti):
        bg_rect = self.secim_kutusu(10,630,degisti) # silah icin
        silah_surf = self.silah_resimleri[silah_index]
        silah_rect = silah_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(silah_surf,silah_rect)

    def magic_overlay(self,magic_index,degisti):
        bg_rect = self.secim_kutusu(80,635,degisti) # magic icin
        magic_surf = self.magic_resimleri[magic_index]
        magic_rect = magic_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(magic_surf,magic_rect)

    def display(self,player):
        self.show_bar(player.saglik,player.ozellikler['saglik'],self.saglik_bar_rect,saglik_renk)
        self.show_bar(player.enerji,player.ozellikler['enerji'],self.enerji_bar_rect,enerji_renk)

        self.show_exp(player.exp)

        self.silah_overlay(player.silah_index,not player.silah_degistirilebilir_mi)
        self.magic_overlay(player.magic_index, not player.magic_degistirilebilir_mi)
        # self.secim_kutusu(80,630) # magic/sihir/buyu icin