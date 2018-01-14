# coding=utf-8

'''%%
%Author        : honghuichao
%Data          : 2018-08-31

%brief         ：求解一个分类器的召回率、精确率、准确率；
%note          : 针对二类分任务还有F1指标，AOC，AUC指标

% 参数(二分类)  ：把正类预测正类（TP）
%              ：把负类预测正类（FP）
%              ：把正类预测负类（FN）
%　　　　　　　 : 把负类预测成负类（TN）
%              ：TF-- 错分
%              ：NP-- 预测成N或P
%              : Acc Acc=(TP+TN)/(TP+TN+FP+FN)
%              : Rec Rec=TP/(TP+FN)
%              : Pre Pre=TP/(TP+FP)
%              : F1  F1=2*R*P/(R+P)

%参数（多分类） ：mii--
%              ：mjj--
%              ：mij--
%              ：mji--
%              ：Recg Recg=sum()
%%
# https://www.zhihu.com/question/19645541
'''
import os
import caffe
import numpy as np

def Test(img, label):
    net = caffe.Net(deploy, caffe_model, caffe.TEST)  # 加载model和network

    # 图片预处理设置
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})  # 设定图片的shape格式(1,3,28,28)
    transformer.set_transpose('data', (2, 0, 1))  # 改变维度的顺序，由原始图片(28,28,3)变为(3,28,28)
    # transformer.set_mean('data', np.load(mean_file).mean(1).mean(1))    #减去均值，前面训练模型时没有减均值，这儿就不用
    transformer.set_raw_scale('data', 255)  # 缩放到【0，255】之间
    transformer.set_channel_swap('data', (2, 1, 0))  # 交换通道，将图片由RGB变为BGR

    im = caffe.io.load_image(img)  # 加载图片
    net.blobs['data'].data[...] = transformer.preprocess('data', im)  # 执行上面设置的图片预处理操作，并将图片载入到blob中

    # 执行测试
    out = net.forward()

    prob = net.blobs['prob'].data[0].flatten()  # 取出最后一层（prob）属于某个类别的概率值，并打印,'prob'为最后一层的名称
    # print prob
    predict = prob.argsort()[-1]
    print prob.argsort()[-1]  # 将概率值排序，取出最大值所在的序号 ,9指的是分为0-9十类
    if predict == label:
        return 1
    else:
        return 0

        # argsort()函数是从小到大排列
        # print 'the class is:',labels[order]   #将该序号转换成对应的类别名称，并打印
        # f=file("/home/liuyun/caffe/examples/DR_grade/label.txt","a+")
        # f.writelines(img+' '+labels[order]+'\n')


if __name__ == "__main__":
    root = 'C:/Users/Administrator/Desktop/MatlabCaffe/caffe/'  # 根目录
    deploy = root + 'models/bvlc_alexnet/2_non/deploy_2_non.prototxt'  # deploy文件
    caffe_model = root + 'models/bvlc_alexnet/2_non/2_non_iter_45000.caffemodel'  # 训练好的 caffemodel
    dir = root + 'data/CharacterDiscrimination/train/'
    filelist = []
    filenames = os.listdir(dir)
    label = 1
    labels_file = open("C:/Users/Administrator/Desktop/MatlabCaffe/tools/qq.txt")  # 返回一个文件对象
    labels = labels_file.readlines()
    for label in labels:
        file_name = label.split(' ', 1)[0]
        lab = label.split(' ', 1)[1]
        fullfilename = os.path.join(dir, file_name)
        print fullfilename
        print Test(fullfilename, label)



