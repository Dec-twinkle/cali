# -*- coding:utf-8 -*-
# @time: 
# @author:张新新
# @email: 1262981714@qq.com
import numpy as np
from scipy import optimize as op
import transforms3d
def reproject_error(A,B,C,X,Y,Z,realcoor):
    if realcoor.shape[1]==2:
        realcoor = np.append(realcoor,np.zeros([realcoor.shape[0],1]),1)
    if realcoor.shape[1]==3:
        realcoor = np.append(realcoor,np.ones([realcoor.shape[0],1]),1)
    errors = np.array([])
    for i in range(len(A)):
        proj_tran = np.dot(np.dot(np.dot(A[i],X),B[i]),np.linalg.inv(np.dot(np.dot(Y,C[i]),Z)))
        # print(i,proj_tran)
        proj = np.dot(proj_tran,realcoor.T)
        error = proj[:3,:]-realcoor.T[:3,:]
        errors = np.append(errors,error)
    return errors.flatten()

def loss_function(X,A,B,C,realcoor):
    Rx = transforms3d.quaternions.quat2mat(X[:4])
    Tx = X[4:7]
    x = np.append(np.append(Rx,np.transpose([Tx]),1),np.array([[0,0,0,1]]),0)
    Ry = transforms3d.quaternions.quat2mat(X[7:11])
    Ty = X[11:14]
    y = np.append(np.append(Ry,np.transpose([Ty]), 1), np.array([[0, 0, 0, 1]]), 0)
    Rz = transforms3d.quaternions.quat2mat(X[14:18])
    Tz = X[18:21]
    z = np.append(np.append(Rz,np.transpose([Tz]), 1), np.array([[0, 0, 0, 1]]), 0)
    return reproject_error(A,B,C,x,y,z,realcoor)

def opt(A,B,C,X,Y,Z,real_coor):
    init = np.array([])
    init = np.append(init,transforms3d.quaternions.mat2quat(X[:3,:3]))
    init = np.append(init,X[:3,3])
    init = np.append(init, transforms3d.quaternions.mat2quat(Y[:3,: 3]))
    init = np.append(init, Y[:3, 3])
    init = np.append(init, transforms3d.quaternions.mat2quat(Z[:3,: 3]))
    init = np.append(init, Z[:3, 3])
    solve = op.root(loss_function,init,args=(A,B,C,real_coor),method="lm")
    X = solve.x
    Rx = transforms3d.quaternions.quat2mat(X[:4])
    Tx = X[4:7]
    x = np.append(np.append(Rx, np.transpose([Tx]), 1), np.array([[0, 0, 0, 1]]), 0)
    Ry = transforms3d.quaternions.quat2mat(X[7:11])
    Ty = X[11:14]
    y = np.append(np.append(Ry, np.transpose([Ty]), 1), np.array([[0, 0, 0, 1]]), 0)
    Rz = transforms3d.quaternions.quat2mat(X[14:18])
    Tz = X[18:21]
    z = np.append(np.append(Rz, np.transpose([Tz]), 1), np.array([[0, 0, 0, 1]]), 0)
    return x,y,z
