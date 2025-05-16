# 封装视频保存逻辑的类
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
    Read all valid images from a specified folder

    Args:
        folder_path: Path to the folder containing images

    Returns:
        List of OpenCV images (numpy arrays)
    """
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
    images = []

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        # Get full file path
        file_path = os.path.join(folder_path, filename)

        # Check if it's a file and has a valid image extension
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(filename)[1].lower()  # Get extension in lowercase
            if file_ext in image_extensions:
                # Read image using OpenCV
                img = cv2.imread(file_path)
                if img is not None:  # Only add successfully read images
                    images.append(img)
    return images

def main()->None:
    # 创建文件的保存的目录
    video_filename = 'output.avi'
    # 创建一个将图片保存为视频的对象
    video_saver = VideoSaver(video_filename, frame_rate=1)  # 初始化视频保存器
    #创建帧计数器
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


if __name__ == '__main__':
    mian()


