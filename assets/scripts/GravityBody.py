from ursina import *
from assets.scripts.gravityAttractor import GravityAttractor
from assets.scripts.RigidBody import RigidBody

class GravityBody(Entity):
    def __init__(self,rigidBody:"RigidBody",attractor:"GravityAttractor"):
        self.entity:Entity = None
        self.rigidBody = rigidBody
        self.attractor = attractor
    def update(self):
        self.rigidBody.setAngularFactor(Vec3(0,0,0))
        self.attractor.Attract(self.entity,self.rigidBody)
