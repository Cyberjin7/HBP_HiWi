
# #####
# This file is part of the RobotDesigner of the Neurorobotics subproject (SP10)
# in the Human Brain Project (HBP).
# It has been forked from the RobotEditor (https://gitlab.com/h2t/roboteditor)
# developed at the Technical University of Munich at the chair of embedded and robotic system.
# #####

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# #####
#
# Copyright (c) 2016, FZI Forschungszentrum Informatik
#
# Changes:
#
#   2016-12-08: Guang Chen (TUM), Major refactoring. Integrated into complex plugin framework.
#
# ######

"""
This module adds SDF support to the RobotDesigner
"""

from . import sdf_export, sdf_import, generic, sdf_world_export, sdf_world_import

from importlib import reload

reload(generic)
reload(sdf_export)
reload(sdf_import)
reload(sdf_world_export)
reload(sdf_world_import)

from .sdf_import import ImportPlain, ImportPackage, ImportZippedPackage
from .sdf_export import ExportPlain, ExportPackage, ExportZippedPackage
from .sdf_world_export import ExportPlainWorld
from .sdf_world_import import ImportPlainWorld

__author__ = "gchen"
