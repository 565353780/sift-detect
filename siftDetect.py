import numpy as np
import cv2
from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 10

img1 = cv2.imread('curling_1.jpg')          # queryImage
# img1 = cv2.imread('rocks.jpg')
img2 = cv2.imread('rocks.png') # trainImage

# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(des1,des2,k=2)

# store all the good matches as per Lowe's ratio test.
good = []
scores = []
for m,n in matches:
    if m.distance < 0.7*n.distance:
        good.append(m)
        scores.append(m.distance / n.distance)

# 我添加的用来测试的 

good = np.expand_dims(good, 1)

print('good match num : ', good.size)

min_score_id = -1
min_score = 1
for i in range(len(scores)):
    if scores[i] < min_score:
        min_score = scores[i]
        min_score_id = i

best = [good[min_score_id]]

print('min(m.distance/n.distance) = ', min_score)

img_out = cv2.drawMatchesKnn(img1, kp1, img2, kp2, best, None, flags=2)

img_out = cv2.resize(img_out, (1920, 1080))

cv2.imshow('image', img_out)

cv2.waitKey(0)

# 下面的代码都没有用到

# if len(good)>MIN_MATCH_COUNT:
#     src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
#     dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
#
#     M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
#     matchesMask = mask.ravel().tolist()
#
#     h,w = img1.shape
#     pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
#     dst = cv2.perspectiveTransform(pts,M)
#
#     img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)
#
# else:
#     print ("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
#     matchesMask = None
#
#
#
# draw_params = dict(matchColor = (0,255,0), # draw matches in green color
#         singlePointColor = None,
#         matchesMask = matchesMask, # draw only inliers
#         flags = 2)
#
# img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
#
# plt.imshow(img3, 'gray')
# plt.show()
