# Computer Vision Calibration tool

Computer vision calibration is an important foundation for 3D vision, and the accuracy of camera calibration
affects the subsequent process. As the basis of 3D vision, camera calibration is helpful for beginners to understand 3D vision.

This repository contains:
1. camera intrinsic and extrinsic parameters calibration.
2. stereo calibration.
2. hand-in-eye and hand-on-eye robot calibration.
3. two robot relative pose calibration.

## Table of Contents
- [Dependencies](#Dependencies) 
- [Board](#Board)
- [Structure](#Structure)
- [Main](#Main)
- [License](#License)


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




## Board
Checkerboard calibration board is the most commonly used and most basic calibration board. 
The general vision system can easily achieve the ideal calibration effect using the checkerboard calibration board.

![image](https://github.com/javapoor/cali/blob/master/image_folder/chessboard.jpg)

Apriltagtags is a common calibration board in the field of robots. Compared with chess board, 
its biggest advantage is that it does not require the calibration board to be fully displayed
 in the camera field of view.
![image](https://github.com/javapoor/cali/blob/master/image_folder/apriltag.png)

## Structure

```
├── readme.md                           // help
├── board                               // apriltag and chess board class
├── config                              // Configuration information
├── calibration_utils                   // calibration utils
├── data                                // example data
├── handineye                           // handineye Pretreatment method and optimization
├── handtoeye                           // handtoeye Pretreatment method and optimization
├── image_folder                        // readme image
├── method                              // hand eye calibration
├── test                                // sample program
└── two_robot_cali_method               // two robot relative pose calibration
```

## Main
### intrinsic and extrinsic calibration
intrinsic and extrinsic calibration is According to the projection model, determine the mapping relationship between 3d points in space and 2d points in picture.


### stereo calibration


### hand eye calibration

### two robot calibration


## Contributors

This project exists thanks to all the people who contribute. 

## License

[NUDT](LICENSE) © Xinxin Zhang



