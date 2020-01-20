import pygame
import pygame.freetype
import time

from scene import *
from object3d import *
from mesh import *
from material import *
from color import *

def main():
    pygame.init()

    mouseSens = 25

    '''x_axis = vector3(1,0,0)
    y_axis = vector3(0,1,0)
    z_axis = vector3(0,0,1)'''

    res_x = 1080
    res_y = 720

    screen = pygame.display.set_mode((res_x, res_y))

    scene = Scene("3d_Viewer")
    scene.camera = Camera(False, res_x, res_y)

    scene.camera.position += vector3(1, 1, 1)
    scene.camera.position -= vector3(0, 0, 2)


    cube = Object3d("Cube1")
    cube.scale = vector3(1, 1, 1)
    cube.position = vector3(1, 1, 1)
    cube.mesh = Mesh.create_pyr((1, 1, 1), None)
    cube.material = Material(color(1,0,0,1), "TestMaterial1")
    scene.add_object(cube)


    
    angle = 15
    axis = vector3(0,0,0)
    #axis.normalize()
    
    delta_time = 0
    prev_time = time.time()
    
    flag = False

    #pygame.event.set_grab(True)

    while(True):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                return
            elif (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    return

        # Clears the screen with a very dark blue (0, 0, 20)
        screen.fill((0,0,0))

        test = pygame.key.get_pressed()

        movementSpeed = 0.01

        pygame.mouse.set_visible(True)

        axis = vector3(0,0,0)

        if(pygame.mouse.get_pos()[0] < res_x / 2):
            axis += vector3(0,1,0)
            pygame.mouse.set_pos((res_x / 2, res_y / 2))
           
          
        if(pygame.mouse.get_pos()[0] > res_x / 2):
            axis -= vector3(0,1,0)
            pygame.mouse.set_pos((res_x / 2, res_y / 2))
            

        if(pygame.mouse.get_pos()[1] > res_y / 2):
            axis -= scene.camera.right()
            pygame.mouse.set_pos((res_x / 2, res_y / 2))
            
        
        if(pygame.mouse.get_pos()[1] < res_y / 2):
            axis += scene.camera.right()
            pygame.mouse.set_pos((res_x / 2, res_y / 2))
            
            

        # Moves the object around X, Y, Z
        if (test[pygame.K_s]):
            scene.camera.position -= scene.camera.forward() * movementSpeed
            flag = True
        if (test[pygame.K_a]):
            scene.camera.position -= scene.camera.right() * movementSpeed
            flag = True
        if (test[pygame.K_d]):
            scene.camera.position += scene.camera.right() * movementSpeed
            flag = True
        if (test[pygame.K_w]):
            scene.camera.position += scene.camera.forward() * movementSpeed
            flag = True
        


        if(axis.magnitude() != 0):
            axis = axis.normalized() * mouseSens 

           
         # Rotates the object, considering the time passed (not linked to frame rate)
        q = from_rotation_vector((axis * math.radians(angle) * delta_time).to_np3()) 
        scene.camera.rotation =scene.camera.rotation * q 


        scene.render(screen)

        # Swaps the back and front buffer, effectively displaying what we rendered
        pygame.display.flip()

        # Updates the timer, so we we know how long has it been since the last frame
        delta_time = time.time() - prev_time
        prev_time = time.time()



main()