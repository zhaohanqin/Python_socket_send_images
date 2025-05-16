# 封装视频保存逻辑的类
import cv2
import numpy as np
import os


class VideoSaver:
    """用于管理视频写入的工具类"""

    def __init__(self, video_filename, frame_rate=20):
        self.video_filename = video_filename
        self.frame_rate = frame_rate
        self.video_writer = None  # 视频写入器实例
        self.frame_size = None  # 视频帧尺寸（宽度，高度）

    def write_frame(self, frame):
        """写入单帧图像到视频文件（自动处理首次初始化）"""
        if self.video_writer is None:
            # 首次调用时根据帧尺寸初始化视频写入器
            self.frame_size = (frame.shape[1], frame.shape[0])  # (宽度，高度)
            fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 定义视频编码格式
            self.video_writer = cv2.VideoWriter(
                self.video_filename,
                fourcc,
                self.frame_rate,
                self.frame_size
            )
        self.video_writer.write(frame)  # 写入当前帧

    def release(self):
        """释放视频写入器资源"""
        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None


# 读取一个文件夹下面的所有的文件
def read_images_from_folder(folder_path: str) -> list[np.ndarray]:
    """
    从指定文件夹中读取所有有效图片

    Args,参数:
        folder_path: 包含图片的文件夹路径

    Returns,返回:
        OpenCV图片列表（numpy数组形式）
    """
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
    images = []

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 获取完整文件路径
        file_path = os.path.join(folder_path, filename)

        # 检查是否为文件且具有有效的图片扩展名
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(filename)[1].lower()  # 获取小写格式的文件扩展名
            if file_ext in image_extensions:
                # 使用OpenCV读取图片
                img = cv2.imread(file_path)
                if img is not None:  # 仅添加成功读取的图片
                    images.append(img)

    return images


def main() -> None:
    # 创建文件的保存的目录
    video_filename = '将图片读进视频里面.avi'
    # 创建一个将图片保存为视频的对象
    video_saver = VideoSaver(video_filename, frame_rate=20)  # 初始化视频保存器
    # 创建帧计数器
    frame_count = 0
    # 读取文件夹下面的所有的图片
    folder_path = 'received_images'
    images = read_images_from_folder(folder_path)
    for img in images:
        frame_count += 1  # 帧计数器递增
        # 将图片保存为视频
        video_saver.write_frame(img)
    print('已经成功将文件夹下的文件保存为视频')
    print('视频的总的的帧数为：', frame_count)
    video_saver.release()


def text() -> None:
    veideo = cv2.VideoCapture('./opencv里面的基础操作/2.mp4')  # 打开视频文件
    frame_count = 0
    while True:
        ret, frame = veideo.read()
        if not ret:
            break
        cv2.imshow('video', frame)
        if cv2.waitKey(0) & 0xFF == 27:
            break
        frame_count += 1
        image_file = os.path.join('received_images', f'img_{frame_count:04d}.jpg')
        cv2.imwrite(image_file, frame)
    print('已经成功将视频保存为图片')
    veideo.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
    # text()
