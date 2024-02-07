import ffmpeg
from pathlib import Path
from pprint import pprint as print
import pandas as pd

files = list(Path("/mnt/nvme0/datasets/video_blue_sky/videoes_from_michael/vid7").rglob("*.MP4"))

for f in files:
    meta_data = ffmpeg.probe(f)["streams"]