genislik = 1280	
yukseklik = 720
fps = 60
kaya_boyut = 64
hitbox_offset = {
    'player':-26,
    'obje':-40,
    'cimen':-10,
    'invisible':0
}

# kullanici arayuzu
bar_yuksekligi = 20
saglik_bar_genisligi = 200
enerji_bar_genisligi = 140
item_box_size = 80
ui_font = 'font/joystix.ttf'
ui_font_size = 18

# renkler
su_renk = '#71ddee'
ui_bg_renk ='#222222'
ui_kenar_renk='#111111'
text_color = '#EEEEEE'

# ui renkler
saglik_renk = 'red'
enerji_renk ='blue'
ui_kenar_renk_active = 'gold'

# upgrade menu
text_color_selected = '#111111'
bar_color = '#EEEEEE'
bar_color_selected = '#111111' # siyah
upgrade_bg_color_selected = '#EEEEEE' #beyaz

silah_verileri = {
    'sword':{'cooldown':100, 'hasar':15, 'resim':'resimler/weapons/sword/full.png'},
    'lance':{'cooldown':400, 'hasar':30, 'resim':'resimler/weapons/lance/full.png'},
    'axe':{'cooldown':300, 'hasar':20, 'resim':'resimler/weapons/axe/full.png'},
    'rapier':{'cooldown':50, 'hasar':8, 'resim':'resimler/weapons/rapier/full.png'},
    'sai':{'cooldown':80, 'hasar':10, 'resim':'resimler/weapons/sai/full.png'}
}

magic_data = {
    'flame':{'guc':5, 'zarar':20, 'resim':'resimler/particles/flame/fire.png'},
    'heal':{'guc':20, 'zarar':10, 'resim':'resimler/particles/heal/heal.png'}
}
# flame: ates
# heal: iyilesmek

# dusman
monster_data = {
    'squid':{'saglik':100, 'exp':100, 'hasar':20, 'attack_type':'slash','attack_sound':'audio/attack/slash.wav', 'hiz':3, 'direnc':3, 'attack_yaricapi':80, 'farketme_yaricapi':360},
    'raccoon':{'saglik':300, 'exp':250, 'hasar':40, 'attack_type':'claw','attack_sound':'audio/attack/claw.wav', 'hiz':2, 'direnc':3, 'attack_yaricapi':120, 'farketme_yaricapi':400},
    'spirit':{'saglik':100, 'exp':110, 'hasar':8, 'attack_type':'thunder','attack_sound':'audio/attack/fireball.wav', 'hiz':4, 'direnc':3, 'attack_yaricapi':60, 'farketme_yaricapi':350},
    'bamboo':{'saglik':70, 'exp':120, 'hasar':6, 'attack_type':'leaf_attack','attack_sound':'audio/attack/slash.wav', 'hiz':3, 'direnc':3, 'attack_yaricapi':50, 'farketme_yaricapi':300}
}
