import argparse
import subprocess
from pathlib import Path
import configparser

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Run COLMAP matcher.')
parser.add_argument('--database_path', default='venice_video/database.db', help='Path to the database file.')
parser.add_argument('--project_path', default='cfgs/matching.ini', help='Path to the project folder.')
parser.add_argument('-c', '--create_cfg', action='store_true', help='Create a configuration file.')
parser.add_argument('-e', '--execute', action='store_true', help='Execute the matcher.')
parser.add_argument('-hx', '--helpx', action='store_true', help='Show this help message and exit.')
args = parser.parse_args()

if args.create_cfg:

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
        'max_error': 4,
        'max_num_matches': 32768,
        'confidence': 0.999,
        'max_num_trials': 10000,
        'min_inlier_ratio': 0.25,
        'min_num_inliers': 15,
        'multiple_models': 0,
        'guided_matching': 0,
        'planar_scene': 0,
        'compute_relative_pose': 0,
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

    # Write the configuration to a file
    with open('cfgs/matching.ini', 'w') as configfile:
        config.write(configfile, space_around_delimiters=True)

# create ini
if args.execute:

    # Build the command to run the matcher
    command = ['colmap', 'sequential_matcher', '--project_path', args.project_path]
    
    if args.helpx:
        command.append('--help')

    print(command)

    # Run the matcher
    subprocess.run(command)