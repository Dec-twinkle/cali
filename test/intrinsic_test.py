# -*- coding:utf-8 -*-
# @time: 
# @author:张新新
# @email: 1262981714@qq.com
from board.apriltagboard import AprilTagBoard as AprilTagBoard
from board import utils
from PIL import Image
import os
import cv2
import numpy as np

def getImgList(root_dir):
    file_list = os.listdir(root_dir)
    rgb_list = []
    for file in file_list:
        rgb_list.append(os.path.join(root_dir,file))
    rgb_list.sort()
    return rgb_list

def main():
    board = AprilTagBoard("../config/apriltag_lab.yml", "../config/tagId_lab.csv")
    imgsize = tuple([640,480])
    root_dir = "../data/caliration_11_7"
    img_list = getImgList(root_dir+"/color")
    depth_list = getImgList(root_dir+"/depth")
    if len(img_list) != len(depth_list):
        print("numer of img and depth not same")
        return 0
    objpoints_list = []
    imgpoints_list = []
    extrinsic_list = []
    for img_path in img_list:
        img = cv2.imread(img_path)
        # tags = board.detectTags(img)
        flag,objpoints, imgpoints = board.getObjImgPointList(img)
        if not flag:
            continue
        objpoints_list.append(objpoints)
        imgpoints_list.append(imgpoints)
    rme,intrinsic,dist = board.intrinsic(imgpoints_list,objpoints_list,imgsize)
    print("before opt rme:",rme)
    objpoints_list_acc = []
    imgpoints_list_acc = []
    depth_points_list = []
    for i in range(len(depth_list)):
        depth_img = cv2.imread(depth_list[i],-1)
        imgpoints_acc, objpoints_acc, depth_points = utils.get_imgpoint_depth(imgpoints_list[i],objpoints_list[i],depth_img)
        objpoints_list_acc.append(objpoints_acc)
        imgpoints_list_acc.append(imgpoints_acc)
        depth_points_list.append(depth_points)
    intrinsic, dist = board.intrinsic_depth_opt(objpoints_list_acc,imgpoints_list_acc,depth_points_list,
                                                              intrinsic,dist)
    for i in range(len(imgpoints_list_acc)):
        flag,extrinsic = board.extrisic_depth(objpoints_list_acc[i],imgpoints_list_acc[i],depth_points_list[i],
                                                       intrinsic,dist)
        extrinsic_opt = board.extrinsic_opt(intrinsic,dist,extrinsic,imgpoints_list_acc[i],objpoints_list_acc[i])
        extrinsic_list.append(extrinsic_opt)
    rme = board.RME_each_pic(intrinsic,dist,extrinsic_list,imgpoints_list_acc,objpoints_list_acc)
    print("after opt rme",rme)
    fs = cv2.FileStorage(os.path.join(root_dir,"intrinsic.yml"),cv2.FileStorage_WRITE)
    fs.write("intrinsic",intrinsic)
    fs.write("dist",dist)
    fs.write("rme",np.mean(rme))
    fs.release()



if __name__=="__main__":
    main()










