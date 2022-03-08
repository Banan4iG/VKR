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


print(barycentric_in([0.42037206759654655, 0.22840344166641824, 0.35122449073703504], [[43.36477917, 53.32235807],[41.54604340, 54.05338552],[40.38851334, 53.09775022]]))


#
## create layer
#suri = "MultiPolygon?crs=epsg:4326&index=yes"
#vl = QgsVectorLayer(suri, "home2", "memory")
#pr = vl.dataProvider()
#vl.updateExtents()
#
## add a feature
#fet = QgsFeature()
#for triangl in triangleXY:
#    fet.setGeometry(QgsGeometry.fromPolygonXY([[QgsPointXY(triangl[0][0], triangl[0][1]), QgsPointXY(triangl[1][0], triangl[1][1]), QgsPointXY(triangl[2][0], triangl[2][1]), QgsPointXY(triangl[0][0], triangl[0][1])]]))
#    pr.addFeatures([fet])
#    vl.updateExtents()
#
#vl.updateExtents()
#if not vl.isValid():
#    print("Layer failed to load!")
#else:
#    QgsProject.instance().addMapLayer(vl)