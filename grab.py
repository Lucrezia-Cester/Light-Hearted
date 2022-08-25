# ===============================================================================
#    This sample illustrates how to grab and process images using the CInstantCamera class.
#    The images are grabbed and processed asynchronously, i.e.,
#    while the application is processing a buffer, the acquisition of the next buffer is done
#    in parallel.
#
#    The CInstantCamera class uses a pool of buffers to retrieve image data
#    from the camera device. Once a buffer is filled and ready,
#    the buffer can be retrieved from the camera object for processing. The buffer
#    and additional image data are collected in a grab result. The grab result is
#    held by a smart pointer after retrieval. The buffer is automatically reused
#    when explicitly released or when the smart pointer object is destroyed.
# ===============================================================================
from pypylon import pylon
from pypylon import genicam
import numpy as np
from matplotlib import pyplot as plt
import sys

# Number of images to be grabbed.
countOfImagesToGrab = 4000

# The exit code of the sample application.
exitCode = 0

try:
    # Create an instant camera object with the camera device found first.
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    camera.Open()
    # Change acquisition frame rate
    camera.ExposureTime.SetValue(100)
    camera.Width = (100)
    camera.Height = (100)
    camera.AcquisitionFrameRateEnable = True
    camera.AcquisitionFrameRate = 500
    # Print the model name of the camera.
    print("Using device ", camera.GetDeviceInfo().GetModelName())

    # demonstrate some feature access
    new_width = camera.Width.GetValue() - camera.Width.GetInc()
    if new_width >= camera.Width.GetMin():
        camera.Width.SetValue(new_width)

    # The parameter MaxNumBuffer can be used to control the count of buffers
    # allocated for grabbing. The default value of this parameter is 10.
    camera.MaxNumBuffer = 1

    # Start the grabbing of c_countOfImagesToGrab images.
    # The camera device is parameterized with a default configuration which
    # sets up free-running continuous acquisition.
    camera.StartGrabbingMax(countOfImagesToGrab)

    # Camera.StopGrabbing() is called automatically by the RetrieveResult() method
    # when c_countOfImagesToGrab images have been retrieved.
    results = []
    while camera.IsGrabbing():
        # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
        grabResult = camera.RetrieveResult(50, pylon.TimeoutHandling_ThrowException)

        # Image grabbed successfully?
        if grabResult.GrabSucceeded():
            # Access the image data.
            #print("Set value: ",
                  #"Exposuretime:", camera.ExposureTime.GetValue(), "AcquisitionFrameRate:",
            # camera.AcquisitionFrameRate.GetValue())

            #print("SizeX: ", grabResult.Width)
            #print("SizeY: ", grabResult.Height)
            img = grabResult.Array
            img = np.array(img)
            #print('this is size', img.shape)
            #plt.imshow(img)
            #plt.show()
            # print("Gray value of first pixel: ", img[0, 0])
        else:
            print("Error: ", grabResult.ErrorCode, grabResult.ErrorDescription)
        grabResult.Release()
        results.append(img)
    results=np.array(results)
    print(results.shape)
    print(results)
    camera.Close()


except genicam.GenericException as e:
    # Error handling.
    print("An exception occurred.")
    print(e.GetDescription())
    exitCode = 1



sys.exit(exitCode)

import numpy as np
import cv2
import os

width = 100
hieght = 96
channel = 3


# Syntax: VideoWriter_fourcc(c1, c2, c3, c4) # Concatenates 4 chars to a fourcc code
#  cv2.VideoWriter_fourcc('M','J','P','G') or cv2.VideoWriter_fourcc(*'MJPG)

fourcc = cv2.VideoWriter_fourcc(*'MP42')  # FourCC is a 4-byte code used to specify the video codec.
# A video codec is software or hardware that compresses and decompresses digital video.
# In the context of video compression, codec is a portmanteau of encoder and decoder,
# while a device that only compresses is typically called an encoder, and one that only
# decompresses is a decoder. Source - Wikipedia

# Syntax: cv2.VideoWriter( filename, fourcc, fps, frameSize )
video = cv2.VideoWriter('test.mp4', fourcc, float(500), (width, hieght))

for frame_count in range(4000):
    img = np.random.randint(0, 255, (hieght, width, channel), dtype=np.uint8)
    video.write(img)

video.release()