#project = QgsProject.instance()
#layer_name = "protected_areas"
#list_layers = project.mapLayersByName(layer_name)
#my_layer = list_layers[0]
my_layer = iface.activeLayer()
features = my_layer.getFeatures()
for feature in features:
    geom = feature.geometry()
    list_points = geom.asMultiPolyline()
    #print (list_points[0])
    print ("Next object:")
    for point in list_points[0]:
        print("Point: x: ", point.x(),"y: ", point.y(), end='\n')
my_layer.removeSelection()

