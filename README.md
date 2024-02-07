
# install:
conda install pytorch=1.13.0 torchvision pytorch-cuda=11.6 -c pytorch -c nvidia
conda install -c fvcore -c iopath -c conda-forge fvcore iopath
conda install -c bottler nvidiacub



# commands: 
colmap feature_extractor --project_path configs/extraction.ini
colmap sequential_matcher --project_path configs/matching.ini
colmap mapper --project_path configs/mapping.ini