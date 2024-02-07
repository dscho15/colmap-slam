# docker pull colmap/colmap:latest
docker run --gpus 0 -w /working -v $1:/working -it colmap/colmap:latest