from importlib.resources import files
from osdagbridge.core.utils.common import KEY_MODULE_PLATE_GIRDER

# Indicates that this module is a valid Osdag plugin
IS_OSDAG_PLUGIN = True

META = {
    "name": "OsdagBridge",
    "description": "A bridge module for Osdag",
    "authors": ["FOSSEE Team"],
    "version": "1.0.0",
    "plugin_class": "osdagbridge.plugin.osdagbridge_plugin:OsdagBridgePlugin",
    "module_tree":[
        (
            KEY_MODULE_PLATE_GIRDER, "Plate Girder Bridge", str(files("osdagbridge").joinpath("desktop", "resources", "images","osdagbridge_plate_girder_bridge.png"))
        ),
    ],
    "icons":[
        str(files("osdag_gui").joinpath("resources", "vectors", "nav_icons", "group_design.svg")),
        str(files("osdag_gui").joinpath("resources", "vectors", "nav_icons", "group_design_dark.svg"))
    ]
}