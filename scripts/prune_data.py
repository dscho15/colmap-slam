from pathlib import Path
from pprint import pprint

import concurrent.futures
import shutil
import pandas as pd
import cv2
import numpy as np
import json

from tqdm import tqdm
from deps.feature_matcher import FeatureMatcher
from deps.feature_extractor import RootSiftExtractor

from argparse import ArgumentParser

if __name__ == "__main__":

    # argparse input json
    args = ArgumentParser()
    args.add_argument("config", type=str, help="Path to the configuration file.")
    args = args.parse_args()

    with open(args.config) as f:
        json_data = json.load(f)

    flag = False
    if not json_data:
        flag = True
        json_data = {
            "path_to_data": "",
            "path_to_sampled_data": "",
            "save_cfg_path": "",
            "file_ext": ".jpg",
            "max_n_features": 8192,
            "median_tsh": 5.0,
            "verbose": True,
            "skip_prune": False
        }
    
    # save the configuration file
    with open(args.config, 'w') as f:
        json.dump(json_data, f, indent=4)
        
    if flag:
        print("Please fill in the configuration file and run the script again.")
        exit(0)
    
    def print_verbose(msg):
        if json_data["verbose"]:
            print(msg)
                    
    if not json_data["skip_prune"]:
        
        file_ext = json_data["file_ext"]
        image_paths = list(Path(json_data["path_to_data"]).rglob(f"*{file_ext}"))
        image_paths = sorted(image_paths)
        image_paths = [str(image.absolute()) for image in image_paths]
        
        print_verbose(f"Number of images: {len(image_paths)}")
        
        def load_image(image_path, grayscale: bool = True):
            return cv2.imread(image_path, cv2.IMREAD_GRAYSCALE if grayscale else cv2.IMREAD_COLOR)
        
        with concurrent.futures.ProcessPoolExecutor() as executor:
            images = list(tqdm(executor.map(load_image, image_paths), total=len(image_paths)))

        feature_extractor = RootSiftExtractor(json_data["max_n_features"])
        feature_matcher = FeatureMatcher()
        processed_images = []
        used = []
        prev_img = None

        output_dict = {
            "images": processed_images,
            "is_used": used
        }

        for i, img in tqdm(enumerate(image_paths)):
            
            processed_images.append(img)
            
            if prev_img is None:
                
                prev_img = images[i]
                (prev_kps, prev_desc) = feature_extractor(prev_img)
                
                used.append(True)
            
            else:
                
                cur_img = images[i]
                (cur_kps, cur_desc) = feature_extractor(cur_img)
                    
                matches = feature_matcher(prev_desc, cur_desc, prev_kps, cur_kps)

                matches = np.array(matches)
                distances = np.linalg.norm(prev_kps[matches[:, 0]] - cur_kps[matches[:, 1]], axis=1)
                
                median_distance, standard_deviation = np.median(distances), np.std(distances)
                
                print_verbose(f"Median distance: {median_distance}, number of matches: {len(matches)}, std: {standard_deviation}")
                
                if median_distance > json_data["median_tsh"]:
                    
                    prev_img = cur_img
                    prev_kps, prev_desc = cur_kps, cur_desc
                    used.append(True)
                
                else:
                    
                    used.append(False)

            if i % 25 == 0:
                
                output_dict["is_used"] = used
                
                dataframe = pd.DataFrame(output_dict)
                dataframe.to_csv(json_data["save_cfg_path"], index=False)

        print("Pruning done, exiting.")
        exit()
        
    print("Pruning skipped, sampling data required for colmap")
    
    dataframe = pd.read_csv(json_data["save_cfg_path"])
    sample_data_p = Path(json_data["path_to_sampled_data"])
    sample_data_p.mkdir(parents=True, exist_ok=True)
    
    j = 0
    for i, row in tqdm(dataframe.iterrows()):
        
        img = row["images"]
        
        if row["is_used"]:

            idx = f"{j}".zfill(5)
            o = sample_data_p / f"image_{idx}.jpg"
            shutil.copy(img, o)
            j += 1
