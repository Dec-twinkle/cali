# -*- coding:utf-8 -*-
# @time: 
# @author:张新新
# @email: 1262981714@qq.com
from board.chessboard import ChessBoard
from calibration_utils.chessboard_cali_utils import chessboard_cali_utils
from PIL import Image
import numpy as np
import os
import cv2

def getImgList(root_dir):
    file_list = os.listdir(root_dir)
    rgb_list = []
    depth_list = []
    for file in file_list:
        if file.endswith(".png"):
            rgb_list.append(os.path.join(root_dir,file))
    return rgb_list

def main():
    board = ChessBoard("../config/chessboard_yanzou_0705.yml")
    imgsize = tuple([3840,2748])
    #root_dir = "../data/stereo/dvs"
    root_dir = "D:\\data\\lcy\\data"
    img_list = getImgList(root_dir)
    objpoints_list = []
    imgpoints_list = []
    extrinsic_list = []
    for img_path in img_list:
        img = cv2.imread(img_path)
        print("start to detect pic:",img_path)
        succ, imgpoints,objpoints = board.GetImageAndObjPoint(img,verbose=1)
        if succ:
            objpoints_list.append(objpoints)
            imgpoints_list.append(imgpoints)
    rme, intrinsic, dist = chessboard_cali_utils.intrinsic(imgpoints_list,objpoints_list,imgsize)
    print("start to estimate extrinsic")
    for i in range(len(objpoints_list)):
        extrinsic = chessboard_cali_utils.extrinsic(imgpoints_list[i], objpoints_list[i],intrinsic,dist)
        extrinsic_list.append(extrinsic)
    print("end estimate extrinsic")
    rme,intrinsic,dist,extrinsic_list = chessboard_cali_utils.cameraparam_opt(intrinsic,dist,extrinsic_list,imgpoints_list,objpoints_list)
    print(intrinsic,dist,np.mean(np.abs(rme)))

    savefile = os.path.join(root_dir,"intrinsic.yml")
    fs = cv2.FileStorage(savefile,cv2.FileStorage_WRITE)
    fs.write("intrinsic",intrinsic)
    fs.write("dist",dist)
    fs.write("rme",np.mean(np.abs(rme)))
if __name__ == '__main__':
    main()