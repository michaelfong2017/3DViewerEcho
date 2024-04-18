import glm
import math
import numpy as np


"""
From World to OpenGL, x to x, y to -z, z to y
"""


def find_center_point(points, data_3d_padded_max_length, view=""):
    # Convert points to NumPy array
    points = np.array(points)

    # Calculate the average position of the points
    center_point = np.mean(points, axis=0)

    # print(f"{view} (world coordinates): {np.round(center_point, 2)}")
    gl_point = np.zeros(3)
    gl_point[0] = center_point[0] / data_3d_padded_max_length * 2.0 - 1.0
    gl_point[1] = center_point[2] / data_3d_padded_max_length * 2.0 - 1.0
    gl_point[2] = -1 * (center_point[1] / data_3d_padded_max_length * 2.0 - 1.0)

    # print(f"{view} (OpenGL coordinates): {np.round(gl_point, 2)}")

    return center_point


def check_zero(v, epsilon=1e-5):
    abs_v = glm.abs(v)
    condition = glm.all(glm.lessThan(abs_v, glm.vec3(epsilon)))
    if condition:
        return True
    return False


def euler_rotation_z_to_vector(vector):
    z_axis = glm.vec3(0, 0, 1)  # Z-axis vector

    # Normalize the input vector
    normalized_vector = glm.normalize(vector)

    # Calculate the dot product between the z-axis and the normalized vector
    dot_product = glm.dot(z_axis, normalized_vector)

    # Calculate the angle between the z-axis and the normalized vector
    angle = math.acos(dot_product)

    # Calculate the cross product between the z-axis and the normalized vector
    cross_product = glm.cross(z_axis, normalized_vector)

    if check_zero(cross_product):
        return glm.vec3(0, 0, 0)

    # Normalize the cross product
    normalized_cross_product = glm.normalize(cross_product)

    # Calculate the rotation quaternion around the cross product vector
    rotation_quat = glm.angleAxis(angle, normalized_cross_product)

    # Convert the rotation quaternion to Euler angles
    euler_angles = glm.degrees(glm.eulerAngles(rotation_quat))

    return euler_angles


"""
From World to OpenGL, need to rotate about the OpenGL x-axis by negative 90 degrees first.
"""


def eulerFromNormal(nx, ny, nz, view=""):
    euler_angles = euler_rotation_z_to_vector(glm.vec3(nx, ny, nz))
    # print(f"{view} (world rotation): {np.round(euler_angles, 2)}")
    return euler_angles[0], euler_angles[1], euler_angles[2]


if __name__ == "__main__":
    eulerFromNormal(-0.73126312, 0.67974802, -0.05654096, "A2C")
    eulerFromNormal(-0.04675716, -0.99789615, 0.04491148, "A4C")
    eulerFromNormal(0.70832753, 0.70326805, 0.06071379, "ALAX")
    eulerFromNormal(0, 0, 1, "SAXM")
    eulerFromNormal(0, 0, 1, "SAXMV")

    points = [
        [108.1640625, 101.5078125, 156.421875],
        [128.1328125, 116.484375, 78.2109375],
        [109.828125, 96.515625, 74.8828125],
    ]
    center = find_center_point(points, 213, "A2C")

    points = [
        [103.171875, 108.1640625, 158.0859375],
        [71.5546875, 106.5, 88.1953125],
        [129.796875, 103.171875, 74.8828125],
    ]
    center = find_center_point(points, 213, "A4C")

    points = [
        [101.5078125, 116.484375, 74.8828125],
        [93.1875, 123.140625, 94.8515625],
        [121.4765625, 96.515625, 73.21875],
    ]
    center = find_center_point(points, 213, "ALAX")

    points = [
        [88.1953125, 103.171875, 112.6015625],
        [116.484375, 103.171875, 112.6015625],
        [69.890625, 108.1640625, 112.6015625],
    ]
    center = find_center_point(points, 213, "SAXM")

    points = [
        [111.4921875, 109.828125, 84.3125],
        [104.8359375, 103.171875, 84.3125],
        [111.4921875, 94.8515625, 84.3125],
    ]
    center = find_center_point(points, 213, "SAXMV")


"""
A2C
Received:  [[108.1640625 101.5078125 156.421875 ]
 [128.1328125 116.484375   78.2109375]
 [109.828125   96.515625   74.8828125]]
FindVisualFromCoords:  [[108.1640625 101.5078125 156.421875 ]
 [128.1328125 116.484375   78.2109375]
 [109.828125   96.515625   74.8828125]]  in view  A2C
Calculated Plane Normal:  [-1611.61853027  1498.08526611  -124.60968018]
Normalized normal:  [-0.73126312  0.67974802 -0.05654096]
up_in_2d: [-46.0695765   42.82412524   3.56208066]
result:  <class 'numpy.ndarray'>
HandleRotationsNumpy View:  A2C
slope:  -1.075785582255083
angle:  -42.90909701574056
/home/michael/3DViewerEcho/dicomprocessor.py:83: UserWarning: Starting a Matplotlib GUI outside of the main thread will likely fail.
  pyplot.figure(frame_index * len(view_to_array_2d) + i, figsize=(width * px, height * px))
QObject::startTimer: Timers can only be used with threads started with QThread
Execution time:  0.480527660000007
---------------------------------------------------------------
A4C
Received:  [[103.171875  108.1640625 158.0859375]
 [ 71.5546875 106.5        88.1953125]
 [129.796875  103.171875   74.8828125]
 [121.4765625 108.1640625  81.5390625]
 [ 98.1796875 106.5        76.546875 ]
 [ 61.5703125 109.828125   83.203125 ]]
FindVisualFromCoords:  [[103.171875  108.1640625 158.0859375]
 [ 71.5546875 106.5        88.1953125]
 [129.796875  103.171875   74.8828125]
 [121.4765625 108.1640625  81.5390625]
 [ 98.1796875 106.5        76.546875 ]
 [ 61.5703125 109.828125   83.203125 ]]  in view  A4C
Calculated Plane Normal:  [ -210.4519043  -4491.48669434   202.14459229]
Normalized normal:  [-0.04675716 -0.99789615  0.04491148]
up_in_2d: [ 2.94570084 62.86745749  2.82942318]
result:  <class 'numpy.ndarray'>
HandleRotationsNumpy View:  A4C
slope:  0.046855733662145654
angle:  267.31732630116977
Perform view specific flip
QObject::startTimer: Timers can only be used with threads started with QThread
Execution time:  0.15983039999991888
---------------------------------------------------------------
ALAX
Received:  [[103.171875  109.828125  156.421875 ]
 [101.5078125 116.484375   74.8828125]
 [ 93.1875    123.140625   94.8515625]
 [121.4765625  96.515625   73.21875  ]]
FindVisualFromCoords:  [[101.5078125 116.484375   74.8828125]
 [ 93.1875    123.140625   94.8515625]
 [121.4765625  96.515625   73.21875  ]]  in view  ALAX
Calculated Plane Normal:  [387.67456055 384.90545654  33.22924805]
Normalized normal:  [0.70832753 0.70326805 0.06071379]
up_in_2d: [-44.62463437 -44.30588699   3.82496866]
result:  <class 'numpy.ndarray'>
HandleRotationsNumpy View:  ALAX
slope:  1.0071942446043163
angle:  44.79463966250513
QObject::startTimer: Timers can only be used with threads started with QThread
Execution time:  0.3523634210000637
---------------------------------------------------------------
SAXM
Received:  [[129.796875  109.828125  114.8203125]
 [ 88.1953125 103.171875  113.15625  ]
 [103.171875   81.5390625 113.15625  ]
 [116.484375  103.171875  114.8203125]
 [104.8359375  88.1953125 111.4921875]
 [ 69.890625  108.1640625 109.828125 ]]
FindVisualFromCoords:  [[ 88.1953125 103.171875  112.6015625]
 [116.484375  103.171875  112.6015625]
 [ 69.890625  108.1640625 112.6015625]]  in view  SAXM
Calculated Plane Normal:  [  0.         -0.        141.2243042]
Normalized normal:  [ 0. -0.  1.]
The normal is aligned with the z-axis.
###############################################
###############################################
Perfectly Horizontal/Vertical Plane
The normal is aligned with the z-axis.
The axis index:  112.6015625
HandleRotationsNumpy View:  SAXM
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Horizontal Plane: Hard-code approach
QObject::startTimer: Timers can only be used with threads started with QThread
Execution time:  0.025664346999747067
---------------------------------------------------------------
SAXMV
Received:  [[111.4921875 109.828125   84.8671875]
 [104.8359375 103.171875   84.8671875]
 [116.484375  116.484375   86.53125  ]
 [123.140625  108.1640625  83.203125 ]
 [119.8125    101.5078125  83.203125 ]
 [111.4921875  94.8515625  83.203125 ]]
FindVisualFromCoords:  [[111.4921875 109.828125   84.3125   ]
 [104.8359375 103.171875   84.3125   ]
 [111.4921875  94.8515625  84.3125   ]]  in view  SAXMV
Calculated Plane Normal:  [ 0.          0.         99.68774414]
Normalized normal:  [0. 0. 1.]
The normal is aligned with the z-axis.
###############################################
###############################################
Perfectly Horizontal/Vertical Plane
The normal is aligned with the z-axis.
The axis index:  84.3125
HandleRotationsNumpy View:  SAXMV
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Horizontal Plane: Hard-code approach
QObject::startTimer: Timers can only be used with threads started with QThread
Execution time:  0.026759087999835174
"""
