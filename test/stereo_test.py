# -*- coding:utf-8 -*-
# @time: 
# @author:张新新
# @email: 1262981714@qq.com
import os
import cv2
from board.apriltagboard import AprilTagBoard
from calibration_utils.apriltag_cali_utils import apriltag_cali_utils
import numpy as np

def getImgList(root_dir):
    file_list = os.listdir(root_dir)
    rgb_list = []
    for file in file_list:
        if file.endswith(".jpg"):
            rgb_list.append(os.path.join(root_dir,file))
    return rgb_list

def main():
    root_dir1 = "D:\\minshi\\0822\\right"
    root_dir2 = "D:\\minshi\\0822\\left"

    imglist1 = getImgList(root_dir1)
    imglist2 = getImgList(root_dir2)

    fs1 = cv2.FileStorage(os.path.join(root_dir1,"intrinsic.yml"), cv2.FileStorage_READ)

    fs2 = cv2.FileStorage(os.path.join(root_dir2,"intrinsic.yml"), cv2.FileStorage_READ)
    intrinsic1 = fs1.getNode("intrinsic").mat()
    dist1 = fs1.getNode("dist").mat()
    intrinsic2 = fs2.getNode("intrinsic").mat()
    dist2 = fs2.getNode("dist").mat()
    fs1.release()
    fs2.release()
    board = AprilTagBoard("../config/apriltag2.yml","../config/tagId4.csv")
    objpoints1_list = []
    imgpoints1_list = []
    objpoints2_list = []
    imgpoints2_list = []
    extrinsic1_list = []
    extrinsic2_list = []
    for imgPath in imglist1:
        print(imgPath, " is detecting!")
        img = cv2.imread(imgPath)
        tags = apriltag_cali_utils.detectTags(board,img,intrinsic1,dist1)
        if len(tags)==0:
            objpoints1_list.append(None)
            imgpoints1_list.append(None)
            extrinsic1_list.append(None)
        else:
            objpoints,imgpoints = board.getObjImgPointList(tags)
            objpoints1_list.append(objpoints)
            imgpoints1_list.append(imgpoints)
            extrinsic = apriltag_cali_utils.extrinsic(tags,board)
            extrinsic_opt = apriltag_cali_utils.extrinsic_opt(intrinsic1,dist1,extrinsic,imgpoints,objpoints)
            extrinsic1_list.append(extrinsic_opt)
    for imgPath in imglist2:
        print(imgPath, " is detecting!")
        img = cv2.imread(imgPath)
        tags = apriltag_cali_utils.detectTags(board,img,intrinsic2,dist2)
        if len(tags)==0:
            objpoints2_list.append(None)
            imgpoints2_list.append(None)
            extrinsic2_list.append(None)
        else:
            objpoints, imgpoints = board.getObjImgPointList(tags)
            objpoints2_list.append(objpoints)
            imgpoints2_list.append(imgpoints)
            extrinsic = extrinsic = apriltag_cali_utils.extrinsic(tags,board)
            extrinsic_opt = apriltag_cali_utils.extrinsic_opt(intrinsic2, dist2, extrinsic, imgpoints, objpoints)
            extrinsic2_list.append(extrinsic_opt)
    rme, H = apriltag_cali_utils.stereo_calibration(imgpoints1_list,objpoints1_list,imgpoints2_list,objpoints2_list,
        intrinsic1,dist1,intrinsic2,dist2,extrinsic1_list.copy(),extrinsic2_list.copy(),board.GetBoardAllPoints())
    print("rme: ",rme)
    print("transform matrix", H)

    save_dir = os.path.join(root_dir1,os.path.pardir)
    fs = cv2.FileStorage(os.path.join(save_dir,"stereo.yml"),cv2.FileStorage_WRITE)
    fs.write("stereo", H)
    fs.write("rme", rme)
    fs.release()
    realcoor = board.GetBoardAllPoints().T
    realcoor = np.append(realcoor, np.zeros([1, realcoor.shape[1]]), 0)
    realcoor = np.append(realcoor, np.ones([1, realcoor.shape[1]]), 0)
    for i in range(len(imglist1)):
        imgpoints2 = imgpoints2_list[i]
        proj = np.dot(np.linalg.inv(extrinsic2_list[i]),np.dot(H,np.dot(extrinsic1_list[i],realcoor)))
        # proj = cv2.projectPoints(proj,extrinsic2_list[i][:3,:3],extrinsic2_list[i][:3,3],intrinsic2,dist2)
        rvec = extrinsic2_list[i][:3,:3]
        tvec = extrinsic2_list[i][:3,3]
        imagePoints, jacobian = cv2.projectPoints(np.transpose(proj[:3,:]).reshape([-1,1,3]), rvec, tvec, intrinsic2, dist2)
        imagePoints = imagePoints.reshape([-1, 2])
        pic = cv2.imread(imglist2[i])
        for i in range(imgpoints2.shape[0]):
            cv2.circle(pic,(int(imgpoints2[i,0]),int(imgpoints2[i,1])),4,(255,0,0),4)
            cv2.circle(pic, (int(imagePoints[i, 0]), int(imagePoints[i, 1])), 4, (0, 255, 0), 4)
        cv2.imshow("reproject",cv2.resize(pic,(1024,1024)))
        cv2.waitKey(0)


if __name__ == '__main__':
    main()




