import cv2
import numpy as np

project = QgsProject.instance()
#Получить список соответствующих зарегистрированных слоев по имени слоя.
#layer = project.mapLayersByName("treangle1")[0]
layer = project.mapLayersByName("test5")[0]
print(layer)
feat = layer.getFeatures()

#загрузка фото
img = cv2.imread('D:/QGIS/tiles/5_contr.png')
#COLOR_BGR2GRAY преобразование между RGB / BGR и оттенками серого, преобразование цветов
imagegray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
sourceColor = np.array(imagegray)[:-15,:]
layers = cv2.split(sourceColor)
imgnp = layers[0]

#Применяет адаптивный порог к массиву.

#cv2.THRESH_BINARY_INV Функция преобразует изображение в оттенках серого в двоичное изображение
_,imgnp = cv2.threshold(imgnp, 238, 255, cv2.THRESH_BINARY_INV)
#медианное значение
imgnp_med = cv2.medianBlur(imgnp, 3)
#Находит контуры в двоичном изображении.

#Функция извлекает контуры из двоичного изображения
contours, _ = cv2.findContours(imgnp_med, cv2.RETR_LIST, cv2.LINE_4)

#точки растра
#Создание списка геометрии, списка удаленных объектов и точек растра
listGeom = []
removeList = []
pointRastr = []

i=0
j=0
for count in contours:
    if (i < (len(contours) - 1)):
        i+=1
#        Создание объект
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
            pointRastr.append(b)
        else:
            checkGeom = 0
            for geomF in listGeom:
                if not geomF.equals(fet.geometry()):
                    if (geomF.area() <= fet.geometry().area()):
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
                pointRastr.append(b)
            elif checkGeom == 2:
                listGeom.append(fet.geometry())
                pointRastr.append(b)
            elif checkGeom == 3:
                continue

# Удаление индексов    
delite = []
for geom in removeList:
    if geom in listGeom:
        index = listGeom.index(geom)
        delite.append(pointRastr[index])
#Удаление объектов
for delitePoint in delite:
    if delitePoint in pointRastr:
        pointRastr.remove(delitePoint)

#сравнение
i = 0
j = 0
indexList = []
tempRastRast = list(pointRastr)

print(pointRastr[0])
for feature in feat:
    i += 1
    j = 0
    for points in tempRastRast:
        j += 1
        count = 0
        tempRastRastObj = list(points)
        savePoint = []
#        for rastVecObjPoint in feature.geometry().asPolygon()[0]:
        for rastVecObjPoint in feature.geometry().asMultiPolygon()[0][0]:
            for rastRastObjPoint in tempRastRastObj:
                if (abs(rastVecObjPoint[0] - rastRastObjPoint[0]) >= 0 and abs(rastVecObjPoint[0] - rastRastObjPoint[0]) < 10) and (abs(rastVecObjPoint[1] - rastRastObjPoint[1]) >= 0 and abs(rastVecObjPoint[1] - rastRastObjPoint[1]) < 20): 
                    count += 1
                    tempRastRastObj.remove(rastRastObjPoint)
                    savePoint.append(rastRastObjPoint)
                    break
#        Равно ли длина найденных точек количество точек векторного объекта
#        if(count >= (len(feature.geometry().asPolygon()[0]))):
        if(count >= (len(feature.geometry().asMultiPolygon()[0][0]))):
            indexList.append(pointRastr.index(points))
            tempRastRast.remove(points)
            break
        else:
            for point in savePoint:
                tempRastRastObj.append(point)

# Отрисовка недостоющих объектов
suri = "MultiPolygon?crs=epsg:20008&index=yes"
layer = QgsVectorLayer(suri, "treangle", "memory")
i = 0
for geomF in pointRastr:
    if i not in indexList:
        a = []
        fet = QgsFeature()
        a.append(geomF)
        fet.setGeometry(QgsGeometry.fromPolygonXY(a))
        pr = layer.dataProvider()
        layer.updateExtents()
        pr.addFeatures([fet])
        layer.updateExtents()

    i += 1
    
QgsProject.instance().addMapLayer(layer)
