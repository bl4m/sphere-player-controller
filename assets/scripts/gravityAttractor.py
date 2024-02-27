from ursina import *
from assets.scripts.RigidBody import RigidBody
from assets.scripts.functions import fromToRotation


class GravityAttractor(Entity):
    def __init__(self):
        self.gravity = -10
        self.entity:Entity = None
    def Attract(self,entity:"Entity",E_rb:"RigidBody"):
        gravityUp = (entity.world_position - self.entity.world_position).normalized()

        bodyUp = entity.up.normalized()

        rotation = fromToRotation(bodyUp,gravityUp)
        rotation = rotation.normalized()

        target_rotation =  entity.getQuat() * rotation
        target_rotation.normalized()

        entity.setQuat(slerp(entity.getQuat(), target_rotation, 1*time.dt))

        E_rb.applyCentralForce(gravityUp*self.gravity)
