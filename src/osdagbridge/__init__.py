from importlib.metadata import metadata
import uuid


IS_OSDAG_PLUGIN = True
META = {
    "name": "osdagbridge-plugin",
    "version": "1.0.0",
    "description": "OsdagBridge - Shared core for analysis and design of steel bridges (CLI, Desktop, Web)",
    "module_tree": [
    ("osdagbridge.core.bridge_types.plate_girder.plategirderbridge.PlateGirderBridge", "Plate Girder Bridge", ":/images/modules/bolted_tension_member.png"),
    ],

    "id": str(uuid.uuid5(uuid.NAMESPACE_DNS, f"osdagbridge-plugin:1.0.0")),
}

# --- Entry point: the class Osdag will instantiate on activation ---
ENTRY_POINT = "core.bridge_types.plate_girder.plategirderbridge.PlateGirderBridge"