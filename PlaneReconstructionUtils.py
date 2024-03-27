import os
import numpy as np
import time
import math
import argparse
import random
import itertools
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import vtk
from vtk.util.numpy_support import vtk_to_numpy
import pydicom as dicom
import nrrd
import subprocess
# import cupyx.scipy.ndimage
# import cupy as cp
from scipy.ndimage import map_coordinates
from scipy.ndimage import rotate
from scipy import ndimage
from scipy.interpolate import RegularGridInterpolator, interp2d
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.transforms import Affine2D
import mpl_toolkits.axisartist.floating_axes as floating_axes
from mpl_toolkits.mplot3d import Axes3D
# import torch
# from torch.utils.data import DataLoader
import logging
# import cv2
from itertools import combinations

#### Data Utils #####
def normalize_echo(data):
    max_echo = data.max()
    min_echo = data.min()
    mean_echo = (max_echo+min_echo)/2.0
    scale_echo = (max_echo-min_echo)/2.0
    return (data-mean_echo)/scale_echo

# Pad 3d np array data
def pad3d(data: np.ndarray):
    max_length = max(data.shape)
    out_size = [max_length, max_length, max_length]
    pad_width = np.array([[0, 0], [0, 0], [0, 0]])
    offsets = np.array([0, 0, 0])
    for d in range(3): # pad in all 3 dimensions
        before = (out_size[d] - data.shape[d]) // 2 # difference floored. 128-233 = -105
        after = out_size[d] - data.shape[d] - before    # the other part. after >= before
        pad_width[d] = [before, after]
    return np.pad(data, pad_width, 'constant'), pad_width, max_length

# Pad entire 4d np array data
def pad4d(data: np.ndarray):
    time = data.shape[0]
    max_length = max(data.shape[1:])
    out_size = [time, max_length, max_length, max_length]
    pad_width = np.array([[0,0], [0, 0], [0, 0], [0, 0]])
    offsets = np.array([0, 0, 0])
    for d in range(3): # pad in all 3 dimensions
        before = (out_size[d+1] - data.shape[d+1]) // 2 # difference floored. 128-233 = -105
        after = out_size[d+1] - data.shape[d+1] - before    # the other part. after >= before
        pad_width[d+1] = [before, after]
    return np.pad(data, pad_width, 'constant'), pad_width, max_length

# Retrieve landmark by calculating "hottest" point from each 3d volume
# def get_landmark_from_heatmap(heatmap):

#     bs, cs, a, b, c = heatmap.shape
#     heatmap = heatmap.view(bs, cs, -1)
#     index = torch.argmax(heatmap, dim=2) # (bs, 6)
#     x, y, z = index//(b*c), (index % (b*c))//c, (index % (b*c))%c
#     x, y, z = x.cpu(), y.cpu(), z.cpu()
#     combined_xyz = np.dstack((x, y, z))

#     return combined_xyz

# # Convert 4d Dicom data to 4d NRRD data
# def dicom_4d_to_nrrd_4d(dicom_filePath):
#     t1 = time.perf_counter()

#     ds = dicom.read_file(dicom_filePath, stop_before_pixels=True)
#     columns = ds.Columns
#     rows = ds.Rows
#     slices = ds[(0x3001,0x1001)].value # private tag!
#     spacing = (
#             ds.PhysicalDeltaX * 10,
#             ds.PhysicalDeltaY * 10,
#             ds[(0x3001,0x1003)].value * 10 # private tag!
#             )
#     frames  = int(ds.NumberOfFrames)
#     imageComponents = frames
#     frameTimeMsec = ds.FrameTime
#     pixelShape = (frames, slices, rows, columns)
#     logging.info(f'DICOM file shape: {pixelShape}')
#     pixelSize = pixelShape[0] * pixelShape[1] * pixelShape[2] * pixelShape[3]
#     totalFileSize = os.path.getsize(dicom_filePath)
#     headerSize = totalFileSize-pixelSize

#     image4D = np.zeros((frames, columns, rows, slices))

#     for frame in range(frames): #frames

#         imgReader = vtk.vtkImageReader()
#         imgReader.SetFileDimensionality(3)
#         imgReader.SetFileName(dicom_filePath)
#         imgReader.SetNumberOfScalarComponents(1)
#         imgReader.SetDataScalarTypeToUnsignedChar()
#         imgReader.SetDataExtent(0,columns-1, 0,rows-1, 0,slices-1)
#         imgReader.SetHeaderSize(headerSize+frame*slices*rows*columns)
#         imgReader.FileLowerLeftOn()
#         imgReader.Update()

#         timeStampSec = "{:.3f}".format(frame * frameTimeMsec * 0.001)

#         img = imgReader.GetOutput()
#         imageArray = vtk_to_numpy(img.GetPointData().GetScalars()).reshape(pixelShape[1:])

#         imageArray = np.rot90(imageArray, k=-1, axes = (0, 2))
#         imageArray = np.flip(imageArray, axis = 1)

#         image4D[frame] = imageArray
#         #print('frame '+str(frame)+' done')

#     logging.info(f'Frame Time (ms)): {frameTimeMsec}')
#     logging.info(f'np.array shape:, {image4D.shape}, {type(image4D)}')


#     t2 = time.perf_counter()
#     # print('time for dicom to array: ', t2-t1)

#     # pyplot.imshow(imageArray[:,88,:],cmap='gray')
#     # pyplot.show()

#     logging.info(f'inter spacing: {spacing}')
#     temp = [1, spacing[0], spacing[1], spacing[2]]
#     spacing4D = np.array(temp)

#     # if not os.path.exists(nrrd_save_path):
#     #     os.makedirs(nrrd_save_path)

#     new_data_array = np.empty(np.rint(image4D.shape*spacing4D).astype(int), dtype=np.float64)

#     # this takes longer then for-loop operation. this:5s. for-loop: 2.5s
#     # new_data_array = cupyx.scipy.ndimage.zoom(cp.array(image4D), spacing4D).get()
#     for t in range(frames): #new_data_array.shape[0]
#         #new_data_array[t,:,:,:] = ndimage.zoom(image4D[t,:,:,:], spacing4D[1:])
#         new_data_array[t,:,:,:] = cupyx.scipy.ndimage.zoom(cp.array(image4D[t,:,:,:], dtype=cp.float64), spacing4D[1:], output=cp.float64).get()
#         #print('frame ' + str(t) + ' normalized')
   
#     new_data_array[new_data_array>254.5] = 255
#     new_data_array[new_data_array<0.5] = 0
#     new_data_array = new_data_array.astype(np.uint8)

#     t3 = time.perf_counter()
#     logging.info(f'time to normalize array: {t3-t2}')

#     logging.info(f'Nrrd obj: {new_data_array.shape}')

#     # for t in range(frames): #new_data_array.shape[0]
#     #     nrrd.write(os.path.join(nrrd_save_path, 't_' + str(t)+'.seq.nrrd'), new_data_array[t,:,:,:])
#     #     #print('frame ' + str(t) + ' saved')
#     # t35 = time.perf_counter()
#     # print('time to save time slices: ', t35-t3)

#     return new_data_array, frameTimeMsec


### Plane reconstruction Utils ###
# Crop image to remove useless black background
def CropImageAndReturnPadding(img, coords, spacing=5):

    coords = np.array(coords)

    # img = img + 0.0 # remove -0.0
    indices = np.where(img > 1e-3)
    if all(array.size == 0 for array in indices):
        logging.error("Can't handle empty image")
        1/0
        return img, coords
    min_y, max_y = np.min(indices[0]), np.max(indices[0])
    min_x, max_x = np.min(indices[1]), np.max(indices[1])

    min_y -= spacing
    max_y += spacing
    min_x -= spacing
    max_x += spacing

    # Ensure that the bounding box remains within the image boundaries
    min_y = max(0, min_y)
    max_y = min(img.shape[0] - 1, max_y)
    min_x = max(0, min_x)
    max_x = min(img.shape[1] - 1, max_x)

    # Crop the original image using the expanded bounding box
    cropped_image = img[min_y:max_y, min_x:max_x]

    coords[:, 0] = coords[:, 0] - min_x
    coords[:, 1] = coords[:, 1] - min_y

    return cropped_image, coords, min_y, max_y, min_x, max_x

# Crop image to remove useless black background
def CropImageWithGivenPadding(img, coords, min_y, max_y, min_x, max_x, spacing=50):

    # img = img + 0.0 # remove -0.0
    indices = np.where(img > 1e-3)
    if all(array.size == 0 for array in indices):
        print("Can't handle empty image")
        1/0
        return img, coords

    # Crop the original image using the expanded bounding box
    cropped_image = img[min_y:max_y, min_x:max_x]

    coords[:, 0] = coords[:, 0] - min_x
    coords[:, 1] = coords[:, 1] - min_y

    return cropped_image, coords

# find the 3 best landmarks
def ransac_landmarks(input_landmarks):
    # input_landmarks: shape (landmark_count, 3)

    # print("input_landmarks: ", input_landmarks)
    input_indices = range(0, input_landmarks.shape[0])
    indices_to_remove = np.where(np.all(input_landmarks == 0, axis=1))[0]
    valid_indices = np.delete(input_indices, indices_to_remove, axis=0)
    # print("valid_indices: ", valid_indices)

    best_landmarks = []
    best_indicies = []

    min_distance = 128

    # Generate all possible combinations of landmarks
    all_combinations_indices = combinations(valid_indices, 3)

    for sample_indices in all_combinations_indices:

        sampled_landmarks = input_landmarks[np.array(sample_indices)]

        # Calculate the plane equation for the current combination
        A, B, C, D = get_plane_equation_from_points(sampled_landmarks[0], sampled_landmarks[1], sampled_landmarks[2])

        if A == B == C == D == 0:
            logging.warning(f'Case of straight line. Ignore this combination')
            continue

        # Calculate the distances from each point to the plane
        distances = np.sum(np.abs(A * input_landmarks[valid_indices, 0] + B * input_landmarks[valid_indices, 1] + C * input_landmarks[valid_indices, 2] + D) / np.sqrt(A**2 + B**2 + C**2))

        # print(sampled_landmarks[0], sampled_landmarks[1], sampled_landmarks[2], " = distances: ", distances)
        if distances < min_distance:
            min_distance = distances
            best_landmarks = sampled_landmarks
            best_indicies = sample_indices

    # print("best_landmarks: ", best_landmarks)
    if len(list(best_indicies)) == 0:
        print("ERROR: No valid points can be located")
        1/0

    logging.info(f'best_indicies: {list(best_indicies)}')
    return list(best_indicies)

# Filter out the most useful & accurate 3 landmarks for plane reconstruction
def IdentifyBestLandmarks(landmarks, view):
    if view == "A2C":
        return [0, 1, 2]
    if view == "A4C":
        return ransac_landmarks(landmarks)
        # return [0, 1, 2]
    if view == "ALAX":
        return ransac_landmarks(landmarks)
    if view == "SAXA":
        # landmarks[:, 2] = np.mean(landmarks[:, 2]) # TODO: hardcode approach
        return [0, 1, 2]
    if view == "SAXB":
        return [0, 1, 3]
    if view == "SAXM":
        return ransac_landmarks(landmarks)
        # return [1, 3, 5] # 1, 3, 5 > 10, 13, 27
    if view == "SAXMV":
        return ransac_landmarks(landmarks)
        # return [0, 1, 5]
    logging.error('View name does not exist!')
    return [0, 1, 2]

# ndimage.rotate angle rotates anticlockwise: TODO: coordinates are not correct, rotation correct but position incorrect
def RotateImageAndCoordinates(image, coordinates, rotation_angle):

    if coordinates.shape[1]  == 3:
        coordinates = coordinates[:, 0:1]

    # Calculate the center of the image
    center = np.array([(image.shape[0] - 1) / 2, (image.shape[1] - 1) / 2])

    # Rotate the image
    rotated_image = rotate(image, rotation_angle, reshape=True)

    # Rotate the coordinates
    rotated_coordinates = np.dot(coordinates - center, np.array([[np.cos(np.deg2rad(rotation_angle)), -np.sin(np.deg2rad(rotation_angle))],
                                                                [np.sin(np.deg2rad(rotation_angle)), np.cos(np.deg2rad(rotation_angle))]])) + center
    return rotated_image, np.array(rotated_coordinates)

def RotateCoordinates(rotated_image, coords, angle):

    coords = np.array(coords)

    # Rotate the coordinates
    center_x = rotated_image.shape[1] // 2
    center_y = rotated_image.shape[0] // 2

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
    
    return np.array(rotated_coords)

# 'A2C': [0, 5, 25],
# 'A4C': [1, 2, 14, 21, 22, 31],
# A4C-LV apex, A4C-TV tip, Lateral mitral annulus, MV tip, Medial mitral annulus, Tricuspid annulus.
# 'SAXA': [12, 28, 29],
# 'SAXB': [8, 9, 23, 30], # 0, 1, 3
# 'ALAX': [3, 4, 7, 24], # 1, 2, 3
# 'SAXM': [6, 10, 11, 13, 26, 27], # 1, 3, 5
def ViewSpecificRotations(image, coords, view):
    
    if view == "A2C": # Left To Right: Posteromedial mitral annulus(25) > Anterolateral mitral annulus(5)
        if coords[2][0] > coords[1][0]:
            image = np.fliplr(image)
            coords[:, 0] = image.shape[1] - coords[:, 0]
            logging.info("Perform view specific l/r flip")
    elif view =="A4C": # Tricuspid annulus(31) ----> Lateral mitral annulus(14)
        if coords[5][0] > coords[2][0]:
            image = np.fliplr(image)
            coords[:, 0] = image.shape[1] - coords[:, 0]
            logging.info("Perform view specific l/r flip")
    elif view =="ALAX": # 'ALAX': [3, 4, 7, 24], # 1, 2, 3
        if coords[3][0] > coords[2][0]: # if Posterior mitral annulus(24) > Aortic annulus(7)
            image = np.fliplr(image)
            coords[:, 0] = image.shape[1] - coords[:, 0]
            logging.info("Perform view specific l/r flip")
    elif view =="SAXB": 
        if coords[2][0] > coords[0][0]: # if SAXB-TV tip(30) > Center of AV(8)
            image = np.fliplr(image)
            coords[:, 0] = image.shape[1] - coords[:, 0]
            logging.info("Perform view specific l/r flip")

    elif view =="SAXM": # 'SAXM': [6, 10, 11, 13, 26, 27], # 1, 3, 5
        # rotate image so RV(27) and LV(13) form horizontal line
        dir_vector = coords[3] - coords[5]
        angle = np.arctan2(dir_vector[1], dir_vector[0]) * 180.0 / np.pi
        image, coords = RotateImageAndCoordinates(image, coords, angle)

        # check for vertical flip
        if coords[3][1] > coords[2][1]: # if LV(13) > IW(11)
            image = np.flipud(image)
            coords[:, 1] = image.shape[0] - coords[:, 1]
            logging.info("Perform view specific u/d flip")

    elif view =="SAXMV": # 'SAXMV': [15, 16, 17, 18, 19, 20], # 0, 1, 5
        # rotate image so MV anterior leaflet  A3(16) and MV posterior leaflet P1(18) form horizontal line
        dir_vector = coords[3] - coords[1]
        angle = np.arctan2(dir_vector[1], dir_vector[0]) * 180.0 / np.pi
        image, coords = RotateImageAndCoordinates(image, coords, angle)

        # check for vertical flip
        if coords[2][1] > coords[5][1]: # if MV anterior leaflet  A1(17) > MV posterior leaflet P3(20)
            image = np.flipud(image)
            coords[:, 1] = image.shape[0] - coords[:, 1]
            logging.info("Perform view specific u/d flip")

    elif view == "SAXA":
        pass


    return image, coords


#### Geometry Utils #####

# Get Plane equation from 3 points
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

def normalizeLength(x) :
    # print(x.shape)
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
    if cos == 1:
        R = np.eye(3)  # Identity matrix (no rotation)
    else:
        cross = np.cross(n1, n2)
        cx, cy, cz = cross
        k = (1 - cos) / ((1 + cos) * (1 - cos))
        
        R = np.array([
            [cx * cx * k + cos, cy * cx * k - cz, cz * cx * k + cy],
            [cx * cy * k + cz, cy * cy * k + cos, cz * cy * k - cx],
            [cx * cz * k - cy, cy * cz * k + cx, cz * cz * k + cos],
        ])
        
    # Compose 4x4 transformation matrix
    M = np.eye(4)
    M[0:3,3] = t
    M[:3,:3] = R

    return M

def PlaneBoundsIntersectionsLines (n, pos, dim):
    # From https://stackoverflow.com/a/73355110/11956857
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

def CheckNormalAxis(normal):
    if abs(normal[0]) == 1:
        logging.info("The normal is aligned with the x-axis.")
        return 0
    elif abs(normal[1]) == 1:
        logging.info("The normal is aligned with the x-axis.")
        return 1
    elif abs(normal[2]) == 1:
        logging.info("The normal is aligned with the x-axis.")
        return 2
    else:
        return -1



#### Core Utils #####
# Find Normal vector from points of view. Will also apply filtering to coordinates
def FindNormalByCoords(coords, view, truth=False, all_landmarks=None):

    # coords: ndarray (ls, 3)
    logging.info(f'FindNormalByCoords: {coords} in view {view}')

    # Pick 3 best coordinates         
    best_indexes = IdentifyBestLandmarks(coords, view)
        
    if view == 'SAXA':
        # go to a4c, obtain points 0 and 4 = global 1(A4C-LV apex) and 22(Medial mitral annulus)
        saxa_normal = [0, 0, 1]
        if all_landmarks is not None:
            if (1 in all_landmarks) and (22 in all_landmarks):
                saxa_normal = all_landmarks[22] - all_landmarks[1]
        logging.info(f'SAXA Normal: {saxa_normal}')
        return np.array(saxa_normal), np.array(coords), best_indexes

    best_pred_corrds = coords[best_indexes, :] # only pick 3 landmarks
    p0, p1, p2 = best_pred_corrds[0:3]
    a, b, c, d = get_plane_equation_from_points(p0, p1, p2)

    # check if straight line. TODO: can be removed if everything works
    if a == b == c == d == 0:
        logging.error('ERROR: THIS SHOULD NOT BE CALLED!!!!!!!!!!!!!!')
        1/0

    return np.array([a, b, c]), best_pred_corrds, best_indexes

# Should only be called on 1 frame to get the following info
# retrun vs, coords_2d, coords_indexes, up_vector_2d, isFlat, axis, axis_index, inslice_coords_vrf, size_slice_x, size_slice_y
def FindVisualFromCoordsOnce(coords, volume, view, truth=False, all_landmarks=None):
    normal, best_coords, coords_indexes = FindNormalByCoords(coords, view, truth, all_landmarks)
    logging.info(f'FindVisualFromCoordsOnce: {best_coords} in view {view}')
    logging.info(coords_indexes)
    # print("Calculated Plane Normal: ", normal)
    normal = normal/np.linalg.norm(normal) # normalize
    # print("Normalized normal: ", normal)
    pos = best_coords[0]
    # print("best_coords[0] - best_coords[1]: ", (best_coords[0] - best_coords[1]))    
    # print("best_coords[0] - best_coords[2]: ", (best_coords[0] - best_coords[2]))    
    # print("best_coords[1] - best_coords[2]: ", (best_coords[1] - best_coords[2]))

    # Perfectly Horizontal/Vertical Plane cases
    if(CheckNormalAxis(normal) >= 0):
        logging.info("Horizontal/Vertical Plane")
        axis = CheckNormalAxis(normal)
        axis_index = coords[coords_indexes[0]][axis]
        logging.info(f'The axis index: {axis_index}')
        if axis == 0: 
            visual = volume[int(axis_index), :, :]
            coords_2d = [landmark[1:] for landmark in coords]
            up_vector_2d = [0, 0, 1.0]
            # Need invert pts y-axis
            coords_2d = [[pts[0], 128-pts[1]] for pts in coords_2d]
        elif axis == 1:
            visual = volume[:, int(axis_index), :]
            coords_2d = [[landmark[0], landmark[2]] for landmark in coords]
            up_vector_2d = [0, 0, 1.0]
            # Need invert pts y-axis
            coords_2d = [[pts[0], 128-pts[1]] for pts in coords_2d]
        elif axis == 2:
            visual = volume[:, :, int(axis_index)]
            coords_2d = [landmark[:2] for landmark in coords]
            up_vector_2d = [1.0, 0, 0]

        coords_2d = np.array(coords_2d)
        # print('displacement_pts_in_2d: ', displacement_pts_in_2d)
        # print("result: ", visual.shape, cross_sectional_slice.min(), cross_sectional_slice.max())
        return visual, coords_2d, coords_indexes, up_vector_2d, normal, True, axis, axis_index, None, None, None

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

    # displace the coordinates
    coords_2d = new_pos - origin_corner_slice

    visual = map_coordinates(volume, inslice_coords_vrf.T, order=1, mode='constant', cval=-1.0)
    visual = visual.reshape(size_slice_x, size_slice_y)

    up_coord1 = [0, 0, 1] # this coordinate system is same for "pos"
    pt_arr = np.concatenate((up_coord1, np.ones((1,))) ,axis = 0).reshape((4,1))
    up_in_2d_1 = np.matmul(np.linalg.inv(Pose_slice_origin_cspecial), pt_arr)
    up_in_2d_1 = up_in_2d_1[:-1].reshape(3, )
    # print("up_in_2d_1:", up_in_2d_1)

    up_coord2 = [0, 0, 64] # this coordinate system is same for "pos" 
    pt_arr = np.concatenate((up_coord2, np.ones((1,))) ,axis = 0).reshape((4,1))
    up_in_2d_2 = np.matmul(np.linalg.inv(Pose_slice_origin_cspecial), pt_arr)
    up_in_2d_2 = up_in_2d_2[:-1].reshape(3, )    
    # print("up_in_2d_2:", up_in_2d_2)

    up_vector_2d = up_in_2d_2 - up_in_2d_1
    logging.info(f'up_in_2d: {up_vector_2d}')

    return visual, coords_2d, coords_indexes, up_vector_2d, normal, False, -1, -1, inslice_coords_vrf, size_slice_x, size_slice_y

# Faster implmentation
def FindVisualFromGivenInfo(volume, isFlat, axis, axis_index, inslice_coords_vrf, size_slice_x, size_slice_y):
    if isFlat == True:
        if axis == 0: 
            visual = volume[int(axis_index), :, :]
        elif axis == 1:
            visual = volume[:, int(axis_index), :]
        elif axis == 2:
            visual = volume[:, :, int(axis_index)]
        return visual
    else:
        visual = map_coordinates(volume, inslice_coords_vrf.T, order=1, mode='constant', cval=-1.0)
        visual = visual.reshape(size_slice_x, size_slice_y)
        return visual



# Extract cross sectional view of volume from given coords
def FindVisualFromCoords(coords, volume, view, truth=False, all_landmarks=None):

    normal, best_coords, coords_indexes = FindNormalByCoords(coords, view, truth, all_landmarks)
    logging.info(f'FindVisualFromCoords: {best_coords} in view {view}')
    logging.info(coords_indexes)
    # print("Calculated Plane Normal: ", normal)
    normal = normal/np.linalg.norm(normal) # normalize
    # print("Normalized normal: ", normal)
    pos = best_coords[0]
    # print("best_coords[0] - best_coords[1]: ", (best_coords[0] - best_coords[1]))    
    # print("best_coords[0] - best_coords[2]: ", (best_coords[0] - best_coords[2]))    
    # print("best_coords[1] - best_coords[2]: ", (best_coords[1] - best_coords[2]))

    # Perfectly Horizontal/Vertical Plane cases
    if(CheckNormalAxis(normal) >= 0):
        logging.info("Horizontal/Vertical Plane")
        axis = CheckNormalAxis(normal)
        axis_index = coords[coords_indexes[0]][axis]
        logging.info(f'The axis index: {axis_index}')
        if axis == 0: 
            cross_sectional_slice = volume[int(axis_index), :, :]
            coords_2d = [landmark[1:] for landmark in coords]
            up_vector_2d = [0, 0, 1.0]
            # Need invert pts y-axis
            coords_2d = [[pts[0], 128-pts[1]] for pts in coords_2d]
        elif axis == 1:
            cross_sectional_slice = volume[:, int(axis_index), :]
            coords_2d = [[landmark[0], landmark[2]] for landmark in coords]
            up_vector_2d = [0, 0, 1.0]
            # Need invert pts y-axis
            coords_2d = [[pts[0], 128-pts[1]] for pts in coords_2d]
        elif axis == 2:
            cross_sectional_slice = volume[:, :, int(axis_index)]
            coords_2d = [landmark[:2] for landmark in coords]
            up_vector_2d = [1.0, 0, 0]

        coords_2d = np.array(coords_2d)
        # print('displacement_pts_in_2d: ', displacement_pts_in_2d)
        # print("result: ", cross_sectional_slice.shape, cross_sectional_slice.min(), cross_sectional_slice.max())
        return cross_sectional_slice, coords_2d, coords_indexes, up_vector_2d, normal

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

    # displace the coordinates
    coords_2d = new_pos - origin_corner_slice

    result = map_coordinates(volume, inslice_coords_vrf.T, order=1, mode='constant', cval=-1.0)
    # print("Map Coordinates time: ", end_time-start_time)
    result = result.reshape(size_slice_x, size_slice_y)
    # print("result: ", type(result))
    # print("result: ", result.shape, result.min(), result.max())
    # print(displacement_pts_in_2d.shape)

    up_coord1 = [0, 0, 1] # this coordinate system is same for "pos"
    pt_arr = np.concatenate((up_coord1, np.ones((1,))) ,axis = 0).reshape((4,1))
    up_in_2d_1 = np.matmul(np.linalg.inv(Pose_slice_origin_cspecial), pt_arr)
    up_in_2d_1 = up_in_2d_1[:-1].reshape(3, )
    # print("up_in_2d_1:", up_in_2d_1)

    up_coord2 = [0, 0, 64] # this coordinate system is same for "pos" 
    pt_arr = np.concatenate((up_coord2, np.ones((1,))) ,axis = 0).reshape((4,1))
    up_in_2d_2 = np.matmul(np.linalg.inv(Pose_slice_origin_cspecial), pt_arr)
    up_in_2d_2 = up_in_2d_2[:-1].reshape(3, )    
    # print("up_in_2d_2:", up_in_2d_2)

    up_vector_2d = up_in_2d_2 - up_in_2d_1
    logging.info(f'up_in_2d: {up_vector_2d}')

    return result, coords_2d, coords_indexes, up_vector_2d, normal

# Fix rotations of view after FindVisualFromCoords(). must be used together
def HandleRotationsNumpy(numpy_img, coords, coords_indexes, up_vector_of_2d_in_3d_space, view):

    logging.info(f'HandleRotationsNumpy View:  {view} {coords} up_vector_of_2d_in_3d_space: {up_vector_of_2d_in_3d_space}')
    # print(coords)

    # rows, column
    # y, x.
    # horizontal line at the top
    # numpy_img[10, :] = 255

    # Horizontal Plane
    if(up_vector_of_2d_in_3d_space[1] == 0):
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # print("Vertical Plane:") # TODO
        logging.warning("Horizontal Plane")
        # SAXA-LV apex
        # print(coords[2])
        rotated_image = rotate(numpy_img, 90, reshape=False)
        # rotated_coords = RotateCoordinates(rotated_image, coords, -90)
        return rotated_image, coords

    
    # slop of x and y axis
    slope = up_vector_of_2d_in_3d_space[0] / up_vector_of_2d_in_3d_space[1]
    logging.debug(f'slope: {slope}')

    angle = math.degrees(math.atan(1 / slope))
    
    # for handling inverted cases. will also h flip later
    if up_vector_of_2d_in_3d_space[0] > 0:
        angle += 180

    #
    if slope == 0 and up_vector_of_2d_in_3d_space[1] >= 0:
        angle = -angle
        
    # print("angle: ", angle)
    rotated_image = numpy_img
    rotated_coords = coords

    rotated_image = rotate(numpy_img, -angle, reshape=False)
    rotated_coords = RotateCoordinates(rotated_image, coords, angle)

    # for handling inverted cases # this should not be needed. flip lr cases handle for view specific
    # if up_vector_of_2d_in_3d_space[0] > 0:
    #     print("ERROR: check why this is called!!!")
    #     rotated_image = np.fliplr(rotated_image)
    #     rotated_coords[:, 0] = rotated_image.shape[1] - rotated_coords[:, 0]

    return rotated_image, rotated_coords