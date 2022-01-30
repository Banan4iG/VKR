from scipy.spatial import Delaunay
import numpy as np

def barycentric_out(pointXY, triangle):
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


def barycentric_in(coor, triangle):
    u = coor[0]
    v = coor[1]
    w = coor[2]
    point1X = triangle[0][0]
    point1Y = triangle[0][1]
    point2X = triangle[1][0]
    point2Y = triangle[1][1]
    point3X = triangle[2][0]
    point3Y = triangle[2][1]
    pointX = u*point1X + v*point2X + w*point3X
    pointY = u*point1Y + v*point2Y + w*point3Y
    pointXY = [pointX, pointY]
    return pointXY

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
triangleXY = points[tri.simplices]

## create layer
#vl = QgsVectorLayer("MultiPolygon", "treangle", "memory")
#pr = vl.dataProvider()
#
## add a feature
#fet = QgsFeature()
#for triangl in triangleXY:
#    fet.setGeometry(QgsGeometry.fromPolygonXY([[QgsPointXY(triangl[0][0], triangl[0][1]), QgsPointXY(triangl[1][0], triangl[1][1]), QgsPointXY(triangl[2][0], triangl[2][1]), QgsPointXY(triangl[0][0], triangl[0][1])]]))
#    pr.addFeatures([fet])
#
## update layer's extent when new features have been added
## because change of extent in provider is not propagated to the layer
#vl.updateExtents()
#
#print("fields:", len(pr.fields()))
#print("features:", pr.featureCount())
#e = vl.extent()
#print("extent:", e.xMinimum(), e.yMinimum(), e.xMaximum(), e.yMaximum())
#
## iterate over features
#features = vl.getFeatures()
#for fet in features:
#    print("F:", fet.id(), fet.attributes(), fet.geometry().asPolygon())


crs = QgsProject.instance().crs()
transform_context = QgsProject.instance().transformContext()
save_options = QgsVectorFileWriter.SaveVectorOptions()
save_options.driverName = "ESRI Shapefile"
save_options.fileEncoding = "windows-1251"

fields = QgsFields()
writer = QgsVectorFileWriter.create(
"E:\Никита\ИС-118\Диплом\VKR\\triangle.shp",
fields,
QgsWkbTypes.MultiPolygon,
crs,
transform_context,
save_options
)

if writer.hasError() != QgsVectorFileWriter.NoError:
    print("Error when creating shapefile: ",  writer.errorMessage())

fet = QgsFeature()
for triangl in triangleXY:
    fet.setGeometry(QgsGeometry.fromPolygonXY([[QgsPointXY(triangl[0][0], triangl[0][1]), QgsPointXY(triangl[1][0], triangl[1][1]), QgsPointXY(triangl[2][0], triangl[2][1]), QgsPointXY(triangl[0][0], triangl[0][1])]]))
    writer.addFeature(fet)

del writer

path = "E:\Никита\ИС-118\Диплом\VKR\\triangle.shp"
vlayer = QgsVectorLayer(path, "triangle", "ogr")
if not vlayer.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(vlayer)

#areaOfInterest = QgsRectangle(450290,400520, 450750,400780)
#QgsTriangle(QgsPoint,QgsPoint,QgsPoint)
#request = QgsFeatureRequest().setFilterRect(areaOfInterest)
#
#for feature in layer.getFeatures(request):
#     do whatever you need with the feature
#    pass
