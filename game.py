from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import json
from random import randrange
import sys

app = Ursina()

grass_texture = load_texture("assets/grass_block.png")
stone_texture = load_texture("assets/stone_block.png")
brick_texture = load_texture("assets/brick_block.png")
dirt_texture = load_texture("assets/dirt_block.png")
sky_texture = load_texture("assets/skybox.png")
arm_texture = load_texture("assets/arm_texture.png")
blockBreak = Audio("assets/block_break.mp3", loop=False, autoplay=False)
blockMake = Audio("assets/block_make.mp3", loop=False, autoplay=False)
texturePicked = 1
voxels = []

def index_in_list(a_list, index):
    return index < len(a_list)

def update():
    global texturePicked

    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()

    if held_keys['1']:
        texturePicked = 1
    elif held_keys['2']:
        texturePicked = 2
    elif held_keys['3']:
        texturePicked = 3
    elif held_keys['4']:
        texturePicked = 4


class Voxel(Button):
    def __init__(self, position=(0,0,0), texture=grass_texture):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=0.5,
            texture=texture,
            color=color.white,
            highlight_color=color.color(0,0,0.92),
            scale=0.5,
            localTextureNumber = texturePicked
        )
        voxels.append({
            'x': self.position.x,
            'y': self.position.y,
            'z': self.position.z,
            'texture': texturePicked
        })
    def input(self, key):
        global voxels

        if self.hovered:
            if key=='left mouse down':
                blockBreak.play()
                index = voxels.index({
                    'x': self.position.x,
                    'y': self.position.y,
                    'z': self.position.z,
                    'texture': self.localTextureNumber
                })

                del voxels[index]

                destroy(self)

            elif key=='right mouse down':
                blockMake.play()

                if texturePicked == 1:
                    voxel = Voxel(position = self.position + mouse.normal, texture=grass_texture)
                if texturePicked == 2:
                    voxel = Voxel(position = self.position + mouse.normal, texture=stone_texture)
                if texturePicked == 3:
                    voxel = Voxel(position = self.position + mouse.normal, texture=brick_texture)
                if texturePicked == 4:
                    voxel = Voxel(position = self.position + mouse.normal, texture=dirt_texture)


class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture= sky_texture,
            scale=150,
            double_sided=True
        )

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='assets/arm',
            texture=arm_texture,
            scale=0.2,
            rotation=Vec3(150, -10, 0),
            position=Vec2(1, -0.6)
        )
    def active(self):
        self.position=Vec2(0.9,-0.5)
    def passive(self):
        self.position=Vec2(1, -0.6)

class Underlay(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='quad',
            scale=(0.20, 0.05),
            position=Vec2(0, -0.465),
            color=color.rgba(0, 0, 0.75, 100),
            texture=load_texture('assets/inventory underlay.png'))


class Inventory(Entity):
    def __init__(self, texture, position, letter):
        super().__init__(
            parent=camera.ui,
            scale=(0.04, 0.04),
            model='quad',
            position=position,
            texture=texture
        )
        self.letter = letter
    def input(self, key):
        if key == f"{self.letter}":
            self.scale = 0.05
        else:
            self.scale = 0.04

if index_in_list(sys.argv, 1):
    data=open(sys.argv[1], "r+").read()
    dataPythonList = json.loads(data)
    for i in range(len(dataPythonList)):
        if dataPythonList[i]['texture'] == 1:
            texturePicked = 1
            voxel = Voxel(position=(dataPythonList[i]['x'], dataPythonList[i]['y'], dataPythonList[i]['z']), texture=grass_texture)
        if dataPythonList[i]['texture'] == 2:
            texturePicked = 2
            voxel = Voxel(position=(dataPythonList[i]['x'], dataPythonList[i]['y'], dataPythonList[i]['z']), texture=stone_texture)
        if dataPythonList[i]['texture'] == 3:
            texturePicked = 3
            voxel = Voxel(position=(dataPythonList[i]['x'], dataPythonList[i]['y'], dataPythonList[i]['z']), texture=brick_texture)
        if dataPythonList[i]['texture'] == 4:
            texturePicked = 4
            voxel = Voxel(position=(dataPythonList[i]['x'], dataPythonList[i]['y'], dataPythonList[i]['z']), texture=dirt_texture)
        print_on_screen("Loaded world from " + sys.argv[1], position=(0,0), origin=(0,0), scale=2)
        texturePicked = 1
else:
    for z in range(20):
        for x in range(20):
            voxel=Voxel(position=(x,0,z))

player = FirstPersonController()
sky = Sky()
hand = Hand()
underlay = Underlay()
inv1 = Inventory(load_texture("assets/grass_block_inventory.png"), Vec2(-0.073, -0.465), '1')
inv2 = Inventory(load_texture("assets/stone_block_inventory.png"), Vec2(-0.025, -0.465), '2')
inv3 = Inventory(load_texture("assets/brick_block_inventory.png"), Vec2(0.025, -0.465), '3')
inv4 = Inventory(load_texture("assets/dirt_block_inventory.png"), Vec2(0.073, -0.465), '4')

#Export
def export():
    jsonString = json.dumps(voxels)
    num = randrange(100)
    f = open("world" + str(num) + ".json", "w")
    print_on_screen("Exported world to world" + str(num) + ".json", position=(0,0), origin=(0,0), scale=2)

    f.write(jsonString)

def input(key):
    if key=='e':
        export()

app.run()