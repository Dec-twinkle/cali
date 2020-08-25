#-*- coding:utf-8 -*-
# @time: 
# @author:张新新
# @email: 1262981714@qq.com
import cv2
import numpy as np
from board import board as board
import yaml

class AprilTagBoard(board.board):
    marker_X = 7
    marker_Y = 5
    markerSeparation = 0.007776
    tag_size = 0.030385
    april_family = "tag36h11"
    tag_id_order = np.array([])
    boardcenter = np.array([])
    boardcorner = np.array([])
    conners_order = np.array([[-1, 1], [1, 1], [1, -1], [-1, -1]])

    def __init__(self,configFile,tagOrderFile):
        self.getParameter(configFile)
        self.tag_id_order = np.loadtxt(tagOrderFile, delimiter=",")
        self.get_board_points()

    def get_board_points(self):
        self.boardcenter = np.empty([self.marker_X * self.marker_Y,2])
        self.boardcorner = np.empty([4 * self.marker_X * self.marker_Y,2])
        m,n = self.marker_X,self.marker_Y
        l = self.tag_size
        seq = self.markerSeparation
        for i in range(n):
            for j in range(m):
                center_x = j*(l+seq)
                center_y = i*(l+seq)
                self.boardcenter[i * m + j, 0] = center_x
                self.boardcenter[i * m + j, 1] = center_y
                for k in range(4):
                    self.boardcorner[4 * (i * m + j) + k, 0] = center_x + l / 2.0 * self.conners_order[k,0]
                    self.boardcorner[4 * (i * m + j) + k, 1] = center_y + l / 2.0 * self.conners_order[k,1]

    def getParameter(self, configfile):
        f = open(configfile, 'r', encoding='utf-8')
        cont = f.read()
        x = yaml.load(cont)
        self.marker_X = x["marker_X"]
        self.marker_Y = x["marker_Y"]
        self.markerSeparation = x["markerSeparation"]
        self.tag_size = x["tag_size"]
        self.april_family = x["april_family"]
        f.close()

    def GetBoardAllPoints(self):
        return self.boardcorner

    def getPointsbyTagId(self,tagId):
        x,y = np.where(self.tag_id_order==tagId)
        center = self.boardcenter[x[0]*self.marker_X+y[0],:]
        corner = self.boardcorner[4*(x[0]*self.marker_X+y[0]):4*(x[0]*self.marker_X+y[0])+4,:]
        return center,corner

    def getObjImgPointList(self,tags):
        objpoint = np.array([])
        imgpoint = np.array([])
        for tag in tags:
            center, conners = self.getPointsbyTagId(tag.tag_id)
            objpoint = np.append(objpoint, conners)
            imgpoint = np.append(imgpoint, tag.corners)
        objpoint = np.reshape(objpoint, [-1, 2])
        imgpoint = np.reshape(imgpoint, [-1, 2])
        return objpoint, imgpoint







