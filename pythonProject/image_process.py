import base64
import re

from PIL import Image
from io import BytesIO

'''图像处理，各种类型的图片都在此处理'''
def base64_2_picture(url):
    '''
    一种常用语html编码中的图片格式，比直接url更快更便捷
    :param url: 传入以Base64 编码的图片数据，形如：data:image/png;base64,iVBORwxxxxxxxxxxxx
    :return:恢复完成的image图像
    '''
    #首先将编码进行拆分
    data_index = url.find('base64,') + len('base64,')
    encoded_data = url[data_index:]

    # 解码Base64数据为二进制文件
    decoded_data = base64.b64decode(encoded_data)
    # 将解码后的数据转换成图像，利用PIL库来将二进制文件转为图片
    image = Image.open(BytesIO(decoded_data))
    # 保存图像到本地
    image.save('/Users/haonan/Desktop/image.png')
    return image

def get_block_w_h_JD(string):
    '''

    :param string: html代码中出现滑块的宽和高
    :return: 滑块的宽和高
    '''
    pa_h = r'top:\s*([\d.]+)px'
    pa_w=r'width:\s*([\d.]+)px'
    if re.search(pa_w,string):
        w=float(re.search(pa_w,string).group(1))
    else:
        print('未找到宽')
    if re.search(pa_h,string):
        h=float(re.search(pa_h,string).group(1))
    else:
        print('未发现高')
    return w,h