vl = iface.activeLayer()
pr = vl.dataProvider()

fet = QgsFeature()
fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(8482791,6516160)))
fet.setAttributes([0, "false"])
pr.addFeatures([fet])
vl.updateExtents()
