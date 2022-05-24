from pyexpat import features
import random

class Index_of_element(object):

    def __init__(self, layers_name):

        self.project = QgsProject.instance()
        self.del_temp_layers()
        self.layers_name = layers_name
        self.layers_name.append("movedLayer")
        self.list_number_rect = []
        self.numbers_seperation_rects = []
        self.coordinate_system = self.project.crs().authid()

    # Получение эксремумов главного прямоугольника
    def get_points_main_rectangle(self):
        def get_extent(lname: str) -> dict:
            extent200 = self.project.mapLayersByName(lname)[0].dataProvider().extent()
            return dict(x_min=extent200.xMinimum(), x_max=extent200.xMaximum(), 
                        y_min=extent200.yMinimum(), y_max=extent200.yMaximum())
        
        extent = get_extent("lakeII")
                        
        left_top = QgsPointXY(extent["x_min"], extent["y_max"])
        right_top = QgsPointXY(extent["x_max"], extent["y_max"])
        right_down = QgsPointXY(extent["x_max"], extent["y_min"])
        left_down = QgsPointXY(extent["x_min"], extent["y_min"])
        
        return [left_top,right_top, right_down, left_down]


    # Создание временного слоя
    def add_temporary_layer(self):
        suri = "MultiPolygon?crs=" + self.coordinate_system + "&index=yes"
        vector_layer = QgsVectorLayer(suri, "rectangle", "memory")#MultiLineString
        pr = vector_layer.dataProvider()
        #vector_layer.setStyleSheet("background: black;")
        vector_layer.updateExtents()

        # Добавление объекта (прямоугольника) на векторнй слой
        triangleXY = self.get_points_main_rectangle()
        fet = QgsFeature()
        fet.setGeometry(QgsGeometry.fromPolygonXY([[#fromPolylineXY
        triangleXY[0],
        triangleXY[1],
        triangleXY[2],
        triangleXY[3],
        triangleXY[0]]]))
        pr.addFeatures([fet])

        # Присваиваем чёрный цвет
        properties = {'color': 'white', 'outline_color': 'black'}
        symbol = QgsFillSymbol.createSimple(properties)
        renderer = QgsSingleSymbolRenderer(symbol)
        vector_layer.setRenderer(renderer)

        vector_layer.updateExtents()
        if not vector_layer.isValid():
            print("Layer failed to load!")
        else:
            QgsProject.instance().addMapLayer(vector_layer)
        
        return "rectangle"


    # Получение всех обектов внутри прямоугольника
    def separation_on_rect(self, name_layer):
        #Получение слоя по имени
        vecotr_layer = self.project.mapLayersByName(name_layer)[0]
        features = vecotr_layer.getFeatures()

        # Получение геометрии
        for feature in features:
            rect_points = feature.geometry().asPolygon()[0]

        # Деление на 4 прямоугольника
        for i in range (1, 5):
            #number_rect += 1
            if( "_" in name_layer):
                new_number_rect = name_layer.split("_")[1] + "." + str(i)
            else:
                new_number_rect = str(i)
            suri = "MultiPolygon?crs=" + self.coordinate_system + "&index=yes"
            vl = QgsVectorLayer(suri, "rectangle_" + new_number_rect, "memory")
            if(len(new_number_rect.split(".")) < 15):
                self.list_number_rect.append(new_number_rect)
            pr = vl.dataProvider()
            vl.updateExtents()

            fet = QgsFeature()
            if(i==1):
                fet.setGeometry(QgsGeometry.fromPolygonXY([[
                rect_points[0],
                QgsPointXY((rect_points[1][0]-rect_points[0][0])/2+rect_points[0][0],rect_points[1][1]),
                QgsPointXY((rect_points[1][0]-rect_points[0][0])/2+rect_points[0][0], (rect_points[1][1]-rect_points[2][1])/2 + rect_points[2][1]),
                QgsPointXY(rect_points[3][0],(rect_points[0][1]-rect_points[3][1])/2 + rect_points[3][1]),
                rect_points[0]]]))
                pr.addFeatures([fet])

            elif(i==2):
                fet.setGeometry(QgsGeometry.fromPolygonXY([[
                QgsPointXY((rect_points[1][0]-rect_points[0][0])/2+rect_points[0][0],rect_points[1][1]),
                rect_points[1],
                QgsPointXY(rect_points[2][0],(rect_points[1][1]-rect_points[2][1])/2 + rect_points[2][1]),
                QgsPointXY((rect_points[1][0]-rect_points[0][0])/2+rect_points[0][0], (rect_points[1][1]-rect_points[2][1])/2 + rect_points[2][1]),
                QgsPointXY((rect_points[1][0]-rect_points[0][0])/2+rect_points[0][0],rect_points[1][1])]]))
                pr.addFeatures([fet])

            elif(i==3):
                fet.setGeometry(QgsGeometry.fromPolygonXY([[
                QgsPointXY((rect_points[1][0]-rect_points[0][0])/2+rect_points[0][0], (rect_points[1][1]-rect_points[2][1])/2 + rect_points[2][1]),
                QgsPointXY(rect_points[2][0],(rect_points[1][1]-rect_points[2][1])/2 + rect_points[2][1]),
                rect_points[2],
                QgsPointXY((rect_points[2][0]-rect_points[3][0])/2+rect_points[3][0],rect_points[2][1]),
                QgsPointXY((rect_points[1][0]-rect_points[0][0])/2+rect_points[0][0], (rect_points[1][1]-rect_points[2][1])/2 + rect_points[2][1])]]))
                pr.addFeatures([fet])

            elif(i==4):
                fet.setGeometry(QgsGeometry.fromPolygonXY([[
                QgsPointXY(rect_points[3][0],(rect_points[0][1]-rect_points[3][1])/2 + rect_points[3][1]),
                QgsPointXY((rect_points[1][0]-rect_points[0][0])/2+rect_points[0][0], (rect_points[1][1]-rect_points[2][1])/2 + rect_points[2][1]),
                QgsPointXY((rect_points[2][0]-rect_points[3][0])/2+rect_points[3][0],rect_points[2][1]),
                rect_points[3],
                QgsPointXY(rect_points[3][0],(rect_points[0][1]-rect_points[3][1])/2 + rect_points[3][1])]]))
                pr.addFeatures([fet])

            # Присваиваем чёрный цвет
            properties = {'color': 'white', 'outline_color': 'black'}
            symbol = QgsFillSymbol.createSimple(properties)
            renderer = QgsSingleSymbolRenderer(symbol)
            vl.setRenderer(renderer)

            vl.updateExtents()
            if not vl.isValid():
                print("Layer failed to load!")
            else:
                QgsProject.instance().addMapLayer(vl)

        # Удаление разделённого вектора
        self.project.removeMapLayer(vecotr_layer.id())   


    # Рекурсия на разделение по прямоугольникам                  
    def separation(self):
        # Получение названий всех прямоугольников
        current_rects = []
        for number in self.list_number_rect:
            current_rects.append("rectangle_" + number)
        for rect in current_rects:
            vecotr_layer = self.project.mapLayersByName(rect)[0]
            features = vecotr_layer.getFeatures()
            # Получение геометрии прямоугольника
            for feature in features:
                rectangle = feature.geometry()

            # Находим количество пересечений со всеми объектами слоя в текущем прямоугольнике
            list_intersects = []
            count_intersects = 0
            inner_intersects = True
            for current_layer in self.layers_name:
                layer = self.project.mapLayersByName(current_layer)[0]
                feats = layer.getFeatures()
                for feature in feats:
                    # Проверка на наличии объектов в прямоугольнике
                    if (rectangle.intersects(feature.geometry())): 
                        count_intersects += 1
                        list_intersects.append(feature.geometry())
                        #list_not_intersects.append(feature.geometry())

            # Обнуление точек пересечения если есть непересекающийся объект
            inner_intersects = self.zero_count_inner_intersects(list_intersects)

            # Заполнение списка прямоугольников с пересечениями
            if (count_intersects > 1 and inner_intersects == True):
                self.numbers_seperation_rects.append(rect.split('_')[1])
                self.numbers_seperation_rects = list(set(self.numbers_seperation_rects))

            if (count_intersects > 1 and inner_intersects == False):
                # Делим прямоугольник на 4
                self.separation_on_rect(rect)
                self.list_number_rect.remove(rect.split("_")[1])
                return self.separation()


    # Получение итогового списка индексом элемента
    def fill_index(self):
        total_list = []
        layers_rect_name = []
        layers_main_name = self.layers_name 
        for current_layer in [layer.name() for layer in QgsProject.instance().mapLayers().values()]:
            if "rectangle_" in current_layer:
                layers_rect_name.append(current_layer)

        for current_layer in layers_main_name:
            feats = self.project.mapLayersByName(current_layer)[0].getFeatures()
            for feat in feats:
                str_feature = ""
                str_index = ""
                for current_rect in layers_rect_name:
                    feats_rect = self.project.mapLayersByName(current_rect)[0].getFeatures()
                    for feat_rect in feats_rect:
                        if(feat.geometry().intersects(feat_rect.geometry())):
                                str_index += current_rect.split("_")[1] + ";"

                str_feature = current_layer + "_" + str(feat.id()) + "_" + str_index
                total_list.append(str_feature)

        print(total_list)
        return total_list


    # Обнуление точек пересечения если есть непересекающийся объект
    def zero_count_inner_intersects(self, list_intersects):
        for geom_in in list_intersects:
            for geom_out in list_intersects:
                if (geom_in != geom_out):
                    if not(geom_in.intersects(geom_out)):
                        return False
        return True


    # Установка цвета прямоугольнико для каждого объекта
    def set_color_rects(self, list_indexs):
        for obj in list_indexs:
            name_layer = obj.split("_")[0]
            id_feature = obj.split("_")[1]
            list_number_rects = obj.split("_")[2]

            vecotr_layer = self.project.mapLayersByName(name_layer)[0]

            for feat in vecotr_layer.getFeatures():
                if feat.id() == int(id_feature):
                    list_number_rects =  list_number_rects.split(";")
                    # Присваиваем цвет каждому объекту
                    r = str(random.randint(0, 255))
                    g = str(random.randint(0, 255))
                    b = str(random.randint(0, 255))
                    properties = {'color': r+','+g+','+b ,'outline_color': 'black'}
                    for number in list_number_rects:
                        if number != "" :
                            current_rect = "rectangle_" + number
                            rect_layer = self.project.mapLayersByName(current_rect)[0]
                            # Присвоение цвета
                            symbol = QgsFillSymbol.createSimple(properties)
                            renderer = QgsSingleSymbolRenderer(symbol)
                            rect_layer.setRenderer(renderer)
                    break

        # Присваиваем серый цвет у пересекающихся прямоугольников
        for number in self.numbers_seperation_rects:
            vecotr_layer = self.project.mapLayersByName('rectangle_' + number)[0]

            properties = {'color': '190, 190, 190', 'outline_color': 'black'}
            symbol = QgsFillSymbol.createSimple(properties)
            renderer = QgsSingleSymbolRenderer(symbol)
            vecotr_layer.setRenderer(renderer)


    # Запуска скрипта
    def run(self):
        # Загрузка первого слоя и его разделение
        self.separation_on_rect(self.add_temporary_layer())
        # Рекурсия распределения прямоугольников 
        self.separation()
        # Получение списка
        list_index = self.fill_index()
        return  list_index


    # Удаление временных слоёв
    def del_temp_layers(self):
        layers_name = [layer.name() for layer in QgsProject.instance().mapLayers().values()]
        for current_layer in layers_name:
            if "rectangle" in current_layer:
                layer = self.project.mapLayersByName(current_layer)[0]
                self.project.removeMapLayer(layer.id())

    def fix_cross(self, indexes):
        class Index:
            def __init__(self, layer_name, id_f, str_indexes):
                self.layer_name = layer_name
                self.id_f = id_f
                list_of_indexes = str_indexes.split(";")
                list_of_indexes.pop()
                self.list_of_indexes = list_of_indexes
        
        def cross_point(line1, line2):
            x1 = line1[0].x()
            y1 = line1[0].y()
            x2 = line1[1].x()
            y2 = line1[1].y()
            x3 = line2[0].x()
            y3 = line2[0].y()
            x4 = line2[1].x()
            y4 = line2[1].y()
            k1 = (y1 - y2) / (x1 - x2)
            b1 = (x2 * y1 - x1 * y2) / (x2 - x1)
            k2 = (y3 - y4) / (x3 - x4)
            b2 = (x4 * y3 - x3 * y4) / (x4 - x3)
            if k1 != k2:
                x = (b2 - b1) / (k1 - k2)
                y = (k2 * b1 - k1 * b2) / (k2 - k1)
                if (min(x1, x2) <= x <= max(x1, x2)) and (min(x3, x4) <= x <= max(x3, x4)) and (min(y1, y2) <= y <= max(y1, y2)) and (min(y3, y4) <= y <= max(y3, y4)):
                    cross_point = QgsPointXY(x,y)
                else:
                    cross_point = 0
            else:
                cross_point = 0
            return cross_point

        def split_line(line):
            x1 = line[0].x()
            y1 = line[0].y()
            x2 = line[1].x()
            y2 = line[1].y()
            xm = (x1 + x2) / 2.0
            ym = (y1 + y2) / 2.0
            return QgsPointXY(xm, ym)

        def is_in_obj(point, obj):
            pol_str = ""
            for el in obj:
                pol_str += str(el.x()) + ' ' + str(el.y()) + ','
            pl_str = 'Polygon((' + pol_str[:-1] + '))'
            polygon_geometry = QgsGeometry.fromWkt(pl_str)
            point_geometry = QgsGeometry.fromWkt('Point ((' + str(point.x()) + ' ' + str(point.y()) + '))')
            polygon_geometry_engine = QgsGeometry.createGeometryEngine(polygon_geometry.constGet())
            polygon_geometry_engine.prepareGeometry()
            if polygon_geometry_engine.intersects(point_geometry.constGet()):
                return True
            else:
                return False
        
        def e_distance(pt1, pt2):
            x1 = pt1.x()
            y1 = pt1.y()
            x2 = pt2.x()
            y2 = pt2.y()
            distance = ((x2 - x1)**2 + (y2 - y1)**2)**(1/2)
            return distance

        def move_pt(centr, list_pt_for_mv):
            list_pt_mvd = []        
            for pt in list_pt_for_mv:
                x_new = (2.0 * pt.x()) - centr.x()
                y_new = (2.0 * pt.y()) - centr.y()
                list_pt_mvd.append(QgsPointXY(x_new, y_new))
            return list_pt_mvd
        
        list_of_classes_index = []
        for index in indexes:
            data = index.split("_")
            list_of_classes_index.append(Index(data[0], data[1], data[2]))
        
        split_list_of_classes_index = []
        for layer_name in self.layers_name:
            list_indexes = []
            for index in list_of_classes_index:
                if index.layer_name == layer_name:
                    list_indexes.append(index)
            split_list_of_classes_index.append(list_indexes)

        
        list_crossing_object = []
        for i in range(len(split_list_of_classes_index) - 1):
            for el1 in split_list_of_classes_index[i]:
                for el2 in split_list_of_classes_index[-1]:
                    cross = list(set(el1.list_of_indexes) & set(el2.list_of_indexes))
                    if cross:
                        list_crossing_object.append((el1, el2))
        
        list_cross_point = []

        for (el1, el2) in list_crossing_object:
            layer1_name = self.project.mapLayersByName(el1.layer_name)[0]
            layer2_name = self.project.mapLayersByName(el2.layer_name)[0]
            feature1 = layer1_name.getFeature(int(el1.id_f))
            feature2 = layer2_name.getFeature(int(el2.id_f))
            list_pt_with_i = []
            list_points1 = feature1.geometry().asMultiPolygon()[0][0]
            list_points2 = feature2.geometry().asPolygon()[0]
            centr = feature2.geometry().centroid().asPoint()
            for i in range(len(list_points1) - 1):
                line1 = (list_points1[i], list_points1[i + 1])
                for j in range(len(list_points2) - 1):
                    line2 = (list_points2[j], list_points2[j + 1])
                    cross_pt = cross_point(line1, line2)
                    if cross_pt != 0:
                        moved_pt = split_line((line1[0],cross_pt))
                        if is_in_obj(moved_pt, list_points2):
                            moved_pt = split_line((cross_pt, line1[1]))
                        list_pt_with_i.append((i, moved_pt))
            
            list_pt_in_big_obj = []
            for pt in list_points2:
                if is_in_obj(pt, list_points1):
                    list_pt_in_big_obj.append(pt)
            
            min_el = min(list_pt_with_i, key=lambda x: x[0])[1]
            min_id = min(list_pt_with_i, key=lambda x: x[0])[0]
            max_el = max(list_pt_with_i, key=lambda x: x[0])[1]
            max_id = max(list_pt_with_i, key=lambda x: x[0])[0] + 1
            curent_pt = min_el
            list_pr_right_pos = []
            while(list_pt_in_big_obj):
                list_d = []
                for pt in list_pt_in_big_obj:
                    distance = e_distance(curent_pt, pt)
                    list_d.append(distance)
                min_d = min(list_d)
                min_i = list_d.index(min_d)
                curent_pt = list_pt_in_big_obj[min_i]
                list_pr_right_pos.append(curent_pt)
                list_pt_in_big_obj.pop(min_i)


            list_pt_mvd = move_pt(centr, list_pr_right_pos)

            l1 = list_points1[:min_id+1]
            l2 = list_points1[max_id:len(list_points1)]
            new_list_for_geom = l1 + [min_el] + list_pt_mvd + [max_el] + l2
            
            geom = QgsGeometry.fromPolygonXY([new_list_for_geom])
            layer1_name.dataProvider().changeGeometryValues({ int(el1.id_f) : geom })
            layer1_name.updateExtents()


            # suri = "MultiPoint?crs=" + self.coordinate_system + "&index=yes"
            # tr_name = "prprpr"
            # vl = QgsVectorLayer(suri, tr_name, "memory")
            # pr = vl.dataProvider()
            # vl.updateExtents()
            # fet = QgsFeature()
            # for pt in list_pt_mvd:
            #     fet.setGeometry(QgsGeometry.fromPointXY(pt))
            #     pr.addFeatures([fet])
            #     vl.updateExtents()

            # vl.updateExtents()
            # if not vl.isValid():
            #     print("Layer failed to load!")
            # else:
            #     QgsProject.instance().addMapLayer(vl)


obj = Index_of_element(["lakeII"])
indexes = obj.run()
obj.set_color_rects(indexes)
obj.fix_cross(indexes)