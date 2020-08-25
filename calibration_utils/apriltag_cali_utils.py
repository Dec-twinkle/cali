# -*- coding:utf-8 -*-
# @time: 
# @author:张新新
# @email: 1262981714@qq.com
from calibration_utils.cali_utils import base_utils
import numpy as np
import cv2
import transforms3d
import pupil_apriltags as apriltag



class apriltag_cali_utils(base_utils):
    @staticmethod
    def detectTags(board, img, cameraMatrix=None, discoff=None, verbose=0):
        """
        检测img中的apriltag，返回一组tag,如果不输入cameraMatrix，tags中不含位姿信息
        :param board: apiriltag.board 包含board的一些参数
        :param img: 需要检测的图片路径
        :param cameraMatrix:相机内参
        :return: tags 检测到的tags
        """
        # img = cv2.imread(img)
        if discoff is not None:
            img = cv2.undistort(img, cameraMatrix, discoff)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)
        at_detector = apriltag.Detector(families=board.april_family)  # for windows
        if cameraMatrix is None:
            tags = at_detector.detect(gray)
            if verbose == 1:
                img = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
                img = apriltag_cali_utils.drawTagAxis(img, tags)
                cv2.namedWindow("apriltag", cv2.WINDOW_NORMAL)
                cv2.imshow("apriltag", img)
                cv2.waitKey(0)
        else:
            if ~(discoff is None):
                gray = cv2.undistort(gray, cameraMatrix, discoff)
            camera_param = [cameraMatrix[0, 0], cameraMatrix[1, 1], cameraMatrix[0, 2], cameraMatrix[1, 2]]
            tags = at_detector.detect(gray, True, camera_param, board.tag_size)
            if verbose == 1:
                img = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
                img = apriltag_cali_utils.drawTagAxis(img, tags, cameraMatrix)
                cv2.namedWindow("apriltag", cv2.WINDOW_NORMAL)
                cv2.imshow("apriltag", cv2.resize(img,(512,512)))
                cv2.waitKey(0)
        # for tag in tags:
        #     print(tag.tag_id)
        return tags

    @staticmethod
    def drawTagAxis(img, tags, cameraMatrix=None, length=0.015, line_width=1):
        """
        在图像上画出每个tag的坐标轴，蓝色表示x轴，绿色表示y轴，红色表示z轴
        :param img: 图片
        :param tags:
        :param cameraMatrix: 相机内参
        :param length: 长度，指实际长度
        :return: img：图片
        """
        point_x = np.array([[length, 0, 0, 1]]).T
        point_y = np.array([[0, length, 0, 1]]).T
        point_z = np.array([[0, 0, length, 1]]).T
        if cameraMatrix is None:
            for tag in tags:
                img = cv2.circle(img, (int(tag.corners[0, 0]), int(tag.corners[0, 1])), 5, (255, 0, 0), thickness=3)
                img = cv2.circle(img, (int(tag.corners[1, 0]), int(tag.corners[1, 1])), 5, (0, 255, 0), thickness=3)
                img = cv2.circle(img, (int(tag.corners[2, 0]), int(tag.corners[2, 1])), 5, (0, 0, 255), thickness=3)
            return img
        cameraMatrix = np.append(cameraMatrix, np.zeros([3, 1]), 1)
        for tag in tags:
            R = tag.pose_R
            T = tag.pose_t
            H = np.append(np.append(R, T, 1), np.array([[0, 0, 0, 1]]), 0)
            pro_x = np.dot(cameraMatrix, np.dot(H, point_x))
            pro_x = pro_x / pro_x[2, 0]
            pro_y = np.dot(cameraMatrix, np.dot(H, point_y))
            pro_y = pro_y / pro_y[2, 0]
            pro_z = np.dot(cameraMatrix, np.dot(H, point_z))
            pro_z = pro_z / pro_z[2, 0]

            cv2.putText(img, str(tag.tag_id), (int(tag.center[0]), int(tag.center[1])), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 2)
            img = cv2.line(img, (int(tag.center[0]), int(tag.center[1])), (int(pro_x[0, 0]), int(pro_x[1, 0])),
                           (255, 0, 0), thickness=line_width)
            img = cv2.line(img, (int(tag.center[0]), int(tag.center[1])), (int(pro_y[0, 0]), int(pro_y[1, 0])),
                           (0, 255, 0), thickness=line_width)
            img = cv2.line(img, (int(tag.center[0]), int(tag.center[1])), (int(pro_z[0, 0]), int(pro_z[1, 0])),
                           (0, 0, 255), thickness=line_width)
            # img = cv2.circle(img,(int(tag.corners[0,0]),int(tag.corners[0,1])),1,(255,0,0),thickness=2)
            # img = cv2.circle(img,(int(tag.corners[1,0]),int(tag.corners[1,1])),1,(0,255,0),thickness=2)
            # img = cv2.circle(img,(int(tag.corners[2,0]),int(tag.corners[2,1])),1,(0,0,255),thickness=2)

        return img
    @staticmethod
    def extrinsic_tags(tags, board):
        """
        得到相机的姿态,主要是将每个tag中估计相机姿态使用4分位法进行筛选
        :param tags: 检测图片的tags
        :param board: apriltag的规格参数
        :param cameraMatrix: 相机内参
        :return: 4*4 旋转矩阵 表示相机的姿态
        """
        q = np.array([])
        t = np.array([])
        n = len(tags)
        for tag in tags:
            q = np.append(q, transforms3d.quaternions.mat2quat(tag.pose_R))
            H = np.append(np.append(tag.pose_R, tag.pose_t, 1), np.array([[0, 0, 0, 1]]), 0)
            x, y = np.where(board.tag_id_order == tag.tag_id)
            board_center = board.boardcenter[x[0] * board.marker_X + y[0], :]
            point = np.array([[-board_center[0], -board_center[1], 0, 1]]).T
            proj = np.dot(H, point)
            orgin = proj / proj[3, 0]
            t = np.append(t, orgin[:3, 0])
        q = np.reshape(q, [-1, 4])
        t = np.reshape(t, [-1, 3])

        # 使用四分位法去除异常值
        if n > 4:
            q1 = q[:, 0]
            q2 = q[:, 1]
            q3 = q[:, 2]
            q4 = q[:, 3]
            Q11 = np.percentile(q1, 25)
            Q31 = np.percentile(q1, 75)
            Q12 = np.percentile(q2, 25)
            Q32 = np.percentile(q2, 75)
            Q13 = np.percentile(q3, 25)
            Q33 = np.percentile(q3, 75)
            Q14 = np.percentile(q4, 25)
            Q34 = np.percentile(q4, 75)
            IQR1 = 1.5 * (Q31 - Q11)
            IQR2 = 1.5 * (Q32 - Q12)
            IQR3 = 1.5 * (Q33 - Q13)
            IQR4 = 1.5 * (Q34 - Q14)
            for i in range(q.shape[0] - 1, -1, -1):
                flag1 = (q[i, 0] < Q11 - IQR1) | (q[i, 0] > Q31 + IQR1)
                flag2 = (q[i, 1] < Q12 - IQR2) | (q[i, 1] > Q32 + IQR2)
                flag3 = (q[i, 2] < Q13 - IQR3) | (q[i, 2] > Q33 + IQR3)
                flag4 = (q[i, 3] < Q14 - IQR4) | (q[i, 3] > Q34 + IQR4)
                if flag1 | flag2 | flag3 | flag4:
                    q = np.delete(q, i, axis=0)
        mean_t = np.array([np.mean(t, axis=0)])
        std_t = np.array([np.std(t, axis=0)])
        error_t = np.empty([t.shape[0], 3], dtype=bool)
        error_t[:, :] = np.abs(t[:, :] - mean_t[0, :]) > 3 * std_t[0, :]
        index, _ = np.where(error_t)
        if np.size(index)>0:
            index_t = np.array(list(set(list(index))))
            t = np.delete(t, index_t, axis=0)
        mean_q = np.mean(q, axis=0)
        mean_t = np.mean(t, axis=0)
        pose_R = transforms3d.quaternions.quat2mat(mean_q)
        pose = np.append(np.append(pose_R, np.array([mean_t]).T, 1), np.array([[0, 0, 0, 1]]), 0)
        return pose



