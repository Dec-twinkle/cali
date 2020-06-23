# -*- coding:utf-8 -*-
# @time: 
# @author:张新新
# @email: 1262981714@qq.com
import numpy as np
from two_robot_cali_method import wang
from two_robot_cali_method import yan_dk
from two_robot_cali_method import rme_opt
from board.chessboard import ChessBoard

def load_data(file):
    data = np.loadtxt(file)
    pose_list = []
    for i in range(int(data.shape[0]/4)):
        pose_list.append(data[i*4:4*(i+1), :])
    return pose_list

def main():
    x_init = np.identity(4)
    y_init = np.identity(4)
    z_init = np.identity(4)
    board = ChessBoard("../config/chessboard.yml")
    A1 = load_data("../data/two_cali_data/A1")
    A2 = load_data("../data/two_cali_data/A2")
    B1 = load_data("../data/two_cali_data/B1")
    B2 = load_data("../data/two_cali_data/B2")
    C1 = load_data("../data/two_cali_data/C1")
    C2 = load_data("../data/two_cali_data/C2")
    A = A1.copy()
    A.extend(A2)
    B = B1.copy()
    B.extend(B2)
    C = C1.copy()
    C.extend(C2)

    print("start to estimate using Wang method")
    X,Y,Z = wang.calibration(A,B,C,x_init,y_init,z_init)
    rme(A,B,C,X,Y,Z,board.GetBoardAllPoints())
    # X1,Y1,Z1 = yan_dk.calibration(A1, B1, C1, A2, B2, C2)
    # rme(A, B, C, X1, Y1, Z1, board.GetBoardAllPoints())
    X2,Y2,Z2  = rme_opt.opt(A,B,C,X,Y,Z,board.GetBoardAllPoints())
    rme(A, B, C, X2, Y2, Z2, board.GetBoardAllPoints())
    print("wang result",X,Y,Z)

def rme(A,B,C,X,Y,Z,realcoor):
    if realcoor.shape[1]==2:
        realcoor = np.append(realcoor,np.zeros([realcoor.shape[0],1]),1)
    if realcoor.shape[1]==3:
        realcoor = np.append(realcoor,np.ones([realcoor.shape[0],1]),1)
    for i in range(len(A)):
        proj_tran = np.dot(np.dot(np.dot(A[i],X),B[i]),np.linalg.inv(np.dot(np.dot(Y,C[i]),Z)))
        # print(i,proj_tran)
        proj = np.dot(proj_tran,realcoor.T)
        error = proj[:3,:]-realcoor.T[:3,:]
        print(i,np.mean(np.abs(error)))



if __name__ == '__main__':
    main()

