import random

class Index_of_element(object):

    def __init__(self):

        self.project = QgsProject.instance()
        self.del_temp_layers()
        self.layers_name = [layer.name() for layer in QgsProject.instance().mapLayers().values()]
        self.list_number_rect = []
        self.numbers_seperation_rects = []

    # Получение эксремумов главного прямоугольника
    def get_points_main_rectangle(self):
        top = QgsPointXY(0,-100)
        left = QgsPointXY(100,0)
        down = QgsPointXY(0,100)
        right = QgsPointXY(-100,0)
        # Цикл по всем слоям
        for current_layer in self.layers_name:
            layer = self.project.mapLayersByName(current_layer)
            features = layer[0].getFeatures()
            for feature in features:
                geom = feature.geometry()
                # Получение типа геометрии
                geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
                if geom.type() == QgsWkbTypes.PointGeometry:
                    if geomSingleType:
                        if(left.x() > geom.asPoint().x()):
                            left = geom.asPoint()
                        if(right.x() < geom.asPoint().x()):
                            right = geom.asPoint()
                        if(top.y() < geom.asPoint().y()):
                            top = geom.asPoint()
                        if(down.y() > geom.asPoint().y()):
                            down = geom.asPoint()
                    else:
                        if(left.x() > geom.asMultiPoint()[0].x()):
                            left = geom.asMultiPoint()[0]
                        if(right.x() < geom.asMultiPoint()[0].x()):
                            right = geom.asMultiPoint()[0]
                        if(top.y() < geom.asMultiPoint()[0].y()):
                            top = geom.asMultiPoint()[0]
                        if(down.y() > geom.asMultiPoint()[0].y()):
                            down = geom.asMultiPoint()[0]
                elif geom.type() == QgsWkbTypes.LineGeometry:
                    if geomSingleType:
                        if(left.x() > geom.asPolyline().x()):
                            left = geom.asPolyline()
                        if(right.x() < geom.asPolyline().x()):
                            right = geom.asPolyline()
                        if(top.y() < geom.asPolyline().y()):
                            top = geom.asPolyline()
                        if(down.y() > geom.asPolyline().y()):
                            down = geom.asPolyline()
                    else:
                        multyPolyLines = geom.asMultiPolyline()[0]
                        for first_point in multyPolyLines:
                            if(left.x() > first_point.x()):
                                left = first_point
                            if(right.x() < first_point.x()):
                                right = first_point
                            if(top.y() < first_point.y()):
                                top = first_point
                            if(down.y() > first_point.y()):
                                down = first_point
                elif geom.type() == QgsWkbTypes.PolygonGeometry:
                    if geomSingleType:
                        poligons = geom.asPolygon()[0][0]
                        for first_point in poligons:
                            if(left.x() > first_point.x()):
                                left = first_point
                            if(right.x() < first_point.x()):
                                right = first_point
                            if(top.y() < first_point.y()):
                                top = first_point
                            if(down.y() > first_point.y()):
                                down = first_point
                    else:
                        poligons = geom.asMultiPolygon()[0][0]
                        for first_point in poligons:
                            if(left.x() > first_point.x()):
                                left = first_point
                            if(right.x() < first_point.x()):
                                right = first_point
                            if(top.y() < first_point.y()):
                                top = first_point
                            if(down.y() > first_point.y()):
                                down = first_point
                else:
                    print("Неизвестный или неверный тип геометрии",current_layer, feature.id())
                
        left_top = QgsPointXY(left.x(), top.y())
        right_top = QgsPointXY(right.x(), top.y())
        right_down = QgsPointXY(right.x(), down.y())
        left_down = QgsPointXY(left.x(), down.y())
        
        return [left_top,right_top, right_down, left_down]


    # Создание временного слоя
    def add_temporary_layer(self):
        vector_layer = QgsVectorLayer("MultiPolygon", "rectangle", "memory")#MultiLineString
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
            vl = QgsVectorLayer("MultiPolygon", "rectangle_" + new_number_rect, "memory")
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
        layers_main_name = []
        for current_layer in [layer.name() for layer in QgsProject.instance().mapLayers().values()]:
            if "rectangle_" in current_layer:
                layers_rect_name.append(current_layer)
            else:
                layers_main_name.append(current_layer)

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


#obj = Index_of_element()
#indexes = obj.run()
#obj.set_color_rects(indexes)
