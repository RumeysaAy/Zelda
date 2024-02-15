from curses.panel import top_panel
from operator import index
from turtle import color, left, title, up
from unicodedata import name
import pygame
from settings import *

class Upgrade:
    def __init__(self,player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_nr = len(player.ozellikler)
        self.attribute_names = list(player.ozellikler.keys()) # attribute: nitelik
        self.max_degerler = list(player.max_ozellikler.values())
        self.font = pygame.font.Font(ui_font,ui_font_size)

        # item olusturma
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6
        self.create_items()

        # selection system
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

    def input(self):
        keys = pygame.key.get_pressed()
        
        if self.can_move:    
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_nr - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].trigger(self.player)

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True
                
    def create_items(self):
        self.item_list = []
        for item,index in enumerate(range(self.attribute_nr)):
            # yatay
            full_width = self.display_surface.get_size()[0]
            artis = full_width // self.attribute_nr
            left = (item * artis) + (artis - self.width) // 2

            # dikey
            top = self.display_surface.get_size()[1] * 0.1
            
            # nesne olusturulacak
            item = Item(left,top,self.width,self.height,index,self.font)
            self.item_list.append(item)
    
    def display(self):
        self.input()
        self.selection_cooldown()

        for index,item in enumerate(self.item_list):
            # get attributes
            name = self.attribute_names[index]
            deger = self.player.get_value_by_index(index)
            max_deger = self.max_degerler[index]
            zarar = self.player.get_cost_by_index(index) 
            item.display(self.display_surface,self.selection_index,name,deger,max_deger,zarar)



class Item:
    def __init__(self,l,t,w,h,index,font):
        self.rect = pygame.Rect(l,t,w,h)
        self.index = index
        self.font = font


    def display_names(self,surface,name,zarar,selected):
        color = text_color_selected if selected else text_color

        # title
        title_surf = self.font.render(name,False,color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))

        # cost
        cost_surf = self.font.render(f'{int(zarar)}',False,color)
        cost_rect = cost_surf.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(0,20))

        # draw
        surface.blit(title_surf,title_rect)
        surface.blit(cost_surf,cost_rect)

    def display_bar(self,surface,deger,max_deger,selected):
        # drawing setup
        top = self.rect.midtop + pygame.math.Vector2(0,60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0,60)
        color = bar_color_selected if selected else bar_color

        # bar setup
        full_height = bottom[1] - top[1]
        number = (deger/max_deger) * full_height
        deger_rect = pygame.Rect(top[0] - 15,bottom[1] - number,30,10)

        # draw elements
        pygame.draw.line(surface,color,top,bottom,5)
        pygame.draw.rect(surface,color,deger_rect)

    def trigger(self,player):
        upgrade_attribute = list(player.ozellikler.keys())[self.index]

        if player.exp >= player.upgrade_zarar[upgrade_attribute] and player.ozellikler[upgrade_attribute] < player.max_ozellikler[upgrade_attribute]:
            player.exp -= player.upgrade_zarar[upgrade_attribute]
            player.ozellikler[upgrade_attribute] *= 1.2
            player.upgrade_zarar[upgrade_attribute] *= 1.4

        if player.ozellikler[upgrade_attribute] > player.max_ozellikler[upgrade_attribute]:
            player.ozellikler[upgrade_attribute] = player.max_ozellikler[upgrade_attribute]

    def display(self,surface,selection_num,name,deger,max_deger,zarar):
        if self.index == selection_num:
            pygame.draw.rect(surface,upgrade_bg_color_selected,self.rect)
            pygame.draw.rect(surface,ui_kenar_renk,self.rect,4)
        else:
            pygame.draw.rect(surface,ui_bg_renk,self.rect)
            pygame.draw.rect(surface,ui_kenar_renk,self.rect,4)

        self.display_names(surface,name,zarar,self.index == selection_num)
        self.display_bar(surface,deger,max_deger,self.index == selection_num)