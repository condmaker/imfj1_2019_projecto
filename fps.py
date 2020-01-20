import pygame
import pygame.freetype
import time
import numpy 

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
    objflag = True
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
            
            
        forwardMovementVector = vector3(scene.camera.forward().x,0,scene.camera.forward().z)

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
        
        if(axis.magnitude() != 0):
            axis = axis.normalized() * mouseSens 

           
        # Rotates the object, considering the time passed (not linked to frame rate)
        q = from_rotation_vector((axis * math.radians(angle) * delta_time).to_np3()) 
        scene.camera.rotation = scene.camera.rotation * q 

        # The PRS Matrix with the rotation values around the camera's position.
        objMatrix = cube.get_prs_matrix(vector3(0, 0, 0), quaternion(scene.camera.position.x, scene.camera.position.y, scene.camera.position.z), cube.scale)

        # The cube normal, transformed to a 4D vector in order to be multiplied with the PRS Matrix
        objNormal = cube.forward().to_np4()
        # The PRS Matrix converted into an array
        objMatrixArray = np.array(objMatrix)

        # This variable will do the multiplication between objNormal and objMatrixArray to create the rotated vector. 
        detectVect = vector3(numpy.matmul(objNormal, objMatrixArray).tolist())

        # Variables with the x, y and z values of the vector
        arg1 = detectVect.x[0]
        arg2 = detectVect.x[1]
        arg3 = detectVect.x[2]

        # Transformation of the rotated vector into vector3, so that it can be used in the dot product between the camera normal.
        detectVect2 = vector3(arg1, arg2, arg3)
        
        # Verifies if the cube and rotated camera normals dot product is negative, and if it is, does not render the object
        if (dot_product(scene.camera.forward().normalized(), - detectVect2.normalized()) < 0):
            if (objflag):
                scene.objects.remove(cube)
                print("dog")
                objflag = False
        else:
            objflag = True
            if (cube not in scene.objects):
                scene.add_object(cube)
        scene.render(screen)

        # Swaps the back and front buffer, effectively displaying what we rendered
        pygame.display.flip()

        # Updates the timer, so we we know how long has it been since the last frame
        delta_time = time.time() - prev_time
        prev_time = time.time()



main()