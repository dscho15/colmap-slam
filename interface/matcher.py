import argparse
from pathlib import Path
import configparser

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Run COLMAP matcher.')
parser.add_argument('database_path', help='Path to the database file.')
parser.add_argument('image_path', help='Path to the images folder.')
parser.add_argument('project_name', help='The name of the project.')
parser.add_argument('path', help='The path to the project.')
args = parser.parse_args()

config = configparser.ConfigParser()

config["General"] = {
    'database_path': args.database_path,
}

# Define the configuration for the matcher
config["SiftMatching"] = {
    'num_threads': -1,
    'use_gpu': 1,
    'gpu_index': -1,
    'max_ratio': 0.8,
    'max_distance': 0.7,
    'cross_check': 1,
    'max_num_matches': 32768,
}

config["TwoViewGeometry"] = {
    'max_error': 4,
    'confidence': 0.999,
    'min_num_inliers': 15,
    'compute_relative_pose': 0,
    'max_num_trials': 10000,
    'min_num_inliers': 15,
    'multiple_models': 0
}

config["SequentialMatching"] = {
    'overlap': 10,
    'quadratic_overlap': 1,
    'loop_detection': 0,
    'loop_detection_period': 10,
    'loop_detection_num_images': 50,
    'loop_detection_num_nearest_neighbors': 1,
    'loop_detection_num_checks': 256,
    'loop_detection_num_images_after_verification': 0,
    'loop_detection_max_num_features': -1,
    'vocab_tree_path': '',  # You need to provide the path to the vocabulary tree file
}

path_to_cfg = Path(args.path) / (args.project_name + "_matcher.ini")

with open(path_to_cfg, 'w') as configfile:
    config.write(configfile, space_around_delimiters=True)

# delete the first row in the file
with open(path_to_cfg, 'r') as fin:
    data = fin.read().splitlines(True)

with open(path_to_cfg, 'w') as fout:
    fout.writelines(data[1:])