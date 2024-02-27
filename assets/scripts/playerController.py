from ursina import *
from assets.scripts.RigidBody import RigidBody,BoxShape

class Player(Entity):
    def __init__(self,world):
        super().__init__(model='cube',scale=0.1,y=51)
        self.rigidBody = RigidBody(world,BoxShape(),self,1)
        
        self.speed = 5
        self.jumpForce = 3
        self.senstivity = Vec2(500,500)

        mouse.locked = True
        mouse.visible = False

        camera.parent = self
        camera.fov = 85
        camera.position = Vec3(0,1,0)
        camera.rotation = Vec3(0,0,0)

        self.speedText = Text('speed: 0',parent=camera.ui,x=0.75,y=0.25)

        self.pointer = Entity(model='quad',scale=.005,rotation_z=45,parent=camera.ui)
    
    def update(self):
        global groundCheck
        self.rigidBody.setActive(True)

        #camera
        rotationX = mouse.x * self.senstivity.x
        rotationY = mouse.y * self.senstivity.y

        self.rotation_y += rotationX * time.dt
        
        camera.rotation_x -= rotationY * time.dt
        camera.rotation_x = clamp(camera.rotation_x,-90,90)

        #movement
        moveDir = (self.left * (-held_keys['d']+held_keys['a']) + self.forward * (-held_keys['s']+held_keys['w'])).normalized()
        targetMoveAmount = moveDir * self.speed
        self.rigidBody.setLinearVelocity(self.rigidBody.getLinearVelocity()+targetMoveAmount*time.dt)
        
        #ground check
        groundCheck = raycast(self.world_position,-self.up.normalized(),0.1,ignore=[self,])

        #velocity limit
        velocity = Vec3(self.rigidBody.getLinearVelocity())
        if sqrt(velocity.x**2+velocity.z**2) > 2:
            velocityXY = velocity.xz.normalized() * 2
            self.rigidBody.setLinearVelocity(Vec3(velocityXY.x,velocity.y,velocityXY.y))
        
        #speed text
        self.speedText.text = f"speed: {round(velocity.length(),1)}"
    
    def input(self,key):
        if key == 'space':
            if groundCheck.hit:
                self.jump()
    
    def jump(self):
        self.rigidBody.applyCentralImpulse(self.up.normalized()*self.jumpForce)