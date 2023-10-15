import os
import sys
import numpy as np
import time
from PIL import Image
import math
import itertools
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import nrrd
import argparse
import subprocess
from scipy.ndimage import map_coordinates
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.transforms import Affine2D
import mpl_toolkits.axisartist.floating_axes as floating_axes
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import RegularGridInterpolator, interp2d

sys.path.append('../')
#import SAXAGetPlane TODO
import RotateImage

def get_plane_equation_from_points(P, Q, R):  
    x1, y1, z1 = P
    x2, y2, z2 = Q
    x3, y3, z3 = R
    a1 = x2 - x1 
    b1 = y2 - y1 
    c1 = z2 - z1 
    a2 = x3 - x1 
    b2 = y3 - y1 
    c2 = z3 - z1 
    a = b1 * c2 - b2 * c1 
    b = a2 * c1 - a1 * c2 
    c = a1 * b2 - b1 * a2 
    d = (- a * x1 - b * y1 - c * z1) 
    return a, b, c, d

#### Utils #####
def normalizeLength(x) :
    # x: (3,n)
    return x / np.linalg.norm(x)

def get_transformation_matrix(n1,o1,n2,o2) :
    """ Get transformation matrix to transform from plane 1 to plane 2
    
    To transform points with the matrix (left-multiplication):
      x' = Mx
      
    Assumption(s):
      - normalized normal vectors
    
    Args:
      n1: normal on plane 1, shape: (3)
      o1: origin of plane 1 space, shape: (3)
      n2: normal on plane 2, shape: (3)
      o2: origin of plane 2 space, shape: (3)
    
    """
    
    # match normal directions of the two planes
    if np.dot(n1,n2) < 0 :
        # revert direction of n1
        n1 = -n1
        
    # Translation from plane 1 to plane 2    
    t = o2-o1

    
    # Rotation from plane 1 to plane 2
    #https://gist.github.com/kevinmoran/b45980723e53edeb8a5a43c49f134724
    cross = np.cross(n1, n2)
    cx,cy,cz = cross
    cos = np.dot(n1, n2)
    k = (1-cos) / ((1+cos) * (1-cos))
    
    R = np.array([
        [cx*cx*k + cos, cy*cx*k -  cz, cz*cx*k +  cy],
        [cx*cy*k +  cz, cy*cy*k + cos, cz*cy*k -  cx],
        [cx*cz*k -  cy, cy*cz*k +  cx, cz*cz*k + cos],
    ])
        
    # Compose 4x4 transformation matrix
    M = np.eye(4)
    M[0:3,3] = t
    M[:3,:3] = R

    return M

##### Cross section utils #####
# From https://stackoverflow.com/a/73355110/11956857
def PlaneBoundsIntersectionsLines (n, pos, dim):
    """Outputs points and vectors defining the lines that the view creates by intersecting the volume's bounds.
      Input:
        Normal vector of the given plane and the coords of a point belonging to the plane.
      Output:
        normals_line, points_line
    """
    def intersectionPlanePlane(n1,p1,n2,p2):
        # Get direction of line
        nout = np.cross(n1.reshape((1,3)),n2.reshape((1,3))).reshape(3,1)
        #print("nout (cross): ", nout.shape)
        #print(nout)
        nout = normalizeLength(nout)
        M =  np.concatenate((n1.reshape(1,3),n2.reshape(1,3)), axis=0)
        b = np.zeros((2,1))
        # print(n1.shape, p1.shape)
        b[0,0]=np.dot(n1,p1)
        b[1,0]=np.dot(n2,p2)
        pout,resid,rank,s = np.linalg.lstsq(M,b, rcond=None)
        return pout, nout

    # ... For each face
    normalFaces = np.concatenate((np.eye(3,3),np.eye(3,3)), axis = 1)
    pointsFaces = np.array([[0,0,0],[0,0,0],[0,0,0], dim, dim, dim]).transpose()
    points_line = np.zeros((3,6))
    normals_line = np.zeros((3,6))

    for face in range(6):
        n1 = normalFaces[:,face].reshape(3,)
        p1 = pointsFaces[:,face].reshape(3,)
        pout, nout = intersectionPlanePlane(n1,p1,n,pos)
        points_line[:,face] = pout.reshape((3,))
        normals_line[:,face] = nout.reshape((3,))

    return normals_line, points_line

def FindPlaneCorners(normals_line, points_line, dim, th=25):
    
    """Outputs the points defined by the intersection of the input lines that 
    are close enough to the borders of the volume to be considered corners of the view plane.
      Input:
        Points and vectors defining lines
      Output:
        p_intersection, intersecting_lines
        """
    def intersectionLineLine(Up,P0,Uq,Q0):
        # Computes the closest point between two lines
        # Must be column points
        b = np.zeros((2,1))
        b[0,0] = -np.dot((P0-Q0),Up)
        b[1,0] = -np.dot((P0-Q0),Uq)
        A = np.zeros((2,2))
        A[0,0] = np.dot(Up,Up)
        A[0,1] = np.dot(-Uq,Up)
        A[1,0] = np.dot(Up,Uq)
        A[1,1] = np.dot(-Uq,Uq)
        if ( np.abs(np.linalg.det(A)) < 10^(-10) ):
            point = np.array([np.nan, np.nan, np.nan]).reshape(3,1)
        else:
            lbd ,resid,rank,s = np.linalg.lstsq(A,b, rcond=None)
            # print('\n')
            # print(lbd)
            P1 = P0 + lbd[0]*Up
            Q1 = Q0 + lbd[1]*Uq
            point = (P1+Q1)/2
        return point
    # ... ... Get closest point for every possible pair of lines and select only the ones inside the box
    npts = 0
    p_intersection = []
    intersecting_lines = []
    # ... Get all possible pairs of lines
    possible_pairs = np.array(list(itertools.combinations(np.linspace(0,normals_line.shape[1]-1,normals_line.shape[1]), 2)))
    for i_pair,pair in enumerate(possible_pairs):
        #print(f"=== pair #{i_pair}: {pair}")
        k = int(pair[0])
        j = int(pair[1])
        Up = normals_line[:,k]
        P0 = points_line[:,k]
        Uq = normals_line[:,j]
        Q0 = points_line[:,j]
        #print("Up: ", Up)
        #print("P0: ", P0)
        #print("Uq: ", Uq)
        #print("Q0: ", Q0)
        closest_point = intersectionLineLine(Up,P0,Uq,Q0)
        epsilon = 2.2204e-10
        # ... ... Is point inside volume? Is it close to the border?
        if closest_point[0] <= dim[0] + epsilon and closest_point[0] >= 0 - epsilon and \
                    closest_point[1] <= dim[1] + epsilon and closest_point[1] >= 0 - epsilon and \
                    closest_point[2] <= dim[2] + epsilon and closest_point[2] >= 0 - epsilon:
            # ... ...  Is it close to the border? 25 mm?
            if dim[0] - closest_point[0] <= th or closest_point[0] - 0 <= th or \
              dim[1] - closest_point[1] <= th or closest_point[1] - 0 <= th or \
              dim[2] - closest_point[2] <= th or closest_point[2] - 0 <= th:
                # print('It is close to teh border')
                npts += 1
                p_intersection.append(closest_point)
                intersecting_lines.append([k,j])

    p_intersection = np.array(p_intersection).transpose()

    return p_intersection, intersecting_lines

def FindNormalByCoords(coords):
    # coords (ls, 3)
    p0, p1, p2 = coords

    a, b, c, d = get_plane_equation_from_points(p0, p1, p2)
    if a == b == c == d == 0:
        print("Error: The three points are on the same straight line!")
        1/0
        return 0

    return np.array([a, b, c])

def FindVisualFromCoords(coords, volume):

    normal = FindNormalByCoords(coords)
    #print(normal)
    #print(coords)
    # print("Calculated Plane Normal: ", normal)
    normal = normal/np.linalg.norm(normal) # normalize

    pos = coords[0]

    up_axis = np.array([0,0,1])
    origin_pt = np.array([0,0,0])

    # ... Get intersection lines between plane and volume bounds
    normals_line, points_line = PlaneBoundsIntersectionsLines(normal, pos, volume.shape)

    # Remove nan lines (= no intersection between the plane and the volume bound)
    mask = ~np.isnan(normals_line).any(axis=0)
    normals_line = normals_line[:,mask]
    points_line = points_line[:,mask]

    # print("normals_line: ", normals_line.shape)
    # print(normals_line)
    # print("points_line: ", points_line.shape)
    # print(points_line)

    # ... Get intersections between generated lines to get corners of view plane
    p_intersection, intersecting_lines = FindPlaneCorners(normals_line, points_line, volume.shape, th=1e-6)
    # print(p_intersection.shape, len(intersecting_lines))

    # # ... Calculate parameters of the 2D slice
    Pose_slice_vrf = get_transformation_matrix(
        up_axis, origin_pt, # z-axis, origin
        normal, pos,
    )
    # print("Pose_slice_vrf: ", Pose_slice_vrf.shape)
    # print(Pose_slice_vrf)

    # ... ... ... Apply transform to corners
    p_intersection_slicerf = np.zeros(p_intersection.shape)
    for corner in range(p_intersection.shape[1]):
        pt_arr = np.concatenate((p_intersection[:,corner], np.ones((1,))) ,axis = 0).reshape((4,1))
        p_intersection_slicerf[:,corner] = np.matmul(np.linalg.inv(Pose_slice_vrf), pt_arr)[:-1].reshape((3,))

    # Also apply transform to coordiantes
    counter = 0
    new_pos = np.zeros(coords.shape)
    for p in coords:
        pt_arr = np.concatenate((p, np.ones((1,))), axis = 0).reshape((4,1))
        new_pos[counter] = np.matmul(np.linalg.inv(Pose_slice_vrf), pt_arr)[:-1].reshape((3,))
        counter += 1

    # ... ... Get slice size based on corners and spacing
    spacing_slice = [1,1]
    min_bounds_slice_xy = np.min(p_intersection_slicerf,axis=1)
    max_bounds_slice_xy = np.max(p_intersection_slicerf,axis=1)
    size_slice_x = int(np.ceil((max_bounds_slice_xy[0] - min_bounds_slice_xy[0] - 1e-6) / spacing_slice[0]))
    size_slice_y = int(np.ceil((max_bounds_slice_xy[1] - min_bounds_slice_xy[1] - 1e-6) / spacing_slice[1]))
    slice_size = [size_slice_x, size_slice_y, 1]
    # print('slice_size')
    # print(slice_size)

    # print("====================================")

    # ... ... Get corner in slice coords and redefine transform mat - make corner origin of the slice
    origin_corner_slice = np.array([min_bounds_slice_xy[0], min_bounds_slice_xy[1],0])
    pt_arr = np.concatenate((origin_corner_slice, np.ones((1,))) , axis=0).reshape((4,1))
    origin_corner_slice_vrf = np.matmul(Pose_slice_vrf, pt_arr)[:-1].reshape((3,))
    Pose_slice_origin_corner_vrf = get_transformation_matrix(
        up_axis, origin_pt, # z-axis, origin
        normal, origin_corner_slice_vrf
    )

    # print("origin_corner_slice: ", origin_corner_slice.shape)
    # print(origin_corner_slice)

    # print("origin_corner_slice_vrf: ", origin_corner_slice_vrf.shape)
    # print(origin_corner_slice_vrf)

    # ... ... Get every possible inslice coordinates
    xvalues = np.linspace(0, size_slice_x-1,size_slice_x)
    yvalues = np.linspace(0, size_slice_y-1,size_slice_y)
    zvalues = np.linspace(0,0,1)
    xx, yy = np.meshgrid(xvalues, yvalues)
    xx = xx.transpose()
    yy = yy.transpose()
    zz = np.zeros(xx.shape)
    inslice_coords = np.concatenate((xx.reshape(-1,1), yy.reshape(-1,1), zz.reshape(-1,1)), axis = 1)

    # ... ... Map every xy point of slice into volume's RF
    inslice_coords_vrf = np.zeros(inslice_coords.shape)
    for coord_set in range(inslice_coords.shape[0]):
        pt_arr = np.concatenate((inslice_coords[coord_set,:],np.ones((1,))) ,axis = 0).reshape((4,1))
        inslice_coords_vrf[coord_set,:] = np.matmul(Pose_slice_origin_corner_vrf, pt_arr)[:-1].reshape((3,))


    # Map 3d up vector into 2d space
    # 3d coord to 2d space
    # 2d to 3d. Inverse when use
    Pose_slice_origin_cspecial = get_transformation_matrix(
        up_axis, (64, 64, 0), # (0,0,1) , (0,0,0)
        normal, origin_corner_slice_vrf, # <--- this is only different
    )

    up_coord1 = [0, 0, 1] # this coordinate system is same for "pos"
    pt_arr = np.concatenate((up_coord1, np.ones((1,))) ,axis = 0).reshape((4,1))
    up_in_2d_1 = np.matmul(np.linalg.inv(Pose_slice_origin_cspecial), pt_arr)
    up_in_2d_1 = up_in_2d_1[:-1].reshape(3, )
    #print(up_in_2d_1)

    up_coord2 = [0, 0, 64] # this coordinate system is same for "pos" 
    pt_arr = np.concatenate((up_coord2, np.ones((1,))) ,axis = 0).reshape((4,1))
    up_in_2d_2 = np.matmul(np.linalg.inv(Pose_slice_origin_cspecial), pt_arr)
    up_in_2d_2 = up_in_2d_2[:-1].reshape(3, )    
    #print(up_in_2d_2)

    up_in_2d = up_in_2d_2 - up_in_2d_1

    # displace the coordinates
    displacement_pts = new_pos - origin_corner_slice

    start_time = time.perf_counter()
    result = map_coordinates(volume, inslice_coords_vrf.T, order=1)
    end_time = time.perf_counter()
    print("Map Coordinates time: ", end_time-start_time)
    result = result.reshape(size_slice_x, size_slice_y)
    print("result: ", result.shape, result.min(), result.max())

    return result, displacement_pts, up_in_2d

def HandleRotations(img, coords, up_vector, view):

    slope = up_vector[0] / up_vector[1]
    #print("slope: ", slope)
    angle = math.degrees(math.atan(1 / slope))
    
    # for handling inverted cases. will also h flip later
    if up_vector[0] > 0:
        angle += 180
        
    #print("angle: ", angle)
    #rotated_image = img.rotate(-angle)
    rotated_image = RotateImage.rotate(img, -angle)

    # Rotate the coordinates
    center_x = rotated_image.width // 2
    center_y = rotated_image.height // 2

    rotated_coords = []
    for coord in coords:
        # Translate the coordinates relative to the center
        translated_x = coord[1] - center_x
        translated_y = coord[0] - center_y

        # Apply the rotation transformation
        rotated_x = int(translated_x * math.cos(math.radians(angle)) -
                        translated_y * math.sin(math.radians(angle)))
        rotated_y = int(translated_x * math.sin(math.radians(angle)) +
                        translated_y * math.cos(math.radians(angle)))

        # Translate the coordinates back to be relative to the top-left corner
        rotated_x += center_x
        rotated_y += center_y

        rotated_coords.append((rotated_x, rotated_y))
        
    rotated_coords = np.array(rotated_coords)

    # for handling inverted cases
    if up_vector[0] > 0:
        rotated_image = RotateImage.h_flip(rotated_image)
        rotated_coords[:, 0] = rotated_image.width - rotated_coords[:, 0]

    # TODO Checking for each individual view. can put somewhere else
    # if view == "A2C":
    #     if rotated_coords[2][0] > rotated_coords[1][0]:
    #         rotated_image = RotateImage.h_flip(rotated_image)
    #         rotated_coords[:, 0] = rotated_image.width - rotated_coords[:, 0]

    return rotated_image, rotated_coords
