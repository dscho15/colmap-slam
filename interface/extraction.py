from pathlib import Path
import argparse
import configparser

parser = argparse.ArgumentParser(description='Create a configuration file.')
parser.add_argument('project_name', default="extraction", help='The name of the project.')
parser.add_argument('path', help='The path to the project.')
parser.add_argument('-p_imgs', '--path_to_images', default=None, help='The path to the images.')
args = parser.parse_args()

config = configparser.ConfigParser()

project_name = args.project_name
project_path = Path(args.path)

image_path = project_path / 'images' if args.path_to_images is None else Path(args.path_to_images)
database_path = project_path / 'database.db'

Path.mkdir(project_path, exist_ok=True)
Path.mkdir(image_path, exist_ok=True)

config["General"] = {
    'database_path': database_path,
    'image_path': image_path,
    'camera_mode': -1,
    'descriptor_normalization': 'l1_root'
}

config["ImageReader"] = {
    'camera_model': 'SIMPLE_RADIAL',
        'single_camera': 0,
        'single_camera_per_folder': 0,
        'single_camera_per_image': 0,
        'existing_camera_id': -1,
        'camera_params': '',
        'default_focal_length_factor': 1.2,
        'camera_mask_path': '',
}

config["SiftExtraction"] = {
    'num_threads': -1,
    'use_gpu': 1,
    'gpu_index': -1,
    'max_image_size': 3200,
    'max_num_features': 8192,
    'first_octave': -1,
    'num_octaves': 4,
    'octave_resolution': 3,
    'peak_threshold': 0.0066666666666666671,
    'edge_threshold': 10,
    'estimate_affine_shape': 0,
    'max_num_orientations': 2,
    'upright': 0,
    'domain_size_pooling': 0,
    'dsp_min_scale': 0.16666666666666666,
    'dsp_max_scale': 3,
    'dsp_num_scales': 10,
}

with open(Path(args.path) / (args.project_name + "_extraction.ini"), 'w') as configfile:
    config.write(configfile, space_around_delimiters=True)

# delete the first row in the file
with open(Path(args.path) / (args.project_name + "_extraction.ini"), 'r') as fin:
    data = fin.read().splitlines(True)

with open(Path(args.path) / (args.project_name + "_extraction.ini"), 'w') as fout:
    fout.writelines(data[1:])