import cv2
import numpy as np

img = cv2.imread('C:/Users/kashi/Desktop/img/0_contr.png')
#разделяем изображение на 3 канала
layers = cv2.split(img)
imgnp = layers[1]


#преобразуем все пиксели изображения яркость которых выше 238 в 0, остальные в значение яркости 255
_,imgnp = cv2.threshold(imgnp, 238, 255, cv2.THRESH_BINARY_INV)


imgnp_med = cv2.medianBlur(imgnp, 3)
#imgnp = cv2.bitwise_and(imgnp_med, imgnp)

contours, _ = cv2.findContours(imgnp_med, cv2.RETR_LIST, cv2.LINE_4)



listGeom = []
i = 0
j = 0
suri = "MultiPolygon?crs=EPSG:32638&index=yes"
vl = QgsVectorLayer(suri, "treangle0", "memory")
removeList = []
for count in contours:
    if (i < (len(contours) - 1)):
        i+=1
        fet = QgsFeature()
        epsilon = 0.0001 * cv2.arcLength(count, True)
        approximations = cv2.approxPolyDP(count, epsilon, True)
        a = []
        b = []
        for point in approximations:
            b.append(QgsPointXY(point[0][0], -point[0][1]))
        b.append(QgsPointXY(approximations[0][0][0],-approximations[0][0][1]))
        a.append(b)
        fet.setGeometry(QgsGeometry.fromPolygonXY(a))
        if ( j == 0):
            j+=1
            listGeom.append(fet.geometry())
        else:
            checkGeom = 0
            for geomF in listGeom:
                if not geomF.equals(fet.geometry()):
                    if (geomF.area() <= fet.geometry().area()):
                        '''
                        if geomF.within(fet.geometry()):
                            checkGeom = 1
                            removeList.append(geomF)
                            continue
                        else:
                            checkGeom = 2
                            continue
                            '''
                        countPoints = 0
                        for point in geomF.asPolygon()[0]:
                            if fet.geometry().contains(point):
                               countPoints += 1
                        if countPoints == len(geomF.asPolygon()[0]):
                            checkGeom = 1
                            removeList.append(geomF)
                            continue
                        else:
                            checkGeom = 2
                            continue    
                    else:
                        '''
                        if fet.geometry().within(geomF):
                            checkGeom = 3
                            break
                        else:
                            checkGeom = 2
                            continue
                            '''
                        countPoints = 0
                        for point in fet.geometry().asPolygon()[0]:
                            if geomF.contains(point):
                                countPoints += 1
                        if countPoints == len(fet.geometry().asPolygon()[0]): 
                            checkGeom = 3
                            break
                        else:
                            checkGeom = 2
                            continue
            if checkGeom == 1:
                listGeom.append(fet.geometry())
            elif checkGeom == 2:
                listGeom.append(fet.geometry())
            elif checkGeom == 3:
                continue
               

    
for geom in removeList:
    if geom in listGeom:
        listGeom.remove(geom)


suri = "MultiPolygon?crs=EPSG:32638&index=yes"
vl = QgsVectorLayer(suri, "Nir" , "memory")
for geomF in listGeom:
    fet = QgsFeature()
    pr = vl.dataProvider()
    vl.updateExtents()
    fet.setGeometry(geomF)
    pr.addFeatures([fet])
    vl.updateExtents()

    if not vl.isValid():
        print("Layer failed to load!")
    else:
        QgsProject.instance().addMapLayer(vl)
