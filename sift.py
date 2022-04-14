import cv2
import os
import numpy as np
from PIL import Image

img_1 = np.array(Image.open("C:/Users/kashi/Documents/Никита/ИС-118/Диплом/VKR/rastr_admline200.tif").convert('L'))
img_2 = np.array(Image.open("C:/Users/kashi/Documents/Никита/ИС-118/Диплом/VKR/rastr_admline1000.tif").convert('L'))

#img_1 = cv2.imread("E:/Никита/ИС-118/Диплом/VKR/rastr_admline200.png")
#img_2 = cv2.imread("rastr_admline1000.tif")

temp1 = img_1
temp2 = img_2
for i in range(1024):
    for j in range(1024):
        if img_1[i][j] == 255:
            temp1[i][j] = 0
        else:
            temp1[i][j] = 255

for i in range(1024):
    for j in range(1024):
        if img_2[i][j] == 255:
            temp2[i][j] = 0
        else:
            temp2[i][j] = 255

#cv2.imshow('img', temp)

npKernel = np.uint8(np.zeros((5,5)))
for i in range(5):
    npKernel[2][i] = 1
    npKernel[i][2] = 1 

npKernel_eroded1 = cv2.erode(temp1, npKernel)
npKernel_eroded2 = cv2.erode(temp2, npKernel)
#cv2.imshow('img', npKernel_eroded)

#Расчет функции SIFT
sift = cv2.xfeatures2d.SIFT_create()

psd_kp1, psd_des1 = sift.detectAndCompute(npKernel_eroded1, None)
psd_kp2, psd_des2 = sift.detectAndCompute(npKernel_eroded2, None)

# 4) Сопоставление признаков фланна
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)

flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(psd_des1, psd_des2, k=2)
goodMatch = []
for m, n in matches:
    # goodMatch - это отфильтрованная высококачественная пара. 
    #Если расстояние до первого совпадения в двух парах меньше 1/2 расстояния до второго совпадения, это может указывать на то, что первая пара является уникальной и неповторяющейся характерной точкой на двух изображениях. , Можно сохранить.
    if m.distance < 0.50*n.distance:
        goodMatch.append(m)
# Добавить измерение
goodMatch = np.expand_dims(goodMatch, 1)

list_points200 = []
list_points1000 = []
for match in goodMatch:
    pt1 = psd_kp1[match[0].queryIdx].pt
    pt2 = psd_kp2[match[0].trainIdx].pt
    list_points200.append((8429085.18 + pt1[0]*216.8, 6629415.28 - pt1[1]*331.8))
    list_points1000.append((8429085.18 + pt2[0]*216.8, 6629415.28 - pt2[1]*331.8))

suri = "MultiPoint?crs=" + QgsProject.instance().crs().authid() + "&index=yes"
tr_name = "pt200"
vl = QgsVectorLayer(suri, tr_name, "memory")
pr = vl.dataProvider()
vl.updateExtents()
for pt in list_points200:
    fet = QgsFeature()
    fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(pt[0], pt[1])))
    pr.addFeatures([fet])
    vl.updateExtents()
    
vl.updateExtents()
if not vl.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(vl)

suri = "MultiPoint?crs=" + QgsProject.instance().crs().authid() + "&index=yes"
tr_name = "pt1000"
vl = QgsVectorLayer(suri, tr_name, "memory")
pr = vl.dataProvider()
vl.updateExtents()
for pt in list_points1000:
    fet = QgsFeature()
    fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(pt[0], pt[1])))
    pr.addFeatures([fet])
    vl.updateExtents()
    
vl.updateExtents()
if not vl.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(vl)

#img_out = cv2.drawMatchesKnn(npKernel_eroded1, psd_kp1, npKernel_eroded2, psd_kp2, goodMatch, None, flags=2)
#
#cv2.imshow('image', img_out)# Показать картинки
#cv2.waitKey(0)# Дождитесь нажатия кнопки
#cv2.destroyAllWindows()# Очистить все окна