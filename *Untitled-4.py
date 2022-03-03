# create layer
suri = "MultiPolygon?crs=epsg:4326&index=yes"
vl = QgsVectorLayer(suri, "home2", "memory")
pr = vl.dataProvider()
vl.updateExtents()

# add a feature
fet = QgsFeature()
fet1 = QgsFeature()
fet.setGeometry(QgsGeometry.fromPolygonXY([[QgsPointXY(38.326744354550335, 52.903748081972225), 
QgsPointXY(38.755305743999074, 53.382566053475514), 
QgsPointXY(38.400584937508484, 53.45149301951075), 
QgsPointXY(37.97771606559452, 52.99432465569498), 
QgsPointXY(38.326744354550335, 52.903748081972225)]]))
fet1.setGeometry(QgsGeometry.fromPolygonXY([[QgsPointXY(42.151759858627194, 53.498933433360875), 
QgsPointXY(41.81802665855436, 53.69944591425968), 
QgsPointXY(41.532451487652715, 53.63830214792879), 
QgsPointXY(41.904036210210386, 53.41043947780082), 
QgsPointXY(42.151759858627194, 53.498933433360875)]]))
pr.addFeatures([fet])
pr.addFeatures([fet1])
vl.updateExtents()

vl.updateExtents()
if not vl.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(vl)