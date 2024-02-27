from ursina import *

def transformDirection(local_direction, rotation):
    quat = Quat()
    quat.setHpr(rotation.normalized())
    world_direction = quat.xform(local_direction)

    return world_direction

def fromToRotation(from_vec, to_vec):
    from_vec = from_vec.normalized()
    to_vec = to_vec.normalized()

    angle = from_vec.angleDeg(to_vec)
    axis = from_vec.cross(to_vec)

    if axis.length() < 0.0001:
        return Quat.identQuat()
    else:
        axis.normalize()

    rotation = Quat()
    rotation.setFromAxisAngle(angle, axis)

    return rotation