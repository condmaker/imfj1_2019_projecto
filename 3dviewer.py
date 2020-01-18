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

    cube2 = Object3d("Cube2")
    cube2.position += vector3(0.25, 0.5, 0)
    cube2.mesh = Mesh.create_pyr((0.5, 1, 1))
    cube2.material = Material(color(0,1,0,1), "TestMaterial2")
    cube.add_child(cube2)

    cube3 = Object3d("Cube2")
    cube3.position += vector3(-0.25, 0.5, 0)
    cube3.mesh = Mesh.create_pyr((0.5, 1, 1))
    cube3.material = Material(color(0,1,0,1), "TestMaterial2")
    cube.add_child(cube3)
    
    angle = 15
    axis = vector3(0,0,0)
    #axis.normalize()
    
    delta_time = 0
    prev_time = time.time()
    
    flag = False

    #pygame.event.set_grab(True)

    while(True):

        if (flag):
            axis = vector3(0,0,0)
            flag = False

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                return
            elif (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    return

        # Clears the screen with a very dark blue (0, 0, 20)
        screen.fill((0,0,0))

        test = pygame.key.get_pressed()

        # Moves the object around X, Y, Z
        if (test[pygame.K_LEFT]):
            axis += vector3(0,2,0)
            flag = True
        if (test[pygame.K_RIGHT]):
            axis -= vector3(0,2,0)
            flag = True
        if (test[pygame.K_UP]):
            axis -= vector3(2,0,0)
            flag = True
        if (test[pygame.K_DOWN]):
            axis += vector3(2,0,0)
            flag = True
        if (test[pygame.K_PAGEUP]):
            axis -= vector3(0,0,2)
            flag = True
        if (test[pygame.K_PAGEDOWN]):
            axis += vector3(0,0,2)
            flag = True
        
        # Moves the object in relation to the camera
        if (test[pygame.K_w]):
            cube.position += vector3(0, 0.01, 0)
            flag = True
        if (test[pygame.K_s]):
            cube.position -= vector3(0, 0.01, 0)
            flag = True
        if (test[pygame.K_a]):
            cube.position -= vector3(0.01, 0, 0)
            flag = True
        if (test[pygame.K_d]):
            cube.position += vector3(0.01, 0, 0)
            flag = True
        if (test[pygame.K_q]):
            cube.position -= vector3(0, 0, 0.01)
            flag = True
        if (test[pygame.K_e]):
            cube.position += vector3(0, 0, 0.01)
            flag = True

        # Rotates the object, considering the time passed (not linked to frame rate)
        q = from_rotation_vector((axis * math.radians(angle) * delta_time).to_np3())
        cube.rotation = q * cube.rotation

        scene.render(screen)

        # Swaps the back and front buffer, effectively displaying what we rendered
        pygame.display.flip()

        # Updates the timer, so we we know how long has it been since the last frame
        delta_time = time.time() - prev_time
        prev_time = time.time()

main()