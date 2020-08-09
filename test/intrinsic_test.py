# -*- coding:utf-8 -*-
# @time: 
# @author:张新新
# @email: 1262981714@qq.com
from board.apriltagboard import AprilTagBoard as AprilTagBoard
from calibration_utils.apriltag_cali_utils import apriltag_cali_utils
from calibration_utils.depth_utils import *
from PIL import Image
import os
import cv2

def getImgList(root_dir):
    file_list = os.listdir(root_dir)
    rgb_list = []
    depth_list = []
    for file in file_list:
        if file.endswith("_rgb.jpg"):
            rgb_list.append(os.path.join(root_dir,file))
        elif file.endswith("_depth.png"):
            depth_list.append(os.path.join(root_dir,file))
    return rgb_list,depth_list

def main():
    board = AprilTagBoard("../config/apriltag.yml", "../config/tagId2.csv")
    imgsize = tuple([1280,960])
    root_dir = "D:\\data\\zhongyou\\0807"
    img_list, depth_list = getImgList(root_dir)
    if len(img_list) != len(depth_list):
        print("numer of img and depth not same")
        return 0
    objpoints_list = []
    imgpoints_list = []
    extrinsic_list = []
    for img_path in img_list:
        img = cv2.imread(img_path)
        tags = apriltag_cali_utils.detectTags(board,img)
        objpoints, imgpoints = board.getObjImgPointList(tags)
        objpoints_list.append(objpoints)
        imgpoints_list.append(imgpoints)
    rme,intrinsic,dist = apriltag_cali_utils.intrinsic(imgpoints_list,objpoints_list,imgsize)
    print("before opt rme:",rme)
    objpoints_list_acc = []
    imgpoints_list_acc = []
    depth_points_list = []
    for i in range(len(depth_list)):
        depth_img = Image.open(depth_list[i])
        imgpoints_acc, objpoints_acc, depth_points = get_imgpoint_depth(imgpoints_list[i],objpoints_list[i],depth_img)
        objpoints_list_acc.append(objpoints_acc)
        imgpoints_list_acc.append(imgpoints_acc)
        depth_points_list.append(depth_points)
    intrinsic, dist = apriltag_cali_utils.intrinsic_depth_opt(objpoints_list_acc,imgpoints_list_acc,depth_points_list,
                                                              intrinsic,dist)
    for i in range(len(imgpoints_list_acc)):
        extrinsic = apriltag_cali_utils.extrisic_depth(objpoints_list_acc[i],imgpoints_list[i],depth_points_list[i],
                                                       intrinsic,dist)
        extrinsic_opt = apriltag_cali_utils.extrinsic_opt(intrinsic,dist,extrinsic,imgpoints_list_acc[i],objpoints_list_acc[i])
        extrinsic_list.append(extrinsic_opt)
    rme = apriltag_cali_utils.RME_each_pic(intrinsic,dist,extrinsic_list,imgpoints_list_acc,objpoints_list_acc)
    print("after opt rme",rme)
    fs = cv2.FileStorage(os.path.join(root_dir,"intrinsic.yml"),cv2.FileStorage_WRITE)
    fs.write("intrinsic",intrinsic)
    fs.write("dist",dist)
    fs.write("rme",np.mean(rme))
    fs.release()



if __name__=="__main__":
    main()










