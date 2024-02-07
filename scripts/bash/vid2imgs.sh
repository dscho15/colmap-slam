#!/bin/bash

# Input parameters
video_path=$1
output_path=$2

# Check if output directory exists, create it if not
if [ ! -d "$output_path" ]; then
  mkdir -p $output_path
fi

fps=$(ffprobe -v error -select_streams v -of default=noprint_wrappers=1:nokey=1 -show_entries stream=avg_frame_rate $video_path | bc -l)
fps=$(printf "%.0f\n" $fps)

echo "FPS: $fps"


# Extract frames
ffmpeg -i $video_path -vf "fps=$fps" $output_path/image_%05d.jpg

#  ./vid2imgs.sh /mnt/nvme0/datasets/video_blue_sky/videoes_from_michael/vid7/C0055.MP4 /mnt/nvme0/datasets/video_blue_sky/videoes_from_michael/vid7/FRAMES/C0055/
