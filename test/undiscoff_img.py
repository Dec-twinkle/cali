import cv2
import numpy as np
import os
if __name__ == "__main__":
    root_dir = "../data/stereo/dvs"
    files = os.listdir(root_dir)
    fs2 = cv2.FileStorage(root_dir+'/intrinsic.yml', cv2.FileStorage_READ)
    # R = cv2.cv.Load(root + '/' + png1 + '.yml', name="transform")

    A = fs2.getNode('intrinsic').mat()
    discoff = fs2.getNode('dist').mat()
    fs2.release()

    for file in files:
        if file.endswith(".png"):
        # if file.endswith(".bmp"):
            path = os.path.join(root_dir,file)
            img = cv2.imread(path)
            img_undiscoff = cv2.undistort(img, A, discoff)
            cv2.namedWindow("undistored", 0)
            cv2.imshow("undistored", img_undiscoff)
            cv2.waitKey(0)
            img = cv2.resize(img, (512, 512))
            re = cv2.resize(img_undiscoff, (512, 512))
            h_all = np.hstack((img, re))
            cv2.imshow("undistored", h_all)
            cv2.waitKey(0)


