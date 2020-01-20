import pygame
from vector3 import *
from object3d import *

class Mesh:
    def __init__(self, name = "UnknownMesh"):
        self.name = name
        self.polygons = []

    def offset(self, v):
        new_polys = []
        for poly in self.polygons:
            new_poly = []
            for p in poly:
                new_poly.append(p + v)
            new_polys.append(new_poly)

        self.polygons = new_polys

    def render(self, screen, matrix, material, cf):
        c = material.color.tuple3()      
        i = 0

        for poly in self.polygons:
            tpoly = []
            tvout = []
            for v in poly:
                vout = v.to_np4()
                vout = vout @ matrix
                
                tvout.append([vout[0], vout[1], vout[2]])
                tpoly.append( ( screen.get_width() * 0.5 + vout[0] / vout[3], screen.get_height() * 0.5 - vout[1] / vout[3]) )

            if ( i < len(poly) - 1):
                aa = tvout[0]
                bb = tvout[1]
                cc = tvout[2]

                #print(tvout)
                #print(aa)
                #print(bb)
                #print(cc)
                a = vector3(aa[0], aa[1], aa[2])
                b = vector3(bb[0], bb[1], bb[2])
                c = vector3(cc[0], cc[1], cc[2])

                #print(a)
                #print(b)
                #print(c)
                A1 = a - b
                A2 = a - c
                R1 = cross_product(A1, A2)
                
                #print(tvout)
                #print((dot_product(R1, cf)))

                if (dot_product(R1, -cf) < 0):
                    pygame.draw.polygon(screen, (255, 255, 255), tpoly, material.line_width)
            i += 1
        


    @staticmethod
    def create_cube(size, mesh = None):
        if (mesh == None):
            mesh = Mesh("UnknownCube")

        Mesh.create_quad(vector3( size[0] * 0.5, 0, 0), vector3(0, -size[1] * 0.5, 0), vector3(0, 0, size[2] * 0.5), mesh)
        Mesh.create_quad(vector3(-size[0] * 0.5, 0, 0), vector3(0,  size[1] * 0.5, 0), vector3(0, 0, size[2] * 0.5), mesh)

        Mesh.create_quad(vector3(0,  size[1] * 0.5, 0), vector3(size[0] * 0.5, 0), vector3(0, 0, size[2] * 0.5), mesh)
        Mesh.create_quad(vector3(0, -size[1] * 0.5, 0), vector3(-size[0] * 0.5, 0), vector3(0, 0, size[2] * 0.5), mesh)

        Mesh.create_quad(vector3(0, 0,  size[2] * 0.5), vector3(-size[0] * 0.5, 0), vector3(0, size[1] * 0.5, 0), mesh)
        Mesh.create_quad(vector3(0, 0, -size[2] * 0.5), vector3( size[0] * 0.5, 0), vector3(0, size[1] * 0.5, 0), mesh)

        return mesh

    @staticmethod
    def create_quad(origin, axis0, axis1, mesh):
        if (mesh == None):
            mesh = Mesh("UnknownQuad")

        poly = []
        poly.append(origin + axis0 + axis1)
        poly.append(origin + axis0 - axis1)
        poly.append(origin - axis0 - axis1)
        poly.append(origin - axis0 + axis1)

        mesh.polygons.append(poly)

        return mesh
    
    @staticmethod
    def create_pyr(size, mesh = None):
        if (mesh == None):
            mesh = Mesh("UnknownPyr")

        Mesh.create_trig(vector3(0, size[1] * 0.5, 0), vector3(size[0] * 0.5, 0, 0), vector3(-size[0] * 0.5, 0, 0), mesh)  # ACB
        Mesh.create_trig(vector3(0, size[1] * 0.5, 0), vector3(-size[0] * 0.5, 0, 0), vector3(0, 0, size[2] * 0.5), mesh)  # ABD
        Mesh.create_trig(vector3(0, size[1] * 0.5, 0), vector3(size[0] * 0.5, 0, 0), vector3(0, 0, size[2] * 0.5), mesh)   # ACD
        Mesh.create_trig(vector3(-size[0] * 0.5, 0, 0), vector3(size[0] * 0.5, 0, 0), vector3(0, 0, size[2] * 0.5), mesh)  # BCD

        return mesh

    @staticmethod
    def create_trig(v1, v2, v3, mesh):
        if (mesh == None):
            mesh = Mesh("UnknownTrig")
        
        poly = []
        poly.append(v1)
        poly.append(v2)
        poly.append(v3)

        mesh.polygons.append(poly)

        return mesh
    
