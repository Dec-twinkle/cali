from abc import ABCMeta,abstractmethod

class board(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def getParameter(self,configfile):
        pass


    @abstractmethod
    def GetBoardAllPoints(self):
        """
        获取标定板上所有可计算的角点
        :return: objpoints: 所有角点
        """
        pass

    @abstractmethod
    def intrinsic(self,imgpoints_list, objpoints_list):
        """
        相机内参标定
        :param imgpoints_list: 图片中的照片检测的角点
        :param objpoints_list: 图片角点对应的标定板上的点
        :return: r:重投影误差
                 mtx:相机内参矩阵
                 dist:相机畸变参数
        """
        pass

    @abstractmethod
    def extrinsic(self,imgpoints, objpoints, intrinsic, dist):
        '''

        :param imgpoints:
        :param objpoints:
        :param intrinsic:
        :param dist:
        :return:
        '''
        pass
