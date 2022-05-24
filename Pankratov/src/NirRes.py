import math
import cv2

project = QgsProject.instance()
layer = project.mapLayersByName("Nir")[0]
print(layer)
feat = layer.getFeatures()

#нахождение ключевых точек

img1 = cv2.imread('5_set.png') 
img2 = cv2.imread('5_set3.png')

img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
# create SIFT object
sift = cv2.SIFT_create()
# detect SIFT features in both images
keypoints_1, descriptors_1 = sift.detectAndCompute(img1,None)
keypoints_2, descriptors_2 = sift.detectAndCompute(img2,None)
# create feature matcher
bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
# match descriptors of both images
matches = bf.match(descriptors_1,descriptors_2)
# sort matches by distance
matches = sorted(matches, key = lambda x:x.distance)

matchesList = []
idMat = -1
for mat in matches:
    if abs(keypoints_1[mat.queryIdx].response - keypoints_2[mat.trainIdx].response) < 0.00001:
        if(len(matchesList) == 1  and  (abs(keypoints_1[matchesList[0].queryIdx].pt[0] - keypoints_1[mat.queryIdx].pt[0]) > 10) )  :
            continue
        matchesList.append(mat)
        if len(matchesList) == 2 :
            break

pointSwichesVectX1 = keypoints_1[matchesList[0].queryIdx].pt[0]
pointSwichesVectY1 = -keypoints_1[matchesList[0].queryIdx].pt[1]
pointSwichesVectX2 = keypoints_1[matchesList[1].queryIdx].pt[0]
pointSwichesVectY2 = -keypoints_1[matchesList[1].queryIdx].pt[1]

pointSwichesRastX1 = keypoints_2[matchesList[0].trainIdx].pt[0]
pointSwichesRastY1 = -keypoints_2[matchesList[0].trainIdx].pt[1]
pointSwichesRastX2= keypoints_2[matchesList[1].trainIdx].pt[0]
pointSwichesRastY2 = -keypoints_2[matchesList[1].trainIdx].pt[1]

print(pointSwichesVectX1)
print(pointSwichesVectY1)
print(pointSwichesVectX2)
print(pointSwichesVectY2)
print(pointSwichesRastX1)
print(pointSwichesRastY1)
print(pointSwichesRastX2)
print(pointSwichesRastY2)
#

Dx1 = pointSwichesVectX2 - pointSwichesVectX1
Dy1 = pointSwichesVectY2 - pointSwichesVectY1

Dx2 = pointSwichesRastX2 - pointSwichesRastX1
Dy2 = pointSwichesRastY2 - pointSwichesRastY1


angl1 = math.atan2(Dy1,Dx1)
angl2 = math.atan2(Dy2,Dx2)
angl =  -(angl1 - angl2)
print(angl1)
print(angl2)
print(angl)

layer = project.mapLayersByName("Nir")[0]
feat = layer.getFeatures()
suri = "MultiPolygon?crs=epsg:20008&index=yes"
vl = QgsVectorLayer(suri, "Nir1" , "memory")
for feature in feat:
    a = []
    b = []
    for points in feature.geometry().asPolygon()[0]:
        #расстояние от объекта до ключевой точки на векторном изображении
        xRast =  points[0] - pointSwichesVectX1
        yRast =  points[1] - pointSwichesVectY1
        #расстояние от объекта до ключевой точки на растровом изображении
        xNew = pointSwichesRastX1 + xRast
        yNew = pointSwichesRastY1 + yRast
        # поворот координат
        x = ((xNew  - pointSwichesRastX1)* math.cos(angl) - (yNew  - pointSwichesRastY1)* math.sin(angl) + pointSwichesRastX1)
        y = ((xNew  - pointSwichesRastX1)* math.sin(angl) + (yNew  - pointSwichesRastY1)* math.cos(angl) + pointSwichesRastY1)
        b.append(QgsPointXY(x, y))
    b.append(b[0])
    a.append(b)
    i += 1 
    fet = QgsFeature()
    pr = vl.dataProvider()
    vl.updateExtents()
    fet.setGeometry(QgsGeometry.fromPolygonXY(a))
    pr.addFeatures([fet])
    vl.updateExtents()

    if not vl.isValid():
        print("Layer failed to load!")
    else:
        QgsProject.instance().addMapLayer(vl)

    
