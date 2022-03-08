from scipy.spatial import Delaunay
import numpy as np

project = QgsProject.instance()

#layer_name = "treangle"
#list_layers = project.mapLayersByName(layer_name)
#if list_layers:
#    treangle_layer = list_layers[0]
#    project.removeMapLayer(treangle_layer.id())

layer_name = "points_b2"
list_layers = project.mapLayersByName(layer_name)
pointsb_layer = list_layers[0]

point_array = []
point_not_vertex = []
features = pointsb_layer.getFeatures()
for feature in features:
    geom = feature.geometry()
    attr_list = feature.attributes()
    print(attr_list)
    list_points = geom.asPoint()
    pointXY = [list_points.x(), list_points.y()]
    point_array.append(pointXY)

points = np.array(point_array)
tri = Delaunay(points)
triangleXY = points[tri.simplices]

# create layer
suri = "MultiPolygon?crs=epsg:4326&index=yes"
vl = QgsVectorLayer(suri, "treangle", "memory")
pr = vl.dataProvider()
vl.updateExtents()

# add a feature
fet = QgsFeature()
for triangl in triangleXY:
    fet.setGeometry(QgsGeometry.fromPolygonXY([[QgsPointXY(triangl[0][0], triangl[0][1]), QgsPointXY(triangl[1][0], triangl[1][1]), QgsPointXY(triangl[2][0], triangl[2][1]), QgsPointXY(triangl[0][0], triangl[0][1])]]))
    pr.addFeatures([fet])
    vl.updateExtents()

vl.updateExtents()
if not vl.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(vl)