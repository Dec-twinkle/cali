# Computer Vision Calibration tool

Computer vision calibration is an important foundation for 3D vision, and the accuracy of camera calibration
affects the subsequent process. As the basis of 3D vision, camera calibration is helpful for beginners to understand 3D vision.

This repository contains:
1. camera intrinsic and extrinsic parameters calibration.
2. hand-in-eye and hand-on-eye robot calibration.
3. two robot relative pose calibration.

## Table of Contents
- [Dependencies](#Dependencies) 
- [Calibration Board](#Calibration Board)
- [Structure](#Structure)
- [Calibration type](#Calibration type)

## Dependencies
```
python 3.6
pupil-apriltags 2.0
scipy 1.5.0
transforms3d 0.3.1
numpy 1.19.0
Pillow 7.1.2
matplotlib 3.2.2
opencv-python 3.4.6.27
```




## Calibration Board
Checkerboard calibration board is the most commonly used and most basic calibration board. 
The general vision system can easily achieve the ideal calibration effect using the checkerboard calibration board.

![image](https://github.com/javapoor/cali/blob/master/image_folder/chessboard.jpg)

Apriltagtags is a common calibration board in the field of robots. Compared with chess board, 
its biggest advantage is that it does not require the calibration board to be fully displayed
 in the camera field of view.
![image](https://github.com/javapoor/cali/blob/master/image_folder/apriltag.png)

## Structure

```
├── readme.md                   // help
├── board                      // apriltag and chess board class
├── config                      // 
│   ├── default.json
│   ├── dev.json                // 开发环境
│   ├── experiment.json         // 实验
│   ├── index.js                // 配置控制
│   ├── local.json              // 本地
│   ├── production.json         // 生产环境
│   └── test.json               // 测试环境
├── data
├── doc                         // 文档
├── environment
├── gulpfile.js
├── locales
├── logger-service.js           // 启动日志配置
├── node_modules
├── package.json
├── app-service.js              // 启动应用配置
├── static                      // web静态资源加载
│   └── initjson
│       └── config.js         // 提供给前端的配置
├── test
├── test-service.js
└── tools
```
