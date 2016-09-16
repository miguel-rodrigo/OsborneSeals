import cv2
import cv2.xfeatures2d as xf
import pickle
# from src.Keypoints_Pickle import KeypointsPickle as KeyP
import src.EvidenceMatrix as em
from src.FeaturesIO import FeaturesIO


class EliminacionSellos:
    kps_saved = []
    desc_saved = []
    kp_matched = []
    position = (0, 0)  # position is (rows, cols), therefore, (y, x)
    detected_seal = 0

    def __init__(self, img):
        self.img = img
        self.seal_locator = em.SealLocator(img)

    def get_keypoints(self, path):
        self.kps_saved, self.desc_saved = FeaturesIO.load_features(path)

    def get_matched_keypoints(self):
        surf = xf.SURF_create()
        kp_img, des_img = surf.detectAndCompute(self.img, None)

        # FLANN parameters
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)  # or pass empty dictionary

        flann = cv2.FlannBasedMatcher(index_params, search_params)

        max_matches = 0
        matched_seal = 0
        all_kp = []
        for i in range(0, len(self.desc_saved)):
            # good_matches = []
            aux_kp = []

            matches = flann.knnMatch(self.desc_saved[i], des_img, k=2)
            for j, (m, n) in enumerate(matches):
                if m.distance < 0.9 * n.distance:
                    # good_matches.append(m)
                    aux_kp.append(kp_img[m.trainIdx])

            all_kp.append(aux_kp)

        #     if len(good_matches) > max_matches:
        #         max_matches = len(good_matches)
        #         matched_seal = i + 1
        #         self.kp_matched = aux_kp
        #
        # if max_matches < 100:
        #     matched_seal = 0
# TODO: mover constantes de sellos que hay en KeypointsPickle.py
#         self.detected_seal = matched_seal

        return all_kp

    def detect_position(self):
        self.seal_locator.calc_occurrences(self.kp_matched)
        self.position = self.seal_locator.calc_position()

    def remove_seal(self, path):
        div_size = self.seal_locator.DIVISION_SIZE
        seal_img = cv2.imread(path, 0)
        fils, cols = seal_img.shape
        pt1 = (int(self.position[1] * div_size - cols / 2), int(self.position[0] * div_size - fils / 2))
        pt2 = (int(self.position[1] * div_size + cols / 2), int(self.position[0] * div_size + fils / 2))
        cv2.rectangle(self.img, pt1, pt2, (255, 255, 255), -1)
