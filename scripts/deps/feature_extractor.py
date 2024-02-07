import numpy as np
import cv2

class RootSiftExtractor:
    
    def __init__(self, n_features: int) -> None:
        super().__init__()
        self.model = cv2.SIFT_create(nfeatures=n_features)

    def __call__(
        self, image: np.ndarray, mask: np.ndarray = None
    ) -> tuple[np.ndarray, np.ndarray]:
        keypoints, descriptors = self.model.detectAndCompute(image, mask)

        keypoints = np.array([kp.pt for kp in keypoints])
        descriptors = np.array(descriptors)

        if descriptors is not None:
            descriptors /= descriptors.sum(axis=1, keepdims=True) + 1e-7
            descriptors = np.sqrt(descriptors)

        return (keypoints, descriptors)