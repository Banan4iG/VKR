import random

class Index_of_element(object):

    def __init__(self, layers_name):

        self.project = QgsProject.instance()
        self.del_temp_layers()
        self.layers_name = layers_name
        self.layers_name.append("homeOne")
        self.list_number_rect = []
        self.numbers_seperation_rects = []
        self.coordinate_system = self.project.crs().authid()

    # Получение эксремумов главного прямоугольника
    def get_points_main_rectangle(self):
        def get_extent(lname: str) -> dict:
            extent200 = self.project.mapLayersByName(lname)[0].dataProvider().extent()
            return dict(x_min=extent200.xMinimum(), x_max=extent200.xMaximum(), 
                        y_min=extent200.yMinimum(), y_max=extent200.yMaximum())
        
        extent = get_extent("lakeI")
                        
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
            print(obj)
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

    def find_cross(self, indexes):
        class Index:
            def __init__(self, layer_name, id_f, str_indexes):
                self.layer_name = layer_name
                self.id_f = id_f
                list_of_indexes = str_indexes.split(";")
                list_of_indexes.pop()
                self.list_of_indexes = list_of_indexes
        
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

        
        for i in range(len(split_list_of_classes_index) - 1):
            for el1 in split_list_of_classes_index[i]:
                for el2 in split_list_of_classes_index[-1]:
                    c = list(set(el1.list_of_indexes) & set(el2.list_of_indexes))
                    if c:
                        print(el1.list_of_indexes)
                        print(el2.list_of_indexes)
                        print(el1.layer_name, el1.id_f)
                        print(c)
                        print(el2.layer_name, el2.id_f)


obj = Index_of_element(["lakeI"])
indexes = obj.run()
obj.set_color_rects(indexes)
obj.find_cross(indexes)