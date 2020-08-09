#-*- coding:utf-8 -*-
# @time: 
# @author:张新新
# @email: 1262981714@qq.com
import numpy as np
import cv2
from calibration_utils.cali_utils import base_utils


class chessboard_cali_utils(base_utils):
    @staticmethod
    def extrinsic(imgpoints, objpoints, intrinsic, dist):
        n = objpoints.shape[0]
        realcoor = np.append(objpoints, np.zeros([n, 1]), 1)
        revl, rvec, tvec = cv2.solvePnP(realcoor, imgpoints, intrinsic, dist)
        R = cv2.Rodrigues(rvec)[0]
        return np.append(np.append(R, tvec, 1), np.array([[0, 0, 0, 1]]), 0)
