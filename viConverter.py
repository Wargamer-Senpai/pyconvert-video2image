import sys
import os
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QMessageBox, QLabel, QPushButton, QFileDialog, QSpinBox, QTabWidget, QStyleFactory
from PyQt5.QtGui import QColor, QPalette

class VideoFromImagesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Convert Video and Images")
        self.setGeometry(100, 100, 800, 200)

        main_widget = QWidget(self)
        layout = QVBoxLayout(main_widget)

        self.tabs = QTabWidget()
        self.image_to_video_tab = ImageToVideoTab()
        self.video_to_image_tab = VideoToImageTab()

        self.tabs.addTab(self.image_to_video_tab, "Images to Video")
        self.tabs.addTab(self.video_to_image_tab, "Video to Images")

        layout.addWidget(self.tabs)

        self.setCentralWidget(main_widget)

        # Set the application style to Fusion (dark mode)
        QApplication.setStyle(QStyleFactory.create("Fusion"))
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        QApplication.setPalette(palette)

class ImageToVideoTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.image_folder_path = ""
        self.framerate = 30

        self.image_folder_label = QLabel("Image Folder:")
        self.image_folder_path_label = QLabel("Folder Path: ")
        self.image_folder_button = QPushButton("Select Folder")
        self.image_folder_button.clicked.connect(self.select_image_folder)

        self.framerate_label = QLabel("Framerate:")
        self.framerate_spinbox = QSpinBox()
        self.framerate_spinbox.setRange(1, 60)
        self.framerate_spinbox.setValue(self.framerate)
        self.framerate_spinbox.valueChanged.connect(self.set_framerate)

        self.create_button = QPushButton("Create Video")
        self.create_button.clicked.connect(self.create_video)

        layout.addWidget(self.image_folder_label)
        layout.addWidget(self.image_folder_path_label)
        layout.addWidget(self.image_folder_button)

        layout.addWidget(self.framerate_label)
        layout.addWidget(self.framerate_spinbox)

        layout.addWidget(self.create_button)

        self.video_stats_label = QLabel("")
        layout.addWidget(self.video_stats_label)

    def select_image_folder(self):
        dialog = QFileDialog()
        folder_path = dialog.getExistingDirectory(self, "Select Image Folder")
        if folder_path:
            self.image_folder_path = folder_path
            self.image_folder_path_label.setText(f"Folder Path: {self.image_folder_path}")

    def show_video_stats(self):
        if not self.video_path:
            return

        try:
            cap = cv2.VideoCapture(self.video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = frame_count / fps

            stats_message = f"Framerate: {fps:.2f} fps\nResolution: {width}x{height}\nDuration: {duration:.2f} seconds\nSize: {os.path.getsize(self.video_path) / (1024 * 1024):.2f} MB"

            self.video_stats_label.setText(stats_message)
        except Exception as e:
            self.video_stats_label.setText(f"Error reading video statistics: {str(e)}")
        finally:
            cap.release()

    def set_framerate(self, value):
        self.framerate = value

    def create_video(self):
        if not self.image_folder_path:
            return

        image_files = [f for f in os.listdir(self.image_folder_path) if f.endswith(".jpg") or f.endswith(".png")]
        if not image_files:
            return

        image_files.sort()
        images = [cv2.imread(os.path.join(self.image_folder_path, file)) for file in image_files]

        height, width, channels = images[0].shape

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        video_path, _ = QFileDialog.getSaveFileName(self, "Save Video", "", "Video Files (*.mp4)")
        if not video_path:
            return

        video = cv2.VideoWriter(video_path, fourcc, self.framerate, (width, height))

        for image in images:
            video.write(image)

        video.release()

        self.show_message("Video has been created.")

    def show_message(self, message):
        msg_box = QMessageBox(self)
        msg_box.setText(message)
        msg_box.exec_()

class VideoToImageTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.video_path = ""
        self.image_folder_path = ""

        self.video_label = QLabel("Video:")
        self.video_path_label = QLabel("Video Path: ")
        self.video_button = QPushButton("Select Video")
        self.video_button.clicked.connect(self.select_video)

        self.image_folder_label = QLabel("Image Folder:")
        self.image_folder_path_label = QLabel("Folder Path: ")
        self.image_folder_button = QPushButton("Select Folder")
        self.image_folder_button.clicked.connect(self.select_image_folder)

        self.extract_button = QPushButton("Extract Images")
        self.extract_button.clicked.connect(self.extract_images)

        layout.addWidget(self.video_label)
        layout.addWidget(self.video_path_label)
        layout.addWidget(self.video_button)

        layout.addWidget(self.image_folder_label)
        layout.addWidget(self.image_folder_path_label)
        layout.addWidget(self.image_folder_button)

        layout.addWidget(self.extract_button)

        self.video_stats_label = QLabel("")
        layout.addWidget(self.video_stats_label)

    def select_video(self):
        dialog = QFileDialog()
        video_path, _ = dialog.getOpenFileName(self, "Select Video", "", "Video Files (*.mp4);;All Files (*)")
        if video_path:
            self.video_path = video_path
            self.video_path_label.setText(f"Video Path: {self.video_path}")
            self.show_video_stats()

    def show_video_stats(self):
        if not self.video_path:
            return

        try:
            cap = cv2.VideoCapture(self.video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = frame_count / fps

            stats_message = f"Framerate: {fps:.2f} fps\nResolution: {width}x{height}\nDuration: {duration:.2f} seconds\nSize: {os.path.getsize(self.video_path) / (1024 * 1024):.2f} MB"

            self.video_stats_label.setText(stats_message)
        except Exception as e:
            self.video_stats_label.setText(f"Error reading video statistics: {str(e)}")
        finally:
            cap.release()

    def select_image_folder(self):
        dialog = QFileDialog()
        folder_path = dialog.getExistingDirectory(self, "Select Destination Folder")
        if folder_path:
            self.image_folder_path = folder_path
            self.image_folder_path_label.setText(f"Folder Path: {self.image_folder_path}")

    def extract_images(self):
        if not self.video_path or not self.image_folder_path:
            return

        try:
            cap = cv2.VideoCapture(self.video_path)
            count = 0

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                image_path = os.path.join(self.image_folder_path, f"frame{count:04d}.jpg")
                cv2.imwrite(image_path, frame)

                count += 1
        except Exception as e:
            self.show_message(f"Error extracting images: {str(e)}")
        else:
            self.show_message(f"{count} images extracted.")
        finally:
            cap.release()

    def show_message(self, message):
        msg_box = QMessageBox(self)
        msg_box.setText(message)
        msg_box.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoFromImagesApp()
    window.show()
    sys.exit(app.exec_())
