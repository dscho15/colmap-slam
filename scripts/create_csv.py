from deps.colmap_interface import read_extrinsics_text, read_extrinsics_binary
from pathlib import Path
from quaternion import slerp, as_quat_array

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas as pd
import seaborn as sns
import json

def main():

    with open('/home/dts/random/colmap-slam/configs/14657_SW_78th_Ave_Tigard_033.json') as f:
        inputs = json.load(f)

    COLMAP_DICT = read_extrinsics_binary(inputs["COLMAP_PATH"])
    CSV_ORIG = inputs["CSV_ORIG_PATH"]
    P_IMGS = inputs["P_IMGS_PATH"]

    imgs = sorted(list(Path(P_IMGS).rglob('*.png')))
    imgs = [img.name for img in imgs]

    orig_data = pd.read_csv(CSV_ORIG)

    data = pd.DataFrame(columns=['img', 'w', 'x', 'y', 'z'])
    data['img'] = imgs

    for key in COLMAP_DICT:
        quat = COLMAP_DICT[key].qvec
        filename = COLMAP_DICT[key].name
        for key, val in zip(['w', 'x', 'y', 'z'], quat.tolist()):
            data.loc[data['img'] == filename, key] = val        

    orig_data["w"] = np.nan
    orig_data["x"] = np.nan
    orig_data["y"] = np.nan
    orig_data["z"] = np.nan

    j = 0
    for idx, row in orig_data.iterrows():
        if row["is_used"]:
            orig_data.loc[idx, "w"] = data.loc[j, "w"]
            orig_data.loc[idx, "x"] = data.loc[j, "x"]
            orig_data.loc[idx, "y"] = data.loc[j, "y"]
            orig_data.loc[idx, "z"] = data.loc[j, "z"]
            j += 1

    data_nan = orig_data.query('w.isna() or x.isna() or y.isna() or z.isna()')

    indices = data_nan.index.values

    diff = np.where(np.diff(indices) != 1)[0]
    diff = np.insert(diff, 0, 0)
    diff = np.append(diff, len(data_nan) - 1)

    intervals = []
    for i in range(len(diff) - 2):
        idx1 = indices[diff[i]]
        idx2 = indices[diff[i + 1]]
        diff[i + 1] += 1
        intervals.append((idx1, idx2))

    intervals.append((indices[diff[-2] - 1], indices[-1]))

    for (idx1, idx2) in intervals[:-1]:
        
        q1 = orig_data.iloc[idx1 - 1, -4:].values
        q2 = orig_data.iloc[idx2 + 1, -4:].values
        
        slerp_vals = slerp(as_quat_array(q1), as_quat_array(q2), 0, 1, np.linspace(0, 1, idx2 - idx1 + 1))
        slerp_vals = np.array(slerp_vals)
        new_vals = np.zeros((len(slerp_vals), 4))
        
        for j, slerp_val in enumerate(slerp_vals):
            w, (x, y, z) = slerp_val.w, slerp_val.vec
            quat = np.array([w, x, y, z])
            new_vals[j] = quat
        
        orig_data.iloc[idx1:idx2 + 1, -4:] = new_vals

    orig_data.to_csv('data.csv', index=False)

    fig, ax = plt.subplots(2, 2, figsize=(10, 10))

    sns.lineplot(data=orig_data, x=orig_data.index, y='x', ax=ax[0, 0])
    sns.lineplot(data=orig_data, x=orig_data.index, y='y', ax=ax[0, 1])
    sns.lineplot(data=orig_data, x=orig_data.index, y='z', ax=ax[1, 0])
    sns.lineplot(data=orig_data, x=orig_data.index, y='w', ax=ax[1, 1])

    plt.savefig(inputs["PLOT_NAME"] + ".png")
    
if __name__ == "__main__":
    
    main()