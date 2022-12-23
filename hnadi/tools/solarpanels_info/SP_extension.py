from functools import partial
import asyncio
import datetime

import omni.ext
import omni.usd
import omni.kit.ui
import omni.ui as ui
from omni.kit.viewport.utility import get_active_viewport_window

from .SP_ui import SolarPanelsINFO_Window
from . import SP_gol
from .viewport_scene import SunPathViewportScene


class SolarPanelsINFO_Extension(omni.ext.IExt):
    WINDOW_NAME : str = "SolarPanels Info Extension"
    MENU_PATH : str = f"Window/{WINDOW_NAME}"


    def _set_menu(self, value):
        """ Set the Menu to Create this Window on and off """
        editor_menu = omni.kit.ui.get_editor_menu()
        if editor_menu:
            editor_menu.set_value(SolarPanelsINFO_Extension.MENU_PATH, value)


    async def _destroy_window_async(self):
        # wait one frame, this is due to the one frame defer
        # in Window::_moveToMainOSWindow()
        await omni.kit.app.get_app().next_update_async()
        if self._window:
            self._window.destroy()
            self._window = None


    def _visiblity_changed_fn(self, visible):
        """ Called when the User Pressed "X" """
        self._set_menu(visible)
        if not visible:
            # Destroy the window, since we are creating new window
            # in show_window
            asyncio.ensure_future(self._destroy_window_async())


    def show_window(self, menu, value):
        """
        Show Window and Deliver Some Methods to it.
        Create ui.window Class and give it to the self._window property.
        """
        if value:
            # 核心操作：为self._window赋值class(ui.window)
            # 注意： Name: str, width: num, height: num 三者必不可少， 否则无法构建此类
            win_width = SP_gol.get_value("Win_Width")
            win_height = SP_gol.get_value("Win_Height")
            
            self._window = SolarPanelsINFO_Window(
                SolarPanelsINFO_Extension.WINDOW_NAME, 
                delegate1 = self.ChangeSceneFunction_sunpath_toggle, 
                delegate2 = self.ChangeSceneFunction_scale,
                delegate3 = self.ChangeSceneFunction_color,
                delegate4 = self.ChangeSceneFunction_time,
                width=win_width, height=win_height
            )

            self._window.set_visibility_changed_fn(self._visiblity_changed_fn)

        elif self._window:
            self._window.visible = False


    def on_startup(self, ext_id):
        """ 
        When Enable the Extension will Excute/Call this Method.
        Set the Ability to Show Window and Menu and Call self.show_window
        """
        # _init()字典，注意：此操作全局仅需用一次，否则字典会被再次初始化
        SP_gol._init()

        # Prepare Inital Settings for SunPathViewportScene
        self.ext_id = ext_id
        self.viewport_window = get_active_viewport_window()
        SP_gol.set_value("Ext_ID", self.ext_id)
        SP_gol.set_value("Actice_Viewport", self.viewport_window)

        # Remind Basic Info
        print("[hnadi.tools.SolarPanelsINFO] STARTUP")
        print(f"Extension ID: {ext_id}")

        # The Ability to Show up the Window if the System Requires it
        ui.Workspace.set_show_window_fn(SolarPanelsINFO_Extension.WINDOW_NAME, partial(self.show_window, None))

        # Add to the Menu in Toolbar
        editor_menu = omni.kit.ui.get_editor_menu()
        if editor_menu:
            self._menu = editor_menu.add_item(SolarPanelsINFO_Extension.MENU_PATH, self.show_window, toggle=True, value=True)

        # Show the Window. It will call `self.show_window`
        ui.Workspace.show_window(SolarPanelsINFO_Extension.WINDOW_NAME)


    def on_shutdown(self):
        """ 
        When Disable the Extension will Excute/Call this Method.
        Destroy the Window and the Viewport Scene 
        """
        print("[omni.tools.SolarPanelsINFO] SHUTDOWN")

        if self._window:
            self._window.destroy()
            self._window = None

        if self._viewport_scene:
            self._viewport_scene.destroy()
            self._viewport_scene = None

        self._menu = None

        # Deregister the function that shows the window from omni.ui
        ui.Workspace.set_show_window_fn(SolarPanelsINFO_Extension.WINDOW_NAME, None)


    def ChangeSceneFunction_sunpath_toggle(self, value):
        """ The Method to Show the Sunpath, this Dropped into the Window """
        SP_gol.set_value("Sunpath_Statu_Bool", value)

        if value:
            self._viewport_scene = SunPathViewportScene(self.viewport_window, self.ext_id)
        else:
            self._viewport_scene.destroy()
            self._viewport_scene = None


    def ChangeSceneFunction_scale(self, value):
        """ The Method to Change the Sun Path Scale """
        SP_gol.set_value("Sunpath_Scale", value)

        if self._viewport_scene:
            self._viewport_scene.destroy()
            self._viewport_scene = SunPathViewportScene(self.viewport_window, self.ext_id)
        else:
            print("Plz Turn on the Sun Path First")


    def ChangeSceneFunction_color(self, R_model, G_model, B_model):
        """ The Method to Change the Sun Path Color """
        R_value = R_model.get_value_as_float()
        G_value = G_model.get_value_as_float()
        B_value = B_model.get_value_as_float()
        RGB_value = (R_value, G_value, B_value)
        SP_gol.set_value("Sunpath_Color", RGB_value)

        if self._viewport_scene:
            self._viewport_scene.destroy()
            self._viewport_scene = SunPathViewportScene(self.viewport_window, self.ext_id)
        else:
            print("Plz Turn on the Sun Path First")


    def ChangeSceneFunction_time(self, HourModel, MonthModel):
        """ The Method to Change the Sun Path Time """
        Month_Num = MonthModel.get_value_as_int()
        Day = SP_gol.get_value("SunPath_Day")
        Datatime_value = int(datetime.date(2016, Month_Num, Day).strftime("%j"))
        # print(Datatime_value)
        SP_gol.set_item("Sunpath_Parameters", 0, Datatime_value) 

        Hour_value = HourModel.get_value_as_int()
        SP_gol.set_item("Sunpath_Parameters", 1, Hour_value) 

        if self._viewport_scene:
            self._viewport_scene.destroy()
            self._viewport_scene = SunPathViewportScene(self.viewport_window, self.ext_id)
            return self._viewport_scene