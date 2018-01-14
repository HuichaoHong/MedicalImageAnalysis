import numpy as np
import matplotlib.pyplot as plt


# 设置默认显示参数
plt.rcParams['figure.figsize'] = (10, 10)  # 图像显示大小
plt.rcParams['image.interpolation'] = 'nearest'  # 最近邻差值: 像素为正方形
plt.rcParams['image.cmap'] = 'gray'
import sys
caffe_root = 'C:/Users/Administrator/Desktop/ore/MatlabCaffe/caffe/'
#sys.path.insert(0, caffe_root + 'python')
import caffe


def vis_square(data):
    # 输入一个形如：(n, height, width) or (n, height, width, 3)的数组，并对每一个形如(height,width)的特征进行可视化

    # 正则化数据
    data = (data - data.min()) / (data.max() - data.min())

    # 将滤波器的核转变为正方形
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = (((0, n ** 2 - data.shape[0]),
                (0, 1), (0, 1))  # 在相邻的滤波器之间加入空白
               + ((0, 0),) * (data.ndim - 3))  # 不扩展最后一维
    data = np.pad(data, padding, mode='constant', constant_values=1)  # 扩展一个像素(白色)

    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])

    plt.imshow(data)
    plt.axis('off')
    plt.show()

caffe.set_mode_gpu()
model_def = caffe_root + 'models/bvlc_reference_caffenet/3_non/deploy.prototxt'    #注意这里使用deploy.prototxt
model_weights = caffe_root + 'models/bvlc_reference_caffenet/3_non/3_non_iter_10000.caffemodel'
net = caffe.Net(model_def,      # 定义模型结构
                model_weights,  # 包含了模型的训练权值
                caffe.TEST)     # 使用测试模式(不执行dropout



# 对输入数据进行变换
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2, 0, 1))  # 还没弄清楚？
transformer.set_raw_scale('data', 255)  # 将像素值从[0,255]变换到[0,1]之间
transformer.set_channel_swap('data', (2, 1, 0))  # 交换通道，从RGB变换到BGR

net.blobs['data'].reshape(50,        # batch 大小
                          3,         # 3-channel (BGR) images
                          227, 227)  # 图像大小为:227x227
image = caffe.io.load_image(caffe_root + 'examples/images/cat.jpg')
transformed_image = transformer.preprocess('data', image)
plt.imshow(image)

# 将图像数据拷贝到为net分配的内存中
net.blobs['data'].data[...] = transformed_image

# 执行分类
output = net.forward()
output_prob = output['prob'][0]  # batch中第一张图像的概率值
print 'predicted class is:', output_prob.argmax()

for layer_name, blob in net.blobs.iteritems():
      print layer_name + '\t' + str(blob.data.shape)

for layer_name, param in net.params.iteritems():
       print layer_name + '\t' + str(param[0].data.shape), str(param[1].data.shape)

filters = net.params['conv1'][0].data
vis_square(filters.transpose(0, 2, 3, 1))

feat = net.blobs['conv1'].data[0, :36]
vis_square(feat)

feat = net.blobs['pool5'].data[0]
vis_square(feat)

feat = net.blobs['fc6'].data[0]
plt.subplot(2, 1, 1)
plt.plot(feat.flat)
plt.subplot(2, 1, 2)
_ = plt.hist(feat.flat[feat.flat > 0], bins=100)
plt.show()