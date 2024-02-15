import pygame
from settings import *

class Kaya(pygame.sprite.Sprite):
    def __init__(self,konum,gruplar,sprite_type,surface =pygame.Surface((kaya_boyut,kaya_boyut))):
        super().__init__(gruplar)
        self.sprite_type = sprite_type
        y_offset = hitbox_offset[sprite_type]
        self.image = surface
        if sprite_type == 'obje':
            self.rect = self.image.get_rect(topleft = (konum[0],konum[1] - kaya_boyut))
        else:
            self.rect = self.image.get_rect(topleft = konum)
        # rect boyutunun yuksekligini kisaltacagiz: alt ve ust kisimdan 5 piksel silinir
        self.hitbox = self.rect.inflate(0,y_offset)











# yükleyeceğimiz resimleri daha hızlı ekrana çizilmesini sağlamak için convert() ve convert_alpha() methodlarını kullanıyoruz.
# Eğer resim dosyası alpha değeri içeriyor ise convert_alpha() methodunu kullanmalıyız. Yoksa convert() methodu yeterlidir.

# Alpha kanalı bir resimdeki bir piksel ya da bir bölgenin ne kadar saydam olacağını belirleyen kanaldır.
# Arkaplan kesme ve saydamlık ayarlamada kullanılır.
# Bir pikselin bir diğer piksel üzerine düştüğünde ortaya çıkacak rengin oranını belirler.