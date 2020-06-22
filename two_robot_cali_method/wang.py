#-*- coding:utf-8 -*-
# @time: 
# @author:张新新
# @email: 1262981714@qq.com\
import numpy as np
import math
from scipy.linalg import expm
from scipy.linalg import logm
def calibration(A,B,C, Xact,Yact, Zact):
    n = len(A)
    Ra = A[:][:3,:3]
    Rb = B[:][:3.:3]
    Rc = C[:][:3.:3]
    Ta = A[:][:3, 3]
    Tb = B[:][:3, 3]
    Tc = C[:][:3, 3]

    e = math.pi/5
    Rx_init = np.dot(expm(so3_vec(e * np.ones([3,1]))), Xact[:3,:3])
    Rz_init = np.dot(expm(so3_vec(e * np.ones([3, 1]))), Zact[:3, :3])
    Ry_init = np.dot(np.dot(np.dot(np.dot(Ra[0],Rx_init),Rb[0]),np.linalg.inv(Rz_init)),Rc[0])

    delR = 1000 * np.ones([9,1])
    n_step = 0
    while(np.linalg.norm(delR)>0.01 and n_step<500):
        q = np.array([n*9,1])
        F = np.array([n*9,9])
        for i in range(n):
            tmp1 = np.dot(Rx_init, Rb[i])
            tmp2 = np.dot(np.dot(Ry_init,Rc[i]),Rz_init)
            qq = - np.dot(Ra[i])*tmp1 +tmp2
            q[i*9:(i+1)*9,0] = qq.reshape([-1,9])[:]


            F11 = -Ra[i] * so3_vec(tmp1[:,0])
            F21 = -Ra[i] * so3_vec(tmp1[:,1])
            F31 = -Ra[i] * so3_vec(tmp1[:,2])
            F12 = so3_vec(tmp2[:,0])
            F22 = so3_vec(tmp2[:,1])
            F32 = so3_vec(tmp2[:,2])
            F13 = np.dot(np.dot(Ry_init,Rc[i]),so3_vec(Rz_init[:,1]))
            F23 = np.dot(np.dot(Ry_init,Rc[i]),so3_vec(Rz_init[:,2]))
            F33 = np.dot(np.dot(Ry_init,Rc[i]),so3_vec(Rz_init[:,3]))
            F[i*9:(i+1)*9,:] = np.array([[F11,F12,F13],
                                         [F21,F22,F23],
                                         [F31,F32,F33]])
        delR = np.dot(np.dot(np.linalg.inv(np.dot(F.T,F)),F.T),q)
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
        p[3*i:3*(i+1),:] = -Ta[i]-Ra[i]*Rx_init*Tb[i]+Ry_init*Tc[i]
    tranform = np.dot(np.linalg.inv(np.dot(J.T,J)),np.dot(J.T,p))
    tX = tranform[:3]
    tY = tranform[3:6]
    tZ = tranform[6:9]
    X = np.zeros([4,4])
    Y = np.zeros([4,4])
    Z = np.zeros([4,4])
    X[4,4] = 1
    Y[4,4] = 1
    Z[4,4] = 1

    X[:3,:3] = Rx_init
    Y[:3,:3] = Ry_init
    Z[:3,:3] = Rz_init
    X[:3, 3] = tX
    Y[:3, 3] = tY
    Z[:3, 3] = tZ

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
    if s.shape == tuple(3, 1):
        s = skew(s)
    n = theta.shape[1]
    g = np.zeros([3, 3, n])
    for i in range(n):
        g[:,:,i] = np.identity(3) + s * math.sin(theta) + s**2 * (1 - math.cos(theta))
    return g

def skew(s):
    s = s.reshape([-1,3])
    return np.array([[0,-s[0,2],s[0,1]],
                     [s[0][2]],0,-s[0,0],
                     [-s[0,1],s[0,0],0]])
