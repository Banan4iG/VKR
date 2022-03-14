from scipy.spatial import Delaunay
import numpy as np


def is_in_triangle(pointXY, triangle):
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
    
def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

def draw_triangle(vertex_points_layer_name):
    list_layers = project.mapLayersByName(vertex_points_layer_name)
    layer_name = list_layers[0]

    point_vertex = []
    features = layer_name.getFeatures()
    for feature in features:
        geom = feature.geometry()
        attr_list = feature.attributes()
        list_points = geom.asMultiPoint()
        pointXY = [list_points[0].x(), list_points[0].y()]
        point_vertex.append(pointXY)
    
    points = np.array(point_vertex)
    tri = Delaunay(points)
    triangleXY = points[tri.simplices]

    suri = "MultiPolygon?crs=epsg:20008&index=yes"
    tr_name = "triangle" + vertex_points_layer_name
    vl = QgsVectorLayer(suri, tr_name, "memory")
    pr = vl.dataProvider()
    vl.updateExtents()

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
    
    return triangleXY

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


project = QgsProject.instance()

layer_name = "trianglepoints200"
list_layers = project.mapLayersByName(layer_name)
if list_layers:
    treangle_layer = list_layers[0]
    project.removeMapLayer(treangle_layer.id())

layer_name = "moved_point"
list_layers = project.mapLayersByName(layer_name)
if list_layers:
    treangle_layer = list_layers[0]
    project.removeMapLayer(treangle_layer.id())

layer_name = "trianglepoints1000"
list_layers = project.mapLayersByName(layer_name)
if list_layers:
    treangle_layer = list_layers[0]
    project.removeMapLayer(treangle_layer.id())

layer_name_200 = "points200"
layer_name_1000 = "points1000"

triangleXY_200 = draw_triangle(layer_name_200)
triangleXY_1000 = draw_triangle(layer_name_1000)

dict_triangleXY_200 = {}
count = 0
for tr in triangleXY_200:
    print(list(tr))
#    dict_triangleXY_200[list(tr)] = count
    count += 1

dict_triangleXY_1000 = {}
count = 0
for tr in triangleXY_1000:
    dict_triangleXY_1000[count] = tr
    count += 1


list_layers = project.mapLayersByName("points")
layer_name = list_layers[0]
features = layer_name.getFeatures()
points = []
for feature in features:
    geom = feature.geometry()
    attr_list = feature.attributes()
    list_points = geom.asMultiPoint()
    pointXY = [list_points[0].x(), list_points[0].y()]
    points.append(pointXY)
coors = []
for point in  points:
    for triangle in triangleXY_200:
        if(is_in_triangle(point,triangle)):
#            print(get_key(dict_triangleXY_200, triangle))
            coors.append([dict_triangleXY_200[triangle], barycentric_out(point, triangle)])
            break

print(coors)

suri = "MultiPoint?crs=epsg:20008&index=yes"
name = "moved_point"
vl = QgsVectorLayer(suri, name, "memory")
pr = vl.dataProvider()
vl.updateExtents()
fet = QgsFeature()

for coor in coors:
    for triangle in triangleXY_1000:
        pointXY = barycentric_in(coor, triangle)
        if(is_in_triangle(pointXY, triangle)):
            fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(pointXY[0], pointXY[1])))
            pr.addFeatures([fet])
            vl.updateExtents()
            break

if not vl.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(vl)

#print("fields:", len(pr.fields()))
#print("features:", pr.featureCount())
#e = vl.extent()
#print("extent:", e.xMinimum(), e.yMinimum(), e.xMaximum(), e.yMaximum())
## iterate over features
#features = vl.getFeatures()
#for fet in features:
#    print("F:", fet.geometry().asPolygon(), end = '\n')


#crs = QgsProject.instance().crs()
#transform_context = QgsProject.instance().transformContext()
#save_options = QgsVectorFileWriter.SaveVectorOptions()
#save_options.driverName = "ESRI Shapefile"
#save_options.fileEncoding = "windows-1251"
#
#fields = QgsFields()
#writer = QgsVectorFileWriter.create(
#"E:\Никита\ИС-118\Диплом\VKR\\triangle.shp",
#fields,
#QgsWkbTypes.MultiPolygon,
#crs,
#transform_context,
#save_options
#)
#
#if writer.hasError() != QgsVectorFileWriter.NoError:
#    print("Error when creating shapefile: ",  writer.errorMessage())
#
#fet = QgsFeature()
#for triangl in triangleXY:
#    fet.setGeometry(QgsGeometry.fromPolygonXY([[QgsPointXY(triangl[0][0], triangl[0][1]), QgsPointXY(triangl[1][0], triangl[1][1]), QgsPointXY(triangl[2][0], triangl[2][1]), QgsPointXY(triangl[0][0], triangl[0][1])]]))
#    writer.addFeature(fet)
#
#del writer
#
#path = "E:\Никита\ИС-118\Диплом\VKR\\triangle.shp"
#vlayer = QgsVectorLayer(path, "triangle", "ogr")
#if not vlayer.isValid():
#    print("Layer failed to load!")
#else:
#    QgsProject.instance().addMapLayer(vlayer)

#areaOfInterest = QgsRectangle(450290,400520, 450750,400780)
#QgsTriangle(QgsPoint,QgsPoint,QgsPoint)
#request = QgsFeatureRequest().setFilterRect(areaOfInterest)
#
#for feature in layer.getFeatures(request):
#     do whatever you need with the feature
#    pass
