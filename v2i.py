import cv2
import os

def extract_frames(input_file, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(input_file)
    if not cap.isOpened():
        print("Error while opening video file.")
        return

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        output_file = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(output_file, frame)

    cap.release()
    print(f"{frame_count} Images has been extraced and saved to '{output_folder}'.")

if __name__ == "__main__":
    # Change paths here (windows/linux path possible)
    video_file = "C:\\Your\\Path\\Here\\46712827.mp4"
    output_folder = "C:\\Your\\Path\\Here\\newFolder"
    extract_frames(video_file, output_folder)
