# Import the modules
import cv2
from sklearn.externals import joblib
from skimage.feature import hog
import numpy as np

# Load the classifier
clf = joblib.load("digits_cls2.pkl")


class DigitDetection:
    def __init__(self, classifier):
        self.clf = joblib.load(classifier)

    def _get_ctrs(self, image, is_src=True):
        if is_src:
            im = cv2.imread(image)
        else:
            im = image

        # Convert to grayscale and apply Gaussian filtering
        im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)

        # Threshold the image
        ret, im_th = cv2.threshold(im_gray, 90, 255, cv2.THRESH_BINARY_INV)
        # Find contours in the image
        ctrs, hier = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL,
                                      cv2.CHAIN_APPROX_SIMPLE)

        return ctrs, im, im_th

    def get_rectangles(self, image, is_src=True):
        ctrs, im, im_th = self._get_ctrs(image, is_src)
        # Get rectangles contains each contour
        rects = [cv2.boundingRect(ctr) for ctr in ctrs]
        rects = sorted(rects, key=lambda x: x[1], reverse=False)
        rects_blocks = [rects[slice(i, i + 4, 1)] for i in
                        range(0, len(rects), 4)]

        # len_vert = sum([item[0][2] for item in rects_blocks])
        # len_hor = sum([item[3] for item in rects_blocks[0]])
        # print(rects_blocks, "RECTS blocks")
        rects = []

        x_start_all = []
        farthest_right_x_all = []
        for block in rects_blocks:
            sorted_block = sorted(block, key=lambda x: x[0])
            x_start_all.append(sorted_block[0][0])
            farthest_right_x_all.append(
                sorted_block[-1][0] + sorted_block[-1][2])
            rects += sorted_block

        # rects = sorted(rects, key=lambda x: x[1],reverse=True)

        x_start = min(x_start_all)
        y_start = min(item[1] for item in rects_blocks[0])
        farthest_down_y = max(item[1] + item[3] for item in rects_blocks[-1])
        farthest_right_x = max(farthest_right_x_all)
        # last = rects[-1]


        print(farthest_down_y, "farthest_down_y")
        cv2.rectangle(im, (x_start, y_start),
                      (farthest_right_x, farthest_down_y), (255, 255, 0),
                      3)
        matrix_coordinates = {"x": x_start, "y": y_start,
                              "ln1": farthest_right_x, "ln2": farthest_down_y}
        digits = []
        for rect in rects:
            # Draw the rectangles
            # cv2.rectangle(im, (rect[0], rect[1]),
            #               (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0),
            #               3)
            #

            # Make the rectangular region around the digit
            leng = int(rect[3] * 1.6)
            pt1 = int(rect[1] + rect[3] // 2 - leng // 2)
            pt2 = int(rect[0] + rect[2] // 2 - leng // 2)
            roi = im_th[pt1:pt1 + leng, pt2:pt2 + leng]
            # Resize the image
            roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
            roi = cv2.dilate(roi, (3, 3))
            # Calculate the HOG features
            roi_hog_fd = hog(roi, orientations=9, pixels_per_cell=(14, 14),
                             cells_per_block=(1, 1), visualise=False)
            nbr = clf.predict(np.array([roi_hog_fd], 'float64'))

            digits.append(str(int(nbr[0])))
            cv2.putText(im, str(int(nbr[0])), (rect[0], rect[1]),
                        cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 255), 3)
        #
        # cv2.imshow("Resulting Image with Rectangular ROIs", im)
        #
        # cv2.waitKey()
        return digits, im.tolist()
