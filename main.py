from ursina import *
from assets.scripts.RigidBody import RigidBody,BulletWorld,SphereShape,CapsuleShape,BoxShape
from assets.scripts.GravityBody import GravityBody
from assets.scripts.gravityAttractor import GravityAttractor
from assets.scripts.playerController import Player
from panda3d.core import DirectionalLight

app = Ursina(development_mode=False,borderless=False)
app.setFrameRateMeter(True)
world = BulletWorld()

window.color = color.black

def random_position_excluding_center(min_distance, max_distance, exclude_radius):
    while True:
        pos = Vec3(random.uniform(-max_distance, max_distance),
                   random.uniform(-max_distance, max_distance),
                   random.uniform(-max_distance, max_distance),)
        if pos.length() > min_distance + exclude_radius:
            return pos


num_entities = 500
for _ in range(num_entities):
    size = random.uniform(0.25, 0.4)
    position = random_position_excluding_center(0, 100, 60)  # Adjust range as needed
    e = Entity(model='sphere', scale=size, position=position)
    e.setLightOff()

planet = Entity(model='assets\\models\\planet',texture='grass',scale=100,collider='sphere')
planet_RB = RigidBody(world,SphereShape(),planet)
planet.add_script(GravityAttractor())

player = Player(world)
player.add_script(GravityBody(player.rigidBody,planet.scripts[0]))

cube = Entity(model='cube',y=50)

def update():
    world.DoPhysics(time.dt)
    dlnp.setPos(player.world_position)


resolution = 1024
dlight = DirectionalLight("sun")

ambientlight = AmbientLight(color=Vec4(0.1,0.1,0.1,1))

dlight.setShadowCaster(True, resolution, resolution)

lens = dlight.getLens()
lens.setNearFar(-80, 200)
lens.setFilmSize((5, 5))

dlnp = render.attachNewNode(dlight)
dlnp.lookAt((-0.7, -0.9, 0.5))
render.setLight(dlnp)

dlnp.setPos((3,10,0))

render.setShaderAuto()

app.run()