# -*- coding:utf-8 -*-
# @time: 
# @author:张新新
# @email: 1262981714@qq.com
import cv2
import os
from board.apriltagboard import AprilTagBoard
from calibration_utils.depth_utils import *
from calibration_utils.apriltag_cali_utils import apriltag_cali_utils
from PIL import Image
import transforms3d
from handineye import *
from method import *

def getImgList(root_dir):
    file_list = os.listdir(root_dir)
    rgb_list = []
    for file in file_list:
        if file.endswith(".png"):
            rgb_list.append(os.path.join(root_dir,file))
    return rgb_list

def get_robot_pose(file):
    temp = np.loadtxt(file)
    poseList = []
    for i in range(temp.shape[0]):
        r = transforms3d.quaternions.quat2mat(np.array([temp[i, 6], temp[i, 3], temp[i, 4], temp[i, 5]]))
        t = np.array([temp[i, :3]]).T
        H = np.append(np.append(r, t, 1), np.array([[0, 0, 0, 1]]), 0)
        poseList.append(H)
    return poseList


def main():

    board = AprilTagBoard("../config/apriltag.yml", "../config/tagId3.csv")
    root_dir = "F:/fbs_data_raw/603/intrinsic"
    img_list, depth_list = getImgList(root_dir)
    fs1 = cv2.FileStorage(os.path.join(root_dir,"intrinsic.yml"))
    intrinsic = fs1.getNode("intrinsic").mat()
    dist = fs1.getNode("dist").mat()
    fs1.release()
    if len(img_list) != len(depth_list):
        print("numer of img and depth not same")
        return 0
    objpoints_list = []
    imgpoints_list = []
    extrinsic_list = []
    tags_list = []
    for img_path in img_list:
        img = cv2.imread(img_path)
        tags = apriltag_cali_utils.detectTags(board, img, intrinsic, dist)
        objpoints, imgpoints = board.getObjImgPointList(tags)
        objpoints_list.append(objpoints)
        imgpoints_list.append(imgpoints)
    objpoints_list_acc = []
    imgpoints_list_acc = []
    depth_points_list = []
    for i in range(len(depth_list)):
        depth_img = Image.open(depth_list[i])
        imgpoints_acc, objpoints_acc, depth_points = get_imgpoint_depth(imgpoints_list[i],objpoints_list[i],depth_img)
        objpoints_list_acc.append(objpoints_acc)
        imgpoints_list_acc.append(imgpoints_acc)
        depth_points_list.append(depth_points)
    reject_id = []
    for i in range(len(imgpoints_list_acc)):

        succ,extrinsic = apriltag_cali_utils.extrisic_depth(objpoints_list_acc[i], imgpoints_list[i],
                                                            depth_points_list[i], intrinsic, dist)
        if not succ:
            reject_id.append(i)
            continue
        extrinsic_opt = apriltag_cali_utils.extrinsic_opt(intrinsic,dist,extrinsic,imgpoints_list_acc[i],objpoints_list_acc[i])
        extrinsic_list.append(extrinsic_opt)

    robot_pose_raw = get_robot_pose(root_dir + "/robot_pos.txt")
    robot_pose = []
    for i in range(len(robot_pose)):
        if i in reject_id:
            continue
        robot_pose.append(robot_pose_raw[i])

    while (True):
        A, B = motion.motion_axxb(robot_pose, extrinsic_list)
        Tsai_handeye = tsai.calibration(A, B)
        dual_handeye = dual.calibration(A, B)
        rx_handeye = rx.refine(dual_handeye, robot_pose, extrinsic_list, board.boardcorner)
        print("rx", rx_handeye)

        A, B = motion.motion_axyb(robot_pose, extrinsic_list)
        li_x, li_y = li.calibration(A, B)
        rz_x, rz_y = rz.refine(li_x, li_y, robot_pose, extrinsic_list, board.boardcorner)
        print("rz", rz_x)
        rz_error = rz.proj_error_each_point(rz_x, rz_y, robot_pose, extrinsic_list, board.boardcorner)
        x, y = np.where(rz_error.reshape([1, -1]) > 0.005)
        if y.shape[0] == 0:
            break
        x, y = np.where(rz_error.reshape([1, -1]) == np.max(rz_error))
        del robot_pose[y[0]]
        del extrinsic_list[y[0]]
        if len(robot_pose)<10:
            break







