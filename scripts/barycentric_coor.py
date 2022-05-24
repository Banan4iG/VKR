#from indexing_of_elements import Index_of_element
from posixpath import split
from random import triangular
from scipy.spatial import Delaunay
from osgeo import gdal
import numpy as np
import cv2
import os
from PIL import Image

class Moved:
    
    #функция инизиализации запускается при создании объекта класса Moved
    def __init__(self, move_layer):
        self.vertex_point_in = "ptI"
        self.vertex_point_out = "ptII"
        self.move_layer = move_layer
        self.type_of_geom = QgsProject.instance().mapLayersByName(move_layer)[0].geometryType()
        self.dict_points200 = {}
        self.dict_points1000 = {}
        self.coordinate_system = QgsProject.instance().crs().authid()

    #функция выполняющая проверку находится ли точка внтутри треугольника
    def is_in_triangle(self, pointXY, triangle):
        pointX = pointXY[0]
        pointY = pointXY[1]
        pointX1 = triangle[0][0]
        pointY1 = triangle[0][1]
        pointX2 = triangle[1][0]
        pointY2 = triangle[1][1]
        pointX3 = triangle[2][0]
        pointY3 = triangle[2][1]
        v1 = ((pointX1 - pointX) * (pointY2 - pointY1)) - ((pointX2 - pointX1)*(pointY1 - pointY))
        v2 = ((pointX2 - pointX) * (pointY3 - pointY2)) - ((pointX3 - pointX2)*(pointY2 - pointY))
        v3 = ((pointX3 - pointX) * (pointY1 - pointY3)) - ((pointX1 - pointX3)*(pointY3 - pointY))
        if (v1 >= 0 and v2 >= 0 and v3 >= 0) or (v1 < 0 and v2 < 0 and v3 < 0):
            return True
        else:
            return False

    def fromSquarToTriangle(self, layer):
        features = layer.getFeatures()
        triangles = []
        for feature in features:
            geom = feature.geometry()
            list_points = geom.asMultiPolygon()
            points = []
            for point in list_points[0][0]:
                pointXY = [point.x(), point.y()]
                points.append(pointXY)
            triangles.append([points[0], points[1], points[3]])
            triangles.append([points[1], points[2], points[3]])
        return triangles

    #функция отрисовки треугольника
    def draw_triangles(self, vertex_point_in, vertex_point_out):
        def toFixed(numObj, digits=0):
            return f"{numObj:.{digits}f}"

        #получения списка базовых точек первой карты 
        list_layers = QgsProject.instance().mapLayersByName(vertex_point_in)
        layer_name = list_layers[0]
        dict_points_in = {}
        point_vertex = []
        point_vertex_wrong = []
        features = layer_name.getFeatures()
        for feature in features:
            geom = feature.geometry()
            list_points = geom.asMultiPoint()
            pointXY = [list_points[0].x(), list_points[0].y()]
            pointXY_wrong = [toFixed(list_points[0].x(), 3), toFixed(list_points[0].y(), 3)]
            s = str(pointXY_wrong[0]), str(pointXY_wrong[1])
            dict_points_in[s] = feature['id']
            point_vertex.append(pointXY)
            point_vertex_wrong.append(pointXY_wrong)
        
        #выполнение треангуляции Делоне
        points = np.array(point_vertex)
        tri = Delaunay(points)
        triangleXY_in = points[tri.simplices]     
        
        points = np.array(point_vertex_wrong)
        tri = Delaunay(points)
        triangleXY_in_wrong = points[tri.simplices]

        #формирование временного списка, состоящий из id точек для соответствия треугольников разных карт 
        triangle_id = []
        for triangle in triangleXY_in_wrong:
            one_triangle_id = [dict_points_in[tuple(triangle[0])],
            dict_points_in[tuple(triangle[1])],
            dict_points_in[tuple(triangle[2])]]
            triangle_id.append(one_triangle_id)

        #получения списка базовых точек второй карты 
        list_layers = QgsProject.instance().mapLayersByName(vertex_point_out)
        layer_name = list_layers[0]
        dict_points_out = {}
        point_vertex = []
        features = layer_name.getFeatures()
        for feature in features:
            geom = feature.geometry()
            list_points = geom.asMultiPoint()
            pointXY = [list_points[0].x(), list_points[0].y()]
            s = str(pointXY[0]), str(pointXY[1])
            dict_points_out[feature['id']] = pointXY
            point_vertex.append(pointXY)
  
        triangleXY = []
        for id in triangle_id:
            triangle = [dict_points_out[id[0]], dict_points_out[id[1]], dict_points_out[id[2]]]
            triangleXY.append(triangle)

        triangleXY_out = np.array(triangleXY)



        # list_net200 = QgsProject.instance().mapLayersByName("net200")
        # net200 = list_net200[0]
        # list_net1000 = QgsProject.instance().mapLayersByName("net1000")
        # net1000 = list_net1000[0]

        # triangleXY_in = self.fromSquarToTriangle(net200)
        # triangleXY_out = self.fromSquarToTriangle(net1000)
        
        #Создание и загрузка в проект векторного слоя с тругольниками первой карты       
        suri = "MultiPolygon?crs=" + self.coordinate_system + "&index=yes"
        tr_name = "triangle" + vertex_point_in
        vl = QgsVectorLayer(suri, tr_name, "memory")
        pr = vl.dataProvider()
        vl.updateExtents()

        fet = QgsFeature()
        for triangl in triangleXY_in:
            fet.setGeometry(QgsGeometry.fromPolygonXY([[QgsPointXY(triangl[0][0], triangl[0][1]), QgsPointXY(triangl[1][0], triangl[1][1]), QgsPointXY(triangl[2][0], triangl[2][1]), QgsPointXY(triangl[0][0], triangl[0][1])]]))
            pr.addFeatures([fet])
            vl.updateExtents()

        vl.updateExtents()
        if not vl.isValid():
            print("Layer failed to load!")
        else:
            QgsProject.instance().addMapLayer(vl)
        
        #Создание и загрузка в проект векторного слоя с тругольниками второй карты 
        suri = "MultiPolygon?crs=" + self.coordinate_system + "&index=yes"
        tr_name = "triangle" + vertex_point_out
        vl = QgsVectorLayer(suri, tr_name, "memory")
        pr = vl.dataProvider()
        vl.updateExtents()

        fet = QgsFeature()
        for triangl in triangleXY_out:
            fet.setGeometry(QgsGeometry.fromPolygonXY([[QgsPointXY(triangl[0][0], triangl[0][1]), QgsPointXY(triangl[1][0], triangl[1][1]), QgsPointXY(triangl[2][0], triangl[2][1]), QgsPointXY(triangl[0][0], triangl[0][1])]]))
            pr.addFeatures([fet])
            vl.updateExtents()

        vl.updateExtents()
        if not vl.isValid():
            print("Layer failed to load!")
        else:
            QgsProject.instance().addMapLayer(vl)
              
        return triangleXY_in, triangleXY_out

    #функция вычисления барицентрических координат точки относительно треугольника
    def barycentric_out(self, pointXY, triangle):
        pointX = pointXY[0]
        pointY = pointXY[1]
        point1X = triangle[0][0]
        point1Y = triangle[0][1]
        point2X = triangle[1][0]
        point2Y = triangle[1][1]
        point3X = triangle[2][0]
        point3Y = triangle[2][1]
        s = ((point2X - point1X)*(point3Y - point1Y) - (point3X - point1X)*(point2Y - point1Y))/2
        s1 = ((point2X - point1X)*(pointY - point1Y) - (pointX - point1X)*(point2Y - point1Y))/2
        s2 = ((pointX - point1X)*(point3Y - point1Y) - (point3X - point1X)*(pointY - point1Y))/2
        s3 = ((point2X - pointX)*(point3Y - pointY) - (point3X - pointX)*(point2Y - pointY))/2
        u = s1/s
        v = s2/s
        w = s3/s
        coor = [u, v, w]
        return coor

    #функция вычисления координат точки относительно ее бариоцентрических координат
    def barycentric_in(self, coor, triangle):
        (u, v, w) = coor
        point1X = triangle[0][0]
        point1Y = triangle[0][1]
        point2X = triangle[1][0]
        point2Y = triangle[1][1]
        point3X = triangle[2][0]
        point3Y = triangle[2][1]
        pointX = u*point3X + v*point2X + w*point1X
        pointY = u*point3Y + v*point2Y + w*point1Y
        pointXY = [pointX, pointY]
        return pointXY
    
    def sift_create(self):
        def get_extent(lname: str) -> dict:
            print(lname)
            extent200 = QgsProject.instance().mapLayersByName(lname)[0].dataProvider().extent()
            return dict(x_min=extent200.xMinimum(), x_max=extent200.xMaximum(), 
                        y_min=extent200.yMinimum(), y_max=extent200.yMaximum())
             
        img_1 = np.array(Image.open("C:/Users/kashi/Documents/Никита/ИС-118/Диплом/VKR/rastr_admline200.tif").convert('L'))
        img_2 = np.array(Image.open("C:/Users/kashi/Documents/Никита/ИС-118/Диплом/VKR/rastr_admline1000.tif").convert('L'))
#        img_1 = np.array(Image.open("E:/Никита/ИС-118/Диплом/VKR/rastr_admline200.tif").convert('L'))
#        img_2 = np.array(Image.open("E:/Никита/ИС-118/Диплом/VKR/rastr_admline1000.tif").convert('L'))
        #img_1 = np.where(img_1==255, 0, 255)

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
        
        extent200 = get_extent("admlin200")
        extent1000 = get_extent("admlin1000")
        cfx_200 = (extent200["x_max"] - extent200["x_min"]) / 1024.0
        cfy_200 = (extent200["y_max"] - extent200["y_min"]) / 1024.0

        cfx_1000 = (extent1000["x_max"] - extent1000["x_min"]) / 1024.0
        cfy_1000 = (extent1000["y_max"] - extent1000["y_min"]) / 1024.0
        
        count = 0
        for match in goodMatch:
            pt1 = psd_kp1[match[0].queryIdx].pt
            pt2 = psd_kp2[match[0].trainIdx].pt
            list_points200.append([count, (extent200["x_min"] + pt1[0]*cfx_200, extent200["y_max"] - pt1[1]*cfy_200)])
            list_points1000.append([count, (extent1000["x_min"]  + pt2[0]*cfx_1000, extent1000["y_max"] - pt2[1]*cfy_1000)])
            count += 1
        list_points200.append([count, (extent200["x_min"], extent200["y_min"])])
        list_points1000.append([count, (extent1000["x_min"], extent1000["y_min"])])
        count += 1
        list_points200.append([count, (extent200["x_min"], extent200["y_max"])])
        list_points1000.append([count, (extent1000["x_min"], extent1000["y_max"])])
        count += 1
        list_points200.append([count, (extent200["x_max"], extent200["y_min"])])
        list_points1000.append([count, (extent1000["x_max"], extent1000["y_min"])])
        count += 1
        list_points200.append([count, (extent200["x_max"], extent200["y_max"])])
        list_points1000.append([count, (extent1000["x_max"], extent1000["y_max"])])  

        suri = "MultiPoint?crs=" + QgsProject.instance().crs().authid() + "&index=yes"
        tr_name = "pt200"
        vl = QgsVectorLayer(suri, tr_name, "memory")
        pr = vl.dataProvider()
        pr.addAttributes([QgsField("id",  QVariant.Int)])
        vl.updateFields()
        vl.updateExtents()
        fet = QgsFeature()
        for pt in list_points200:
            fet.setGeometry(QgsGeometry.fromMultiPointXY([QgsPointXY(pt[1][0], pt[1][1])]))
            fet.setAttributes([pt[0]])
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
        pr.addAttributes([QgsField("id",  QVariant.Int)])
        vl.updateFields()
        vl.updateExtents()
        fet = QgsFeature()
        for pt in list_points1000:
            fet.setGeometry(QgsGeometry.fromMultiPointXY([QgsPointXY(pt[1][0], pt[1][1])]))
            fet.setAttributes([pt[0]])
            pr.addFeatures([fet])
            vl.updateExtents()
            
        vl.updateExtents()
        if not vl.isValid():
            print("Layer failed to load!")
        else:
            QgsProject.instance().addMapLayer(vl)
    
    def split_line(self, points):
        otrs = []
        for i in range(len(points) - 1):
            line = [points[i], points[i+1]]
            xm = (line[0][0] + line[1][0]) / 2
            ym = (line[0][1] + line[1][1]) / 2
            
            xm1 = (line[0][0] + xm) / 2
            ym1 = (line[0][1] + ym) / 2
            
            xm2 = (xm + line[1][0]) / 2
            ym2 = (ym + line[1][1]) / 2
            
            otrs.append(points[i])
            otrs.append([xm1, ym1])
            otrs.append([xm, ym]) 
            otrs.append([xm2, ym2])
        otrs.append(points[-1])
        return otrs
    
    # def split_line(self, points, count = 2):
    #     def dev(pt,ct):
    #         res = []
    #         xm = (pt[0][0] + pt[1][0]) / 2
    #         ym = (pt[0][1] + pt[1][1]) / 2
    #         ct -= 1
    #         if ct > 0: 
    #             res.append(dev( [[pt[0][0], pt[0][1]], [xm, ym] ], count))
    #             res.append([xm, ym]) 
    #             res.append(dev( [[xm, ym], [pt[1][0], pt[1][1]]], count))
    #         else:
    #             res.append([xm, ym])
    #         return res
    #     otrs = []
    #     for i in range(len(points) - 1):
    #         line = [points[i], points[i+1]]
    #         otrs.append(points[i])
    #         otrs += dev(line, count)
    #     otrs.append(points[-1])
    #     return otrs
    
    #основная функция запускаемая пользователем
    
    def run(self):
        project = QgsProject.instance()
        #удаление слоёв
        for layer in project.mapLayers().values():
            if layer.name().startswith("triangle") or layer.name().startswith("moved"): #or layer.name().startswith("pt"):
                project.removeMapLayer(layer.id())
        
        #self.sift_create()
        
        ls_1 = project.mapLayersByName(self.vertex_point_in)
        ls_2 = project.mapLayersByName(self.vertex_point_out)
        ls_3 = project.mapLayersByName(self.move_layer)
                      
        if not ls_1 or not ls_2 or not ls_3:
            print("Указанного слоя с таким именем не существует")
            return
        
        
        #получение списков и отрисовка треугольников
        (triangleXY_in, triangleXY_out) = self.draw_triangles(self.vertex_point_in, self.vertex_point_out)

        #индексация треугольников
        dict_triangleXY_in = {}
        count = 0
        for tr in triangleXY_in:
            dict_triangleXY_in[str(tr)] = count
            count += 1

        dict_triangleXY_out = {}
        count = 0
        for tr in triangleXY_out:
            dict_triangleXY_out[count] = tr
            count += 1

        list_layers = project.mapLayersByName(self.move_layer)
        layer_name = list_layers[0]
        features = layer_name.getFeatures()
        #получение объектов на первой карте и их построение на второй относительно геометрии    
        #тип геометрии: точки
        if self.type_of_geom == 0:
            points = []
            for feature in features:
                geom = feature.geometry()
                attr_list = feature.attributes()
                list_points = geom.asMultiPoint()
                pointXY = [list_points[0].x(), list_points[0].y()]
                points.append(pointXY)
            
            coors = []
            for point in points:
                for triangle in triangleXY_in:
                    if(self.is_in_triangle(point,triangle)):
                        coors.append([dict_triangleXY_in[str(triangle)], self.barycentric_out(point, triangle)])
                        break


            suri = "MultiPoint?crs=" + self.coordinate_system + "&index=yes"
            name = "movedLayer"
            vl = QgsVectorLayer(suri, name, "memory")
            pr = vl.dataProvider()
            vl.updateExtents()
            fet = QgsFeature()

            for coor in coors:
                pointXY = self.barycentric_in(coor[1], dict_triangleXY_out[coor[0]])
                fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(pointXY[0], pointXY[1])))
                pr.addFeatures([fet])
                vl.updateExtents()
        
        #тип геометрии: линии
        if self.type_of_geom == 1:
            feature_XY =[]
            for feature in features:
                points = []
                geom = feature.geometry()
                attr_list = feature.attributes()
                list_points = geom.asMultiPolyline()
                for point in list_points[0]:
                    pointXY = [point.x(), point.y()]
                    points.append(pointXY)
#                feature_XY.append(self.split_line(points))
                feature_XY.append(points)

            #feature_XY_split = self.split_line(feature_XY)
            feature_coors = []
            for points in feature_XY:
                coors = []
                for point in points:
                    for triangle in triangleXY_in:
                        if(self.is_in_triangle(point,triangle)):
                            coors.append([dict_triangleXY_in[str(triangle)], self.barycentric_out(point, triangle)])
                            break
                feature_coors.append(coors)


            suri = "MultiLineString?crs=" + self.coordinate_system + "&index=yes"
            name = "movedLayer"
            vl = QgsVectorLayer(suri, name, "memory")
            pr = vl.dataProvider()
            vl.updateExtents()
            fet = QgsFeature()

            for coors in feature_coors:
                list_pointXY = []
                for coor in coors:
                    pointXY = self.barycentric_in(coor[1], dict_triangleXY_out[coor[0]])
                    list_pointXY.append(QgsPointXY(pointXY[0], pointXY[1]))
                fet.setGeometry(QgsGeometry.fromPolylineXY(list_pointXY))
                pr.addFeatures([fet])
                vl.updateExtents()
        
        #тип геометрии: полигоны
        if self.type_of_geom == 2:
            
            feature_XY =[]
            for feature in features:
                points = []
                geom = feature.geometry()
                attr_list = feature.attributes()
                list_points = geom.asMultiPolygon()
                for point in list_points[0][0]:
                    pointXY = [point.x(), point.y()]
                    points.append(pointXY)
                feature_XY.append(self.split_line(points))
#                feature_XY.append(points)
            
            #feature_XY_split = self.split_line(feature_XY)
            feature_coors = []
            for points in feature_XY:
                coors = []
                for point in points:
                    for triangle in triangleXY_in:
                        if(self.is_in_triangle(point,triangle)):
                            coors.append([dict_triangleXY_in[str(triangle)], self.barycentric_out(point, triangle)])
                            break
                feature_coors.append(coors)


            suri = "MultiPolygon?crs=" + self.coordinate_system + "&index=yes"
            name = "movedLayer"
            vl = QgsVectorLayer(suri, name, "memory")
            pr = vl.dataProvider()
            vl.updateExtents()
            fet = QgsFeature()

            for coors in feature_coors:
                list_pointXY = []
                for coor in coors:
                    pointXY = self.barycentric_in(coor[1], dict_triangleXY_out[coor[0]])
                    list_pointXY.append(QgsPointXY(pointXY[0], pointXY[1]))
                fet.setGeometry(QgsGeometry.fromPolygonXY([list_pointXY]))
                pr.addFeatures([fet])
                vl.updateExtents()
        
        #добавление слоя на карту
        if not vl.isValid():
            print("Layer failed to load!")
        else:
            QgsProject.instance().addMapLayer(vl)

#создание объекта класса Moved: указание имён слоёв с базовыми точками двух карт и переносимых объектов, а также указание типа геометрии
mv = Moved("homeOne")
mv.run()