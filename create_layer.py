vl = iface.activeLayer()
pr = vl.dataProvider()
fet = QgsFeature()
fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(8554199.6,6289640.6)))
pr.addFeatures([fet])
vl.updateExtents()

fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(8648405.2,6380124.2)))
pr.addFeatures([fet])
vl.updateExtents()

fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(8651159,6307233)))
pr.addFeatures([fet])
vl.updateExtents()

vl.removeSelection()
