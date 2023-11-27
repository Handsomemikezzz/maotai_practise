# 采用cv库来求解滑动验证中滑块的移动距离问题
import cv2 as cv
import random
import numpy as np
def get_edges(image):
    '''
    :param image: 传入图像
    :return: 得到图像内的所有边缘图（灰度图）
    '''
    picture = cv.imread(image)
    #高斯算法去噪
    picture = cv.GaussianBlur(picture,ksize=(5,5),sigmaX=0)
    #转为二值图像：
    gray_picture=  cv.cvtColor(picture,cv.COLOR_BGR2GRAY)
    #Canny边缘检测得到图像中的边缘信息
    edges = cv.Canny(gray_picture,threshold1=200,threshold2=500)
    #提取轮廓
    target_edges = cv.findContours(edges,mode=cv.RETR_CCOMP,method=cv.CHAIN_APPROX_SIMPLE)

    contour_image  =np.zeros_like(picture)#创建大小相同的空白图像
    cv.drawContours(contour_image,target_edges[0],-1,(255,255,255),1)
    cv.imwrite('/Users/haonan/Desktop/image_edge.png',contour_image)

    return target_edges

def get_area_range(w,h):
    '''在html代码中读取到滑块的长度w 与高度
    传入此函数通过设定误差范围为正负0.2即可得到面积筛选
    '''
    min_area = w*h*0.64
    max_area = w*h*1.44
    return min_area,max_area
def get_perimeter_range(w,h):
    '''周长范围'''
    min = 0.8*(w+h)
    max = 1.2*(w+h)
    return min,max

def get_offset_threshold(w):
    '''定义边缘的偏移量
    即x值的范围，因为边缘本身就有一定的距离，所以其偏移量也应在一定的范围内'''
    min = 0.2*w
    max = 0.85*w
    return  min,max


def get_distance(image,w,h):
    '''

    :param image: 传入的图像
    :param w: 图像的宽：通过页面代码读取
    :param h: 图像的高：页面代码读取
    :return: 缺口位置的x位置坐标，若想得到滑动距离，则需要减去滑块的w（滑块其实位置在图片左方时）
    '''
    contour_area_min, contour_area_max = get_area_range(w,h)
    arc_length_min, arc_length_max = get_perimeter_range(w,h)
    offset_min, offset_max = get_offset_threshold(w)
    offset = None
    edges = get_edges(image)
    for edge in edges:
        x,y,wid,hie = cv.boundingRect(edge)
        if contour_area_min<cv.contourArea(edge)<contour_area_max and \
            arc_length_min<cv.arcLength(edge,True)<arc_length_max and \
            offset_min<x<offset_max:
            #标注目标图像
            cv.rectangle(image,(x,y),(x+wid,y+hie),(0,0,255),2)
            offset=x
    cv.imwrite('target_image.png',image)
    print('缺口位置坐标',offset)


def gen_move_track(distance):
    '''
    为了避免检测出机器的滑动，我们需要自定义一个滑动轨迹
    1.是一个变加速运动
    2.可以先超过目标，再往回移动，模拟人类情况
    :return:
    '''
    track = []
    x= 0
    max_distance=distance+20
    mid = distance*0.6
    current = 0
    v = 0#初速度
    a=random.randint(3,5)
    dt=0.2
    while x<distance:
        if x<mid:
            a+=1
        else:
            a-=1
        v0=v+a*dt
        v=v0+a*dt#当前速度
        x = v0*dt+0.5*a*dt*dt
        current+=x
        track.append(round(x))
    return track











