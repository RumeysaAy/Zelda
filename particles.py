import pygame
from support import import_folder
from random import choice

class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # magic
            'flame':import_folder('resimler/particles/flame/frames'),
            'aura':import_folder('resimler/particles/aura'),
            'heal':import_folder('resimler/particles/heal/frames'),

            # attacks
            'claw':import_folder('resimler/particles/claw'),
            'slash':import_folder('resimler/particles/slash'),
            'sparkle':import_folder('resimler/particles/sparkle'),
            'leaf_attack':import_folder('resimler/particles/leaf_attack'),
            'thunder':import_folder('resimler/particles/thunder'),

            # monster deaths
            'squid':import_folder('resimler/particles/smoke_orange'),
            'raccoon':import_folder('resimler/particles/raccoon'),
            'spirit':import_folder('resimler/particles/nova'),
            'bamboo':import_folder('resimler/particles/bamboo'),

            # leafs
            'leaf': (
                import_folder('resimler/particles/leaf1'),
                import_folder('resimler/particles/leaf2'),
                import_folder('resimler/particles/leaf3'),
                import_folder('resimler/particles/leaf4'),
                import_folder('resimler/particles/leaf5'),
                import_folder('resimler/particles/leaf6'),
                self.reflect_images(import_folder('resimler/particles/leaf1')),
                self.reflect_images(import_folder('resimler/particles/leaf2')),
                self.reflect_images(import_folder('resimler/particles/leaf3')),
                self.reflect_images(import_folder('resimler/particles/leaf4')),
                self.reflect_images(import_folder('resimler/particles/leaf5')),
                self.reflect_images(import_folder('resimler/particles/leaf6'))
            )


        }

    def reflect_images(self,frames): # yansitma
        new_frames = []
        for frame in frames:
            ters_cevrilmis_frame = pygame.transform.flip(frame,True,False)
            # transform.flip, bir Yüzeyi dikey, yatay veya her ikisini birden çevirebilir.
            new_frames.append(ters_cevrilmis_frame)
        return new_frames

    def cimen_olustur_particles(self,konum,gruplar):
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(konum,animation_frames,gruplar)

    def create_particles(self,animation_type,konum,gruplar):
        animation_frames = self.frames[animation_type]
        ParticleEffect(konum,animation_frames,gruplar)

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self,konum,animation_frames,gruplar):
        super().__init__(gruplar)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_hiz = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = konum)


    def animate(self):
        self.frame_index += self.animation_hiz
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()