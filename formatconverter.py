import os

# os.environ['CUDA_VISIBLE_DEVICES'] = '3'
import vtk
import numpy as np
import pydicom as dicom
from vtk.util.numpy_support import vtk_to_numpy
import nrrd
from matplotlib import pyplot, cm
from scipy import ndimage
import time
from PIL import Image


def dicom_to_array(dicom_filePath):
    t1 = time.perf_counter()

    ds = dicom.read_file(dicom_filePath, stop_before_pixels=True)
    columns = ds.Columns
    rows = ds.Rows
    slices = ds[(0x3001, 0x1001)].value  # private tag!
    spacing = (
        ds.PhysicalDeltaX * 10,
        ds.PhysicalDeltaY * 10,
        ds[(0x3001, 0x1003)].value * 10,  # private tag!
    )
    frames = int(ds.NumberOfFrames)
    imageComponents = frames
    frameTimeMsec = ds.FrameTime
    pixelShape = (frames, slices, rows, columns)
    print("dicom file shape: ", pixelShape)
    pixelSize = pixelShape[0] * pixelShape[1] * pixelShape[2] * pixelShape[3]
    totalFileSize = os.path.getsize(dicom_filePath)
    headerSize = totalFileSize - pixelSize

    image4D = np.zeros((frames, columns, rows, slices))

    for frame in range(frames):  # frames
        imgReader = vtk.vtkImageReader()
        imgReader.SetFileDimensionality(3)
        imgReader.SetFileName(dicom_filePath)
        imgReader.SetNumberOfScalarComponents(1)
        imgReader.SetDataScalarTypeToUnsignedChar()
        imgReader.SetDataExtent(0, columns - 1, 0, rows - 1, 0, slices - 1)
        imgReader.SetHeaderSize(headerSize + frame * slices * rows * columns)
        imgReader.FileLowerLeftOn()
        imgReader.Update()

        timeStampSec = "{:.3f}".format(frame * frameTimeMsec * 0.001)

        img = imgReader.GetOutput()
        imageArray = vtk_to_numpy(img.GetPointData().GetScalars()).reshape(
            pixelShape[1:]
        )

        imageArray = np.rot90(imageArray, k=-1, axes=(0, 2))
        imageArray = np.flip(imageArray, axis=1)

        image4D[frame] = imageArray
        # print('frame '+str(frame)+' done')

    print("np.array shape:", image4D.shape, type(image4D))

    t2 = time.perf_counter()
    print("time for dicom to array: ", t2 - t1)

    # pyplot.imshow(imageArray[:,88,:],cmap='gray')
    # pyplot.show()

    print("inter spacing: ", spacing)
    temp = [1, spacing[0], spacing[1], spacing[2]]
    spacing4D = np.array(temp)

    # if not os.path.exists(nrrd_save_path):
    #     os.makedirs(nrrd_save_path)

    # new_data_array = np.empty(
    #     np.rint(image4D.shape * spacing4D).astype(int), dtype=np.float64
    # )

    # this takes longer then for-loop operation. this:5s. for-loop: 2.5s
    # new_data_array = cupyx.scipy.ndimage.zoom(cp.array(image4D), spacing4D).get()
    # for t in range(frames):  # new_data_array.shape[0]
    #     new_data_array[t, :, :, :] = ndimage.zoom(image4D[t, :, :, :], spacing4D[1:])
    #     # new_data_array[t, :, :, :] = cupyx.scipy.ndimage.zoom(
    #     #     cp.array(image4D[t, :, :, :], dtype=cp.float64),
    #     #     spacing4D[1:],
    #     #     output=cp.float64,
    #     # ).get()
    #     # print('frame ' + str(t) + ' normalized')

    # new_data_array[new_data_array > 254.5] = 255
    # new_data_array[new_data_array < 0.5] = 0
    # new_data_array = new_data_array.astype(np.uint8)

    # t3 = time.perf_counter()
    # print("time to normalize array: ", t3 - t2)

    # print("Nrrd obj: ", new_data_array.shape)

    # for t in range(frames): #new_data_array.shape[0]
    #     nrrd.write(os.path.join(nrrd_save_path, 't_' + str(t)+'.seq.nrrd'), new_data_array[t,:,:,:])
    #     #print('frame ' + str(t) + ' saved')
    # t35 = time.perf_counter()
    # print('time to save time slices: ', t35-t3)

    return image4D, spacing4D


def pad4d(data: np.ndarray):
    time = data.shape[0]
    max_length = max(data.shape[1:])
    print("max: ", max_length)
    out_size = [time, max_length, max_length, max_length]
    pad_width = np.array([[0, 0], [0, 0], [0, 0], [0, 0]])
    offsets = np.array([0, 0, 0])
    for d in range(3):  # pad in all 3 dimensions
        before = (
            out_size[d + 1] - data.shape[d + 1]
        ) // 2  # difference floored. 128-233 = -105
        after = (
            out_size[d + 1] - data.shape[d + 1] - before
        )  # the other part. after >= before
        pad_width[d + 1] = [before, after]
    return np.pad(data, pad_width, "constant"), pad_width, max_length
