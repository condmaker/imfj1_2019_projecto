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

    # Defining the resolution
    res_x = 1080
    res_y = 720
    screen = pygame.display.set_mode((res_x, res_y))

    # Starting the scene
    scene = Scene("3d_Viewer")
    scene.camera = Camera(False, res_x, res_y)
    global scene

    # Positioning the starting position of the camera
    scene.camera.position += vector3(1, 1, 1)
    scene.camera.position -= vector3(0, 0, 2)

    # Defining the first object, a tetrahedron
    tetahedron = Object3d("Tetahedr1")
    tetahedron.scale = vector3(1, 1, 1)
    tetahedron.position = vector3(1, 1, 1)
    tetahedron.mesh = Mesh.create_pyr((1, 1, 1), None)
    tetahedron.material = Material(color(1,0,0,1), "TestMaterial1")
    scene.add_object(tetahedron)

    # Defining the second tetahedron, that is a child of 'cube'
    tthdr2 = Object3d("Tetahedr2")
    tthdr2.position += vector3(0.25, 0.5, 0)
    tthdr2.mesh = Mesh.create_pyr((0.5, 1, 1))
    tthdr2.material = Material(color(0,1,0,1), "TestMaterial2")
    tetahedron.add_child(tthdr2)

    # Defining the third tetahedron, that is also a child of 'cube'
    tthdr3 = Object3d("Tetahedr2")
    tthdr3.position += vector3(-0.25, 0.5, 0)
    tthdr3.mesh = Mesh.create_pyr((0.5, 1, 1))
    tthdr3.material = Material(color(0,1,0,1), "TestMaterial2")
    tetahedron.add_child(tthdr3)
    
    # Defining the angle and axis of the object that will be rotated (normalizing the axis gives a divided by 0 error)
    angle = 15
    axis = vector3(0,0,0)
    #axis.normalize()
    
    # Starting the delta_time variable so the game runs on time and is not tied to framerate
    delta_time = 0
    prev_time = time.time()
    
    flag = False

    while(True):

        # A flag that verifies if the player has pressed a key, and puts the axis at (0,0,0) position so it doesn't keep moving 
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

        # Gets a list of all the pressed keys so we can observe actions around them
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
            tetahedron.position += vector3(0, 0.01, 0)
            flag = True
        if (test[pygame.K_s]):
            tetahedron.position -= vector3(0, 0.01, 0)
            flag = True
        if (test[pygame.K_a]):
            tetahedron.position -= vector3(0.01, 0, 0)
            flag = True
        if (test[pygame.K_d]):
            tetahedron.position += vector3(0.01, 0, 0)
            flag = True
        if (test[pygame.K_q]):
            tetahedron.position -= vector3(0, 0, 0.01)
            flag = True
        if (test[pygame.K_e]):
            tetahedron.position += vector3(0, 0, 0.01)
            flag = True

      

        # Rotates the object, considering the time passed (not linked to frame rate)
        q = from_rotation_vector((axis * math.radians(angle) * delta_time).to_np3())
        tetahedron.rotation = q * tetahedron.rotation

        scene.render(screen)

        # Swaps the back and front buffer, effectively displaying what we rendered
        pygame.display.flip()

        # Updates the timer, so we we know how long has it been since the last frame
        delta_time = time.time() - prev_time
        prev_time = time.time()

main()