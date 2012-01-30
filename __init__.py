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
 This script initializes the plugin, making it known to QGIS.
"""
def name():
    return "Ringer"
def description():
    return "Converts rings to new polygons"
def version():
    return "Version 0.1"
def icon():
    return "icon.png"
def qgisMinimumVersion():
    return "1.0"
def classFactory(iface):
    # load Ringer class from file Ringer
    from ringer import Ringer
    return Ringer(iface)
