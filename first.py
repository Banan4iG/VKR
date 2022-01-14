from scipy.spatial import Delaunay
import numpy as np

#project = QgsProject.instance()
#layer_name = "protected_areas"
#list_layers = project.mapLayersByName(layer_name)
#my_layer = list_layers[0]
point_array = []
my_layer = iface.activeLayer()
features = my_layer.getFeatures()
for feature in features:
    geom = feature.geometry()
    list_points = geom.asMultiPoint()
    pointXY = [list_points[0].x(), list_points[0].y()]
    point_array.append(pointXY)
    #print ("Point: x: ", list_points[0].x(),"y: ", list_points[0].y())
    #print ("Next object:")
    #for point in list_points[0]:
        #print("Point x: ", point)
        #print("Point: x: ", point.x(),"y: ", point.y(), end='\n')
my_layer.removeSelection()

points = np.array(point_array)
tri = Delaunay(points)
print(points[tri.simplices][0])



#areaOfInterest = QgsRectangle(450290,400520, 450750,400780)
#QgsTriangle(QgsPoint,QgsPoint,QgsPoint)
#request = QgsFeatureRequest().setFilterRect(areaOfInterest)
#
#for feature in layer.getFeatures(request):
#     do whatever you need with the feature
#    pass


