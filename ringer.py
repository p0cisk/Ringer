"""
/***************************************************************************
 Ringer
                                 A QGIS plugin
 Converts polygon inner rings to polygons
                              -------------------
        begin                : 2011-03-08
        copyright            : (C) 2011 by Pocisk
        email                : pocisk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog

class Ringer:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(QIcon(":/plugins/ringer/icon.png"), \
            "Ringer", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        # Add toolbar button and menu item
        QObject.connect(self.iface, SIGNAL("currentLayerChanged(QgsMapLayer*)"), self.EnablePlugin)
        self.iface.advancedDigitizeToolBar().addAction(self.action)
        #self.iface.addPluginToMenu("&Ringer", self.action)
        self.action.setEnabled(False)

    def unload(self):
        # Remove the plugin menu item and icon
        #self.iface.removePluginMenu("&Ringer",self.action)
        self.iface.advancedDigitizeToolBar().removeAction(self.action)

    # run method that performs all the real work
    def run(self):
        layer = self.iface.activeLayer()
        provider = layer.dataProvider()
        fet = QgsFeature()
        geom = []
        fets = []

        onlySelected = (layer.selectedFeatureCount() <> 0)
        #QInputDialog.getText( self.iface.mainWindow(), "t", "b",   QLineEdit.Normal, 'tak' )

        allAttrs = provider.attributeIndexes()
        provider.select(allAttrs)
        fields = provider.fields()

        if not onlySelected:
            layer.invertSelection()

        fets = layer.selectedFeatures()

        for fet in fets:

            if fet.geometry().isMultipart():
                geom = fet.geometry().asMultiPolygon()
                for polygon in geom:
                    self.addPolys(polygon, layer)
            else:
                geom = fet.geometry().asPolygon()
                self.addPolys(geom, layer)

        if not onlySelected:
            layer.invertSelection()

        self.iface.mapCanvas().refresh()


    def addPolys(self, polygon, layer):
        rings = []
        fetOut = QgsFeature()
        if len(polygon)>1:
            rings = polygon[1:]
            for ring in rings:
                fetOut.setGeometry( QgsGeometry.fromPolygon([ring]) )
                layer.addFeature(fetOut,False)
                undo = QgsUndoCommand(layer, 'add feature')
                undo.storeFeatureAdd(fetOut)
            #layer.setModified(True,True)

    def EnablePlugin(self):
        layer = self.iface.activeLayer()
        if layer <> None:
            if (layer.isEditable()) and (layer.geometryType() == QGis.Polygon):
                self.action.setEnabled(True)
                QObject.connect(layer,SIGNAL("editingStopped()"),self.EnablePlugin)
                QObject.disconnect(layer,SIGNAL("editingStarted()"),self.EnablePlugin)
            else:
                self.action.setEnabled(False)
                QObject.connect(layer,SIGNAL("editingStarted()"),self.EnablePlugin)
                QObject.disconnect(layer,SIGNAL("editingStopped()"),self.EnablePlugin)