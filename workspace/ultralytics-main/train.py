# train_yolo.py

from ultralytics import YOLO

def main():
    # 选择模型，可以是 'yolov8n.pt', 'yolov8s.pt', 'yolov8m.pt', 'yolov8l.pt', 'yolov8x.pt'
    model = YOLO("yolo11n.pt")   # 加载预训练模型

    # 开始训练
    model.train(
        data="data.yaml",     # 数据集配置文件
        epochs=100,              # 训练轮数
        imgsz=640,               # 输入图片大小
        batch=16,                # batch size
        device=0,                # GPU编号，CPU可写 'cpu'
        workers=4,               # 数据加载线程
        name="yolo_exp"          # 保存结果的文件夹名
    )

if __name__ == "__main__":
    main()
