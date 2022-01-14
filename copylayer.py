project = QgsProject.instance()
layer_name200 = "points200"
layer_name1000 = "points1000"

list_layers = project.mapLayersByName(layer_name200)
points200_layer = list_layers[0]
list_layers = project.mapLayersByName(layer_name1000)
points1000_layer = list_layers[0]

features = points200_layer.getFeatures()
pr = points1000_layer.dataProvider()

for feature in features:
    pr.addFeatures([feature])
    points1000_layer.updateExtents()
