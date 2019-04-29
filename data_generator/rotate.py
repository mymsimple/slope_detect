
import logging
from PIL import Image, ImageDraw, ImageFont, ImageFilter,ImageOps
import random
import os
logger = logging.getLogger("rotate")
ROTATE_ANGLE = 30        # 随机旋转角度
classes_name = ["正图","90度","180度","270度"]
degrees = [0,90,180,270]

def init_logger():
    logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s',
        level=logging.DEBUG,
        handlers=[logging.StreamHandler()])


def degree_rotate(img,degree):
    # 宽和高
    w, h = img.size
    # 中心点
    center = (w // 2, h // 2)
    logger.debug("指定角度旋转度数:%f" % degree)
    return img.rotate(degree,center=center,expand=1)


def process_folder(dir,type):
    label_file_name = os.path.join("data",type+".txt")

    label_file = open(label_file_name,"w")
    target_dir = os.path.join("data",type)

    for image_name in os.listdir(dir):
        file_name = os.path.join(dir, image_name)
        _,type = os.path.splitext(file_name)
        if type in ['.jpg','.png','.JPG','.jpeg','.PNG']:
            logger.debug("处理原始图片:%s", file_name)
            rotate_one_image(file_name,label_file,target_dir)
        else:
            logger.warning("警告：文件%s不是图片，忽略",file_name)
            continue
    label_file.close()


#旋转一张图片
def rotate_one_image(raw_image_name,label_file,target_dir):
    for i in range(4):
        d = degrees[i]
        # 原图
        image = Image.open(raw_image_name)
        # 按4个方向要求旋转先
        image = degree_rotate(image,d)
        # 得到文件名和后缀
        (filepath, tempfilename) = os.path.split(raw_image_name)
        name,subfix = os.path.splitext(tempfilename)
        name+= "_" + str(i)
        logger.debug("产生%s的图：%s", classes_name[i], name)
        rotate_one_direction(image,name,subfix,label_file,target_dir,i)


# 旋转一个角度，每一个角度生成5~10个样本并存储
def rotate_one_direction(image,image_name,subfix,label_file,target_dir,clazz):
    random_num = random.randint(5,10)  # 5~10的随机数
    for i in range(1, random_num):
        name = image_name+"_"+str(i)
        rotated_file_name = os.path.join(target_dir,name+subfix)

        small_degree = random.uniform(-ROTATE_ANGLE, ROTATE_ANGLE)  # 随机旋转0-30度
        rotated_file = degree_rotate(image,small_degree)
        rotated_file.save(rotated_file_name)

        label_file.write(rotated_file_name)
        label_file.write(" ")
        label_file.write(str(clazz))
        label_file.write("\n")

        logger.debug("保存旋转后的图片&标签：%s", rotated_file_name)


# 把指定目录下的文件都旋转，生成测试和验证代码
if __name__ == '__main__':

    import argparse

    init_logger()

    parser = argparse.ArgumentParser()
    parser.add_argument("--type") # 啥类型的数据啊，train/validate/test
    parser.add_argument("--dir")  # 这个程序的主目录
    args = parser.parse_args()
    DATA_DIR = args.dir
    TYPE= args.type

    images_dir = os.path.join("data",TYPE)
    if not os.path.exists(images_dir): os.makedirs(images_dir)

    process_folder(DATA_DIR, TYPE)
