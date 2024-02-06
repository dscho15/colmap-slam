import configparser
from argparse import ArgumentParser

# Parse command-line arguments
parser = ArgumentParser(description='Run COLMAP mapper.')
parser.add_argument('--project_path', default='configs/mapping.ini', help='Path to the project folder.')
parser.add_argument('--database_path', default='venice_video/database.db', help='Path to the database file.')
parser.add_argument('--output_path', default='venice_video/sparse', help='Path to the output folder.')
parser.add_argument('--image_path', default='venice_video/images', help='Path to the images folder.')
parser.add_argument('-c', '--create_cfg', action='store_true', help='Create a configuration file.')
parser.add_argument('-e', '--execute', action='store_true', help='Execute the mapper.')
parser.add_argument('-hx', '--helpx', action='store_true', help='Show this help message and exit.')
args = parser.parse_args()

if args.create_cfg:

    config = configparser.ConfigParser()

    config['Default'] = {
        'random_seed': 0,
        'log_to_stderr': 0,
        'log_level': 2,
        'database_path': f'{args.database_path}',  # You need to provide the path
        'image_path': f'{args.image_path}',  # You need to provide the path,
        'output_path': f'{args.output_path}',  # You need to provide the path
    }

    config['Mapper'] = {
        'min_num_matches': 15,
        'ignore_watermarks': 0,
        'multiple_models': 1,
        'max_num_models': 50,
        'max_model_overlap': 20,
        'min_model_size': 10,
        'init_image_id1': -1,
        'init_image_id2': -1,
        'init_num_trials': 200,
        'extract_colors': 1,
        'num_threads': -1,
        'min_focal_length_ratio': 0.1,
        'max_focal_length_ratio': 10,
        'max_extra_param': 1,
        'ba_refine_focal_length': 1,
        'ba_refine_principal_point': 0,
        'ba_refine_extra_params': 1,
        'ba_min_num_residuals_for_multi_threading': 50000,
        'ba_local_num_images': 6,
        'ba_local_function_tolerance': 0,
        'ba_local_max_num_iterations': 25,
        'ba_global_pba_gpu_index': -1,
        'ba_global_images_ratio': 1.1,
        'ba_global_points_ratio': 1.1,
        'ba_global_images_freq': 500,
        'ba_global_points_freq': 250000,
        'ba_global_function_tolerance': 0,
        'ba_global_max_num_iterations': 50,
        'ba_global_max_refinements': 5,
        'ba_global_max_refinement_change': 0.0005,
        'ba_local_max_refinements': 2,
        'ba_local_max_refinement_change': 0.001,
        'snapshot_path': '',  # You need to provide the path
        'snapshot_images_freq': 0,
        'fix_existing_images': 0,
        'init_min_num_inliers': 100,
        'init_max_error': 4,
        'init_max_forward_motion': 0.95,
        'init_min_tri_angle': 16,
        'init_max_reg_trials': 2,
        'abs_pose_max_error': 12,
        'abs_pose_min_num_inliers': 30,
        'abs_pose_min_inlier_ratio': 0.25,
        'filter_max_reproj_error': 4,
        'filter_min_tri_angle': 1.5,
        'max_reg_trials': 3,
        'local_ba_min_tri_angle': 6,
        'tri_max_transitivity': 1,
        'tri_create_max_angle_error': 2,
        'tri_continue_max_angle_error': 2,
        'tri_merge_max_reproj_error': 4,
        'tri_complete_max_reproj_error': 4,
        'tri_complete_max_transitivity': 5,
        'tri_re_max_angle_error': 5,
        'tri_re_min_ratio': 0.2,
        'tri_re_max_trials': 1,
        'tri_min_angle': 1.5,
        'tri_ignore_two_view_tracks': 1,
    }

    # Write the configuration to a file
    with open(args.project_path, 'w') as configfile:
        config.write(configfile)

if args.execute:

    import subprocess

    # Build the command to run the mapper
    command = ['colmap', 'mapper', '--project_path', 'cfgs/mapping.ini']

    if args.helpx:
        command.append('--help')
    
    print(command)

    # Run the mapper
    subprocess.run(command)