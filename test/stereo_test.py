# -*- coding:utf-8 -*-
# @time: 
# @author:张新新
# @email: 1262981714@qq.com
import os
import cv2
from board.chessboard import ChessBoard
from calibration_utils.chessboard_cali_utils import chessboard_cali_utils


def getImgList(root_dir):
    file_list = os.listdir(root_dir)
    rgb_list = []
    for file in file_list:
        if file.endswith(".png"):
            rgb_list.append(os.path.join(root_dir,file))
    return rgb_list

def main():
    root_dir1 = ""
    root_dir2 = ""

    imglist1 = getImgList(root_dir1)
    imglist2 = getImgList(root_dir2)

    fs1 = cv2.FileStorage(os.path.join(root_dir1,"intrinsic.yml"))
    fs2 = cv2.FileStorage(os.path.join(root_dir2,"intrinsic.yml"))
    intrinsic1 = fs1.getNode("intrinsic").mat()
    dist1 = fs1.getNode("dist").mat()
    intrinsic2 = fs2.getNode("intrinsic").mat()
    dist2 = fs2.getNode("dist").mat()
    fs1.release()
    fs2.release()
    board = ChessBoard("")
    objpoints1_list = []
    imgpoints1_list = []
    objpoints2_list = []
    imgpoints2_list = []
    extrinsic1_list = []
    extrinsic2_list = []
    for img in imglist1:
        print(img, " is detecting!")
        succ,objpoints,imgpoints = board.GetImageAndObjPoint(img)
        if not succ:
            objpoints1_list.append(None)
            imgpoints1_list.append(None)
            extrinsic1_list.append(None)
        else:
            objpoints1_list.append(objpoints)
            imgpoints1_list.append(imgpoints)
            extrinsic = chessboard_cali_utils.extrinsic(imgpoints,objpoints,intrinsic1,dist1)
            extrinsic_opt = chessboard_cali_utils.extrinsic_opt(intrinsic1,dist1,extrinsic,imgpoints,objpoints)
            extrinsic1_list.append(extrinsic_opt)
    for img in imglist2:
        print(img, " is detecting!")
        succ,objpoints,imgpoints = board.GetImageAndObjPoint(img)
        if not succ:
            objpoints2_list.append(None)
            imgpoints2_list.append(None)
            extrinsic2_list.append(None)
        else:
            objpoints2_list.append(objpoints)
            imgpoints2_list.append(imgpoints)
            extrinsic = chessboard_cali_utils.extrinsic(imgpoints, objpoints, intrinsic2, dist2)
            extrinsic_opt = chessboard_cali_utils.extrinsic_opt(intrinsic1, dist1, extrinsic, imgpoints, objpoints)
            extrinsic1_list.append(extrinsic_opt)
    rme, H = chessboard_cali_utils.stereo_calibration(imgpoints1_list,objpoints1_list,imgpoints2_list,objpoints2_list,
        intrinsic1,dist1,intrinsic2,dist2,extrinsic1_list,extrinsic2_list,board.GetBoardAllPoints())

    print("rme: ",rme)
    print("transform matrix", H)

    save_dir = os.path.join(root_dir1,os.path.pardir)
    fs = cv2.FileStorage(os.path.join(save_dir,"stereo.yml"),cv2.FileStorage_WRITE)
    fs.write("stereo", H)
    fs.write("rme", rme)
    fs.release()








