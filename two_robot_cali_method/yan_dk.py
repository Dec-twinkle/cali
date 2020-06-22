# -*- coding:utf-8 -*-
# @time: 
# @author:张新新
# @email: 1262981714@qq.com
import numpy as np
from method import li

def calibration(A1, B1, C1, A2, B2, C2):
    """
    使用d-k方法进行双机器臂标定
    A1和C2 fixed
    :param A1: robot1 pose
    :param B1: camera pose
    :param C1: robot2 pose
    :param A2:
    :param B2:
    :param C2:
    :return:
    """
    A1 = A1[0]
    C2 = C2[0]
    Z,Xt = li.calibration(C1,B1)
    B_inv = []
    for j in range(len(B2)):
        B_inv.append(np.linalg.inv(B2[j]))
    X,Zt = li.calibration(A2,B_inv)

    U,_,Vt = np.linalg.svd(Xt[:3,:3])
    Xt[:3,:3] = np.dot(U,Vt)
    U,_,Vt = np.linalg.svd(X[:3,:3])
    X[:3,:3] = np.dot(U,Vt)
    U, _, Vt = np.linalg.svd(Zt[:3, :3])
    Zt[:3, :3] = np.dot(U, Vt)
    U, _, Vt = np.linalg.svd(Z[:3, :3])
    Z[:3, :3] = np.dot(U, Vt)

    Y1 = np.dot(np.dot(A1, X), np.linalg.inv(Xt))
    Y2 = np.dot(np.dot(Zt, np.linalg.inv(Z)),np.linalg.inv(C2))

    Err1 = np.linalg.norm(np.dot(np.dot(A1,X),B1[0])- np.dot(np.dot(Y1,C1[0]),Z))
    Err2 = np.linalg.norm(np.dot(np.dot(A2[0],X),B2[0])- np.dot(np.dot(Y2,C2),Z))
    if Err1<Err2:
        Y = Y1
    else:
        Y = Y2
    return X,Y,Z




