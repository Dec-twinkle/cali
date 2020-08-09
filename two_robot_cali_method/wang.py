# -*- coding:utf-8 -*-
# @time: 
# @author:张新新
# @email: 1262981714@qq.com\
import numpy as np
import math
from scipy.linalg import expm
from scipy.linalg import logm
def calibration(A,B,C, Xact,Yact, Zact):
    n = len(A)
    Ra = []
    Rb = []
    Rc = []
    Ta = []
    Tb = []
    Tc = []
    for i in range(n):
        Ra.append(A[i][:3, :3])
        Rb.append(B[i][:3, :3])
        Rc.append(C[i][:3, :3])
        Ta.append(A[i][:3, 3].reshape([-1,1]))
        Tb.append(B[i][:3, 3].reshape([-1,1]))
        Tc.append(C[i][:3, 3].reshape([-1,1]))
    e = math.pi/5
    Rx_init = np.dot(expm(so3_vec(e * np.ones([3,1]))), Xact[:3,:3])
    Rz_init = np.dot(expm(so3_vec(e * np.ones([3, 1]))), Zact[:3, :3])
    Ry_init = np.dot(np.dot(np.dot(np.dot(Ra[0],Rx_init),Rb[0]),np.linalg.inv(Rz_init)),np.linalg.inv(Rc[0]))

    delR = 10000 * np.ones([9,1])
    n_step = 0
    while(np.linalg.norm(delR)>0.01 and n_step<500):
        q = np.empty([n*9,1])
        F = np.empty([n*9,9])
        for i in range(n):
            tmp1 = np.dot(Rx_init, Rb[i])
            tmp2 = np.dot(np.dot(Ry_init,Rc[i]),Rz_init)
            qq = - np.dot(Ra[i],tmp1) +tmp2
            q[i*9:(i+1)*9,:] = qq.T.reshape([-1,1])


            F11 = - np.dot(Ra[i], so3_vec(tmp1[:,0]))
            F21 = - np.dot(Ra[i], so3_vec(tmp1[:,1]))
            F31 = - np.dot(Ra[i], so3_vec(tmp1[:,2]))
            F12 = so3_vec(tmp2[:,0])
            F22 = so3_vec(tmp2[:,1])
            F32 = so3_vec(tmp2[:,2])
            F13 = np.dot(np.dot(Ry_init,Rc[i]),so3_vec(Rz_init[:,0]))
            F23 = np.dot(np.dot(Ry_init,Rc[i]),so3_vec(Rz_init[:,1]))
            F33 = np.dot(np.dot(Ry_init,Rc[i]),so3_vec(Rz_init[:,2]))
            F1 = np.vstack((np.vstack((F11,F21)),F31))
            F2 = np.vstack((np.vstack((F12,F22)),F32))
            F3 = np.vstack((np.vstack((F13,F23)),F33))
            FF = np.hstack((F1,np.hstack((F2,F3))))
            F[i*9:(i+1)*9,:] = FF[:,:]
        delR = np.dot(np.dot(np.linalg.inv(np.dot(F.T,F)),F.T),q).flatten()
        print("cost is",np.linalg.norm(delR))
        thetaX = np.linalg.norm(delR[0:3])
        Rx_init = np.dot(skewexp(delR[0:3] / thetaX, thetaX), Rx_init)
        thetaY = np.linalg.norm(delR[3:6])
        Ry_init = np.dot(skewexp(delR[3:6] / thetaY, thetaY), Ry_init)
        thetaZ = np.linalg.norm(delR[6:9])
        Rz_init = np.dot(skewexp(delR[6:9] / thetaZ, thetaZ), Rz_init)
        n_step = n_step+1
    J = np.zeros([3*n, 9])
    p = np.zeros([3*n, 1])
    for i in range(n):
        J[3*i:3*(i+1),:3] = Ra[i]
        J[3*i:3*(i+1),3:6] = - np.identity(3)
        J[3*i:3*(i+1),6:9] = -np.dot(Ry_init,Rc[i])
        p[3*i:3*(i+1),:] = -Ta[i]-np.dot(np.dot(Ra[i],Rx_init),Tb[i])+np.dot(Ry_init,Tc[i])
    tranform = np.dot(np.linalg.inv(np.dot(J.T,J)),np.dot(J.T,p))
    tX = tranform[:3]
    tY = tranform[3:6]
    tZ = tranform[6:9]
    X = np.zeros([4,4])
    Y = np.zeros([4,4])
    Z = np.zeros([4,4])
    X[3,3] = 1
    Y[3,3] = 1
    Z[3,3] = 1

    X[:3,:3] = Rx_init
    Y[:3,:3] = Ry_init
    Z[:3,:3] = Rz_init
    X[:3, 3] = tX[:,0]
    Y[:3, 3] = tY[:,0]
    Z[:3, 3] = tZ[:,0]

    return X,Y,Z



def so3_vec(X):
    X = np.reshape(X,[-1,3])
    if X.shape[0]==3:
        g = np.array([-X[1,2],X[0,2],-X[0,1]])
    else:
        g = np.array([[0,-X[0,2],X[0,1]],
                      [X[0,2],0,-X[0,0]],
                      [-X[0,1],X[0,0],0]
                       ])
    return g

def skewexp(s, theta):
    s = s.reshape(-1,3)
    if s.shape[0]==1:
        s = skew(s)
    g = np.identity(3) + s * math.sin(theta) + np.dot(s,s) * (1 - math.cos(theta))
    return g

def skew(s):
    s = s.reshape([-1,3])
    return np.array([[0,-s[0,2],s[0,1]],
                     [s[0][2],0,-s[0,0]],
                     [-s[0,1],s[0,0],0]])
