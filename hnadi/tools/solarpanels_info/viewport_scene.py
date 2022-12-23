__all__ = ["ViewportScene"]
import datetime

import omni.ui as ui
from omni.ui import scene as sc
from omni.ui import color as cl

from .sunpath import DrawSunpath, SunpathData
from . import SP_gol


class SunPathViewportScene():
    """The Object Info Manupulator, placed into a Viewport"""

    def __init__(self, viewport_window, ext_id: str):
        self._scene_view = None
        self._viewport_window = viewport_window

        # Create a unique frame for our SceneView
        with self._viewport_window.get_frame(ext_id):
            # Create a default SceneView (it has a default camera-model)
            self._scene_view = sc.SceneView()
            # Add the manipulator into the SceneView's scene
            with self._scene_view.scene:
                if SP_gol.get_value("Sunpath_Statu_Bool"):
                    pathmodel = SunpathData(*SP_gol.get_value("Sunpath_Parameters"))
                    sunpath = DrawSunpath(pathmodel)
                    sunpath.color = cl(*SP_gol.get_value("Sunpath_Color"))
                    sunpath.scale = SP_gol.get_value("Sunpath_Scale") * 200
                    sunpath.draw_sunpath()

            # Register the SceneView with the Viewport to get projection and view updates
            self._viewport_window.viewport_api.add_scene_view(self._scene_view)


    def __del__(self):
        self.destroy()


    def destroy(self):
        if self._scene_view:
            # Empty the SceneView of any elements it may have
            self._scene_view.scene.clear()
            # Be a good citizen, and un-register the SceneView from Viewport updates
            if self._viewport_window:
                self._viewport_window.viewport_api.remove_scene_view(self._scene_view)
        # Remove our references to these objects
        self._viewport_window = None
        self._scene_view = None


# Aborted
# class ChangeScene:
#     def __init__(self) -> None:
#         self.ext_id = SP_gol.get_value("Ext_ID")
#         self.viewport_window = SP_gol.get_value("Actice_Viewport")
#         self._viewport_scene = SunPathViewportScene(self.viewport_window, self.ext_id)


#     def ChangeSceneFunction_sunpath_toggle(self, value):
#         """ The Method to Show the Sunpath, this Dropped into the Window """
#         SP_gol.set_value("Sunpath_Statu_Bool", value)

#         if value:
#             self._viewport_scene = SunPathViewportScene(self.viewport_window, self.ext_id)
#         else:
#             self._viewport_scene.destroy()
#             self._viewport_scene = None


#     def ChangeSceneFunction_scale(self, value):
#         """ The Method to Change the Sun Path Scale """
#         SP_gol.set_value("Sunpath_Scale", value)

#         if self._viewport_scene:
#             self._viewport_scene.destroy()
#             self._viewport_scene = SunPathViewportScene(self.viewport_window, self.ext_id)
#         else:
#             print("Plz Turn on the Sun Path First")


#     def ChangeSceneFunction_color(self, R_model, G_model, B_model):
#         """ The Method to Change the Sun Path Color """
#         R_value = R_model.get_value_as_float()
#         G_value = G_model.get_value_as_float()
#         B_value = B_model.get_value_as_float()
#         RGB_value = (R_value, G_value, B_value)
#         SP_gol.set_value("Sunpath_Color", RGB_value)

#         if self._viewport_scene:
#             self._viewport_scene.destroy()
#             self._viewport_scene = SunPathViewportScene(self.viewport_window, self.ext_id)
#         else:
#             print("Plz Turn on the Sun Path First")


#     def ChangeSceneFunction_time(self, HourModel, MonthModel):
#         """ The Method to Change the Sun Path Time """
#         Month_Num = MonthModel.get_value_as_int()
#         Day = SP_gol.get_value("SunPath_Day")
#         Datatime_value = int(datetime.date(2016, Month_Num, Day).strftime("%j"))
#         # print(Datatime_value)
#         SP_gol.set_item("Sunpath_Parameters", 0, Datatime_value) 

#         Hour_value = HourModel.get_value_as_int()
#         SP_gol.set_item("Sunpath_Parameters", 1, Hour_value) 

#         if self._viewport_scene:
#             self._viewport_scene.destroy()
#             self._viewport_scene = SunPathViewportScene(self.viewport_window, self.ext_id)
#             return self._viewport_scene