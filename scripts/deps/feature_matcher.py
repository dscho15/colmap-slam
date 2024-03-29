import numpy as np
import cv2

class FeatureMatcher:
    ratio_test = 0.5
    fm_ransac_confidence = 0.999
    fm_ransac_reproj_threshold = 1.0
    fm_ransac_method = cv2.RANSAC

    def __init__(
        self,
        norm_type: int = cv2.NORM_L1,
        cross_check: bool = True,
        ratio_test: float = 0.5,
    ) -> None:
        self.cross_check = cross_check
        self.matcher = cv2.BFMatcher(norm_type)
        self.norm_type = norm_type
        self.ratio_test = ratio_test

    def __call__(
        self,
        desc1: np.ndarray,
        desc2: np.ndarray,
        kps1: np.ndarray,
        kps2: np.ndarray,
    ):
        indices1, indices2 = [], []

        init_matches1 = self.matcher.knnMatch(desc1, desc2, k=2)
        init_matches2 = self.matcher.knnMatch(desc2, desc1, k=2)

        matches = []
        for i, (m1, n1) in enumerate(init_matches1):
            cond = True
            
            if self.cross_check:
                is_cross_check_valid = init_matches2[m1.trainIdx][0].trainIdx == i
                cond *= is_cross_check_valid

            if self.ratio_test is not None:
                is_ratio_test_valid = m1.distance <= self.ratio_test * n1.distance
                cond *= is_ratio_test_valid

            if cond:
                matches.append(m1)
                indices1.append(m1.queryIdx)
                indices2.append(m1.trainIdx)

        if type(kps1) is list and type(kps2) is list:
            points1 = np.array([kps1[m.queryIdx].pt for m in matches])
            points2 = np.array([kps2[m.trainIdx].pt for m in matches])
        else:
            points1 = np.array([kps1[m.queryIdx] for m in matches])
            points2 = np.array([kps2[m.trainIdx] for m in matches])
        
        _, mask = cv2.findFundamentalMat(
            points1=points1,
            points2=points2,
            method=self.fm_ransac_method,
            ransacReprojThreshold=self.fm_ransac_reproj_threshold,
            confidence=self.fm_ransac_confidence,
        )

        indices1 = np.array(indices1)[mask.ravel() == 1]
        indices2 = np.array(indices2)[mask.ravel() == 1]

        matches = [(i1, i2) for i1, i2 in zip(indices1, indices2)]
        matches = np.asarray(matches)

        return matches