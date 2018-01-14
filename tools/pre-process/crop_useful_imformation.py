# coding=gbk
#Author      ：honghuichao
#Data        ：2017-0903
#Tel         ：18016620691
#功能        ：
#使用说明    ：只需使用load_Img(src,dst)即可完成一个文件夹src所有文件的数据无关空白部分的裁剪，最后保存至dst

"""数据增强
   1. 翻转变换 flip
   2. 随机修剪 random crop
   3. 色彩抖动 color jittering
   4. 平移变换 shift
   5. 尺度变换 scale
   6. 对比度变换 contrast
   7. 噪声扰动 noise
   8. 旋转变换/反射变换 Rotation/reflection

"""
import os
import cv2
import numpy as np

def load_Img(imgDir,save):
    for root,dirs,files in os.walk(imgDir):
        for file in files:
            img_path= os.path.join(root,file)
            print img_path
            image = cv2.imread(img_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gradX = cv2.Sobel(gray, ddepth=cv2.cv.CV_32F, dx=1, dy=0, ksize=-1)
            gradY = cv2.Sobel(gray, ddepth=cv2.cv.CV_32F, dx=0, dy=1, ksize=-1)
            # subtract the y-gradient from the x-gradient
            gradient = cv2.subtract(gradX, gradY)
            gradient = cv2.convertScaleAbs(gradient)
            # blur and threshold the image
            blurred = cv2.blur(gradient, (9, 9))
            (_, thresh) = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
            closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            # perform a series of erosions and dilations
            closed = cv2.erode(closed, None, iterations=4)
            closed = cv2.dilate(closed, None, iterations=4)
            (cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

            # compute the rotated bounding box of the largest contour
            rect = cv2.minAreaRect(c)
            box = np.int0(cv2.cv.BoxPoints(rect))

            # draw a bounding box arounded the detected barcode and display the image
            # cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
            Xs = [i[0] for i in box]
            Ys = [i[1] for i in box]
            x1 = min(Xs)
            x2 = max(Xs)
            y1 = min(Ys)
            y2 = max(Ys)
            hight = y2 - y1
            width = x2 - x1
            cropImg = image[y1:y1 + hight, x1:x1 + width]
            cv2.imwrite(save+"/"+file, cropImg)

            cv2.waitKey(0)


if __name__ == '__main__':
    load_Img("C:\\Users\\Administrator\\Desktop\\煤矸石",
             "C:\\Users\\Administrator\\Desktop\\gan")





