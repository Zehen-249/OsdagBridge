import os, sys
import yaml


from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from osdag_gui.plugin.widget_plugin import WidgetPlugin
# from osdag_gui.ui.windows.template_page import CustomWindow
from osdag_gui.data.database.database_config import MODULE_MAP

from osdagbridge import META
from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge
from osdagbridge.core.utils.common import KEY_MODULE_PLATE_GIRDER
from osdagbridge.desktop.ui.template_page import CustomWindow

class OsdagBridgePlugin(WidgetPlugin):
    def __init__(self):
        super().__init__()
        for key, value in META.items():
            setattr(self, key, value)

    def open(self, module_key, module_name, main_window):
        """
        This method is called when the plugin is opened by clicking on SVG card in the Osdag GUI. It should contain the logic to initialize and display the plugin's user interface.
        
        :param module_key: The unique key of the module that is being opened.
        :param module_name: Display name of the module that is being opened.
        :param main_window: The main window object of the Osdag GUI.

        :return: None
        """
        self.module_key = module_key
        self.module_name = module_name
        self.main_window = main_window

        MODULE_MAP[self.module_key] = [module_key, module_name, self.open, "OsdagBridge"]

        self.backend_class = self._backend_class(module_key)

        id = self.main_window.update_module_count(self.backend_class)
        self.main_window.clear_layout(self.main_window.main_widget_layout)
        
        template_page = CustomWindow(module_name.title(), self.backend_class, parent=self.main_window)
        
        # Connect Import XLSX
        # template_page.importSection.connect(self.main_window.import_section)

        template_page.setWindowFlags(Qt.Widget)
        template_page.setAttribute(Qt.WA_DontCreateNativeAncestors, True)
        template_page.setAttribute(Qt.WA_NativeWindow, False)
        
        # Prevent all children from creating native windows
        # IMPORTANT: This enables event detection after opening template_page
        for child in template_page.findChildren(QWidget):
            child.setAttribute(Qt.WA_DontCreateNativeAncestors, True)

        # # Load the last Design Inputs-start------------------------------------
        # last_design_folder = os.path.join('ResourceFiles', 'last_designs')
        # last_design_file = str(module_name).replace(' ', '') + ".osi"
        # last_design_file = os.path.join(last_design_folder, last_design_file)
        # last_design_dictionary = {}

        # # Create folder if it doesn't exist
        # if not os.path.isdir(last_design_folder):
        #     os.makedirs(last_design_folder)

        # # Load previous design if file exists
        # if os.path.isfile(last_design_file):
        #     with open(str(last_design_file), 'r') as last_design:
        #         last_design_dictionary = yaml.safe_load(last_design)
        #         template_page.setDictToUserInputs(last_design_dictionary)
        # Load the last Design Inputs-end------------------------------------

        self.main_window.main_widget_instance = template_page
        # template_page.downloadDatabase.connect(self.main_window.download_Database)
        self.main_window._update_sidebar_visibility()
        self.main_window.main_widget_layout.addWidget(template_page)
        
        index = self.main_window.tab_bar.currentIndex()
        self.main_window.tab_bar.setTabText(index, module_name.title())

    def _backend_class(self, module_key):
        """
        This method returns the backend class associated with the module key.

        :param module_key: Key of the module that is being opened.
        :return: The backend class associated with the plugin.
        """

        if module_key == KEY_MODULE_PLATE_GIRDER:
            return PlateGirderBridge