import os
import shutil

def filter_and_move_images(input_folder, jpg_output_folder, raw_output_folder):
    if not os.path.exists(jpg_output_folder):
        os.makedirs(jpg_output_folder)
    if not os.path.exists(raw_output_folder):
        os.makedirs(raw_output_folder)

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith('.jpg'):
                input_file_path = os.path.join(root, file)
                output_file_path = os.path.join(jpg_output_folder, file)
                shutil.move(input_file_path, output_file_path)
                print(f"已移动 JPG 文件: {input_file_path} 到 {output_file_path}")
            else:
                input_file_path = os.path.join(root, file)
                output_file_path = os.path.join(raw_output_folder, file)
                shutil.move(input_file_path, output_file_path)
                print(f"已移动 RAW 文件: {input_file_path} 到 {output_file_path}")

input_folder = 'src/selection/input'
jpg_output_folder = 'src/selection/jpg'
raw_output_folder = 'src/selection/raw'

filter_and_move_images(input_folder, jpg_output_folder, raw_output_folder)
