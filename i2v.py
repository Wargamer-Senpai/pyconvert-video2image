import cv2
import os

def images_to_video(input_folder, output_file, frame_rate=30):
    image_files = [f for f in os.listdir(input_folder) if f.endswith(".jpg")]
    if not image_files:
        print("No Images (.jpg) in input folder found.")
        return

    image_files.sort()

    first_image = cv2.imread(os.path.join(input_folder, image_files[0]))
    height, width, _ = first_image.shape

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_file, fourcc, frame_rate, (width, height))

    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        frame = cv2.imread(image_path)
        out.write(frame)

    out.release()
    print(f"Video '{output_file}' has been created.")

if __name__ == "__main__":
    # Change paths here (windows/linux path possible)
    output_file = "C:\\Your\\Path\\Here\\46712827.mp4"
    input_folder = "C:\\Your\\Path\\Here\\newFolder"
    images_to_video(input_folder, output_file)
