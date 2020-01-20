import pygame
import pygame.freetype
import time
import numpy 

from jsonreader import *
from scene import *
from object3d import *
from mesh import *
from material import *
from color import *

def main():
    
    pygame.init()

    mouseSens = 25

    res_x = 1080
    res_y = 720

    #List of all possible objects
    objects = []


    screen = pygame.display.set_mode((res_x, res_y))

    scene = Scene("3d_Viewer")
    scene.camera = Camera(False, res_x, res_y)

    scene.camera.position += vector3(1, 1, 1)
    scene.camera.position -= vector3(0, 0, 2)



# ----- Objects in the Scene -----

    #Cube - Blue
    cube = Object3d("Cube1")
    cube.scale = vector3(1, 1, 1)
    cube.position = vector3(3, 1, 3)
    m = Mesh()
    m.polygons = retrieve_points("cube", 2)
    cube.mesh = m
    cube.material = Material(color(0,1,1,1), "TestMaterial1", 0)
    scene.add_object(cube)
    objects.append(cube)

    #Pyramid - Orange
    pyr = Object3d("Pyramid1")
    pyr.scale = vector3(1, 1, 1)
    pyr.position = vector3(1, 1, 1)
    p = Mesh()
    p.polygons = retrieve_points("pyramid", 2)
    pyr.mesh = p
    pyr.material = Material(color(1,0.5,0,1), "TestMaterial2s", 0)
    scene.add_object(pyr)
    objects.append(pyr)

    #Pyramid - Green
    pyr = Object3d("Pyramid2")
    pyr.scale = vector3(1, 4, 1)
    pyr.position = vector3(-2, 4, 1)
    p = Mesh()
    p.polygons = retrieve_points("pyramid", 2)
    pyr.mesh = p
    pyr.material = Material(color(0,0.5,0,1), "TestMaterial3s", 0)
    scene.add_object(pyr)
    objects.append(pyr)


    #Pyramid - Grey
    pyr = Object3d("Pyramid3")
    pyr.scale = vector3(1, 1, 1)
    pyr.position = vector3(-3, 1, 2)
    p = Mesh()
    p.polygons = retrieve_points("pyramid", 2)
    pyr.mesh = p
    pyr.material = Material(color(0.5,0.5,0.5,1), "TestMaterial4s", 0)
    scene.add_object(pyr)
    objects.append(pyr)
    


    angle = 15
    axis = vector3(0,0,0)
    #axis.normalize()
    
    delta_time = 0
    prev_time = time.time()
    
    flag = False
    objflag = True
    #pygame.event.set_grab(True)


# ----- Game ----- 
    
    while(True):
        
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                return
            elif (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    return

        # Clears the screen with a very dark blue (0, 0, 20)
        screen.fill((5,5,15))

        test = pygame.key.get_pressed()

        movementSpeed = 0.01

        pygame.mouse.set_visible(True)

        axis = vector3(0,0,0)

        #Player looks to the left
        if(pygame.mouse.get_pos()[0] < res_x / 2):
            axis += vector3(0,1,0)
            pygame.mouse.set_pos((res_x / 2, res_y / 2))
              
        #Player looks to the right      
        if(pygame.mouse.get_pos()[0] > res_x / 2):
            axis -= vector3(0,1,0)
            pygame.mouse.set_pos((res_x / 2, res_y / 2))
            
        #Player looks down
        if(pygame.mouse.get_pos()[1] > res_y / 2):
            axis -= scene.camera.right()
            pygame.mouse.set_pos((res_x / 2, res_y / 2))
      
        #Player looks up
        if(pygame.mouse.get_pos()[1] < res_y / 2):
            axis += scene.camera.right()
            pygame.mouse.set_pos((res_x / 2, res_y / 2))    
            
        #Locks play to the ground / Ensures player can't fly around   
        forwardMovementVector = vector3(scene.camera.forward().x,0,scene.camera.forward().z)

        #Adds mouse sensibility to the camera movement
        if(axis.magnitude() != 0):
            axis = axis.normalized() * mouseSens 

        # Moves the object around X, Y, Z
        if (test[pygame.K_s]):
            scene.camera.position -= forwardMovementVector * movementSpeed
            flag = True
        if (test[pygame.K_a]):
            scene.camera.position -= scene.camera.right() * movementSpeed
            flag = True
        if (test[pygame.K_d]):
            scene.camera.position += scene.camera.right() * movementSpeed
            flag = True
        if (test[pygame.K_w]):
            scene.camera.position += forwardMovementVector * movementSpeed
            flag = True
   
           
        # Rotates the object, considering the time passed (not linked to frame rate)
        q = from_rotation_vector((axis * math.radians(angle) * delta_time).to_np3()) 
        scene.camera.rotation = scene.camera.rotation * q 

        # Verifies if each object and rotated camera normals dot product is negative, and if it is, does not render the object
        for obj in objects:
            if (dot_product(scene.camera.forward().normalized(), - (obj.position - scene.camera.position).normalized()) > -0.5):
                if (objflag):
                    if (obj in scene.objects):
                        scene.objects.remove(obj)
                        objflag = False
            else:
                objflag = True
                if (obj not in scene.objects):
                    scene.add_object(obj)

        scene.render(screen)

        # Swaps the back and front buffer, effectively displaying what we rendered
        pygame.display.flip()

        # Updates the timer, so we we know how long has it been since the last frame
        delta_time = time.time() - prev_time
        prev_time = time.time()

main()