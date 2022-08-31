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
countOfImagesToGrab = 3000

# The exit code of the sample application.
exitCode = 0

try:
    # Create an instant camera object with the camera device found first.
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    camera.Open()
    # Change acquisition frame rate
    camera.ExposureTime.SetValue(130)
    camera.Width = 100 #(720*16//9)
    camera.Height =100 #(720)
    # 720 * 16 // 9, 720
    camera.AcquisitionFrameRateEnable = True
    camera.AcquisitionFrameRate = 300
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
        grabResult = camera.RetrieveResult(20, pylon.TimeoutHandling_ThrowException)

        # Image grabbed successfully?
        if grabResult.GrabSucceeded():
            # Access the image data.
            #print("Set value: ",
                  #"Exposuretime:", camera.ExposureTime.GetValue(), "AcquisitionFrameRate:",
            # camera.AcquisitionFrameRate.GetValue())

            #print("SizeX: ", grabResult.Width)
            #print("SizeY: ", grabResult.Height)
            img = grabResult.Array
            # import ipdb; ipdb.set_trace()
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
    print('shape',img.shape)
    print(results)
    camera.Close()



except genicam.GenericException as e:
    # Error handling.
    print("An exception occurred.")
    print(e.GetDescription())
    exitCode = 1

#
#
# import cv2
# import numpy
# import os
#
# os.chdir(os.path.expanduser("~/Desktop"))
# shape = (96, 100)
# frame = results
#
# video_name = 'output.avi'
# fps = 500
# video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'XVID'), fps, shape)
#
# for i in range(fps * 5):
#     video.write(frame)
#
# video.release()
#
# cap = cv2.VideoCapture('output.avi')
#
# while (cap.isOpened()):
#     ret, frame = cap.read()
#
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     cv2.imshow('frame', gray)
#
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()


import numpy as np
import cv2
size = 100,100
duration = 2
fps = 25
out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (results.shape[2], results.shape[1]), False)
# for _ in range(fps * duration):
#     data = np.random.randint(0, 256, size, dtype='uint8')
#     out.write(data)

# size =  (720, 1276)
for frame in range(results.shape[0]):
    data = results[frame]
    out.write(data)

out.release()
# sys.exit(exitCode)
