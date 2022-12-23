import omni.usd
import omni.kit.commands
import omni.timeline
import omni.ui as ui
from pxr import Usd, Sdf, Gf


""" Build Global Dictionary """
# Inital Settings
def _init():
    global _global_dict
    _global_dict = {}

    # SolarPanels CheckFlag
    _global_dict["SolarPanels_Flag"] = False
    _global_dict["SolarPanels_Prim"] = None
    _global_dict["SolarPanels_PrimPath"] = None
    _global_dict["Ext_ID"] = None
    _global_dict["Actice_Viewport"] = None
    _global_dict["Load_Counts"] = 0


    # SolarPanels Attributes
    _global_dict["Material_Prim"] = None
    _global_dict["Material_Path"] = "/World/OV_SunlightPanelsSim/Looks/SimulationTimestamp"

    # TimeLine Basic Settings
    _global_dict["TimeLine"] = None
    _global_dict["TimeLine_StartFrame"] = 0
    _global_dict["TimeLine_EndFrame"] = 1000
    _global_dict["TimeLine_TimeCodesUnit"] = 30
    _global_dict["Min"] = 0
    _global_dict["Max"] = 100

    # SolarPanels RunTime Data
    _global_dict["CurrentTime"] = None

    # UI Basic Settings
    _global_dict["Win_Width"] = 370
    _global_dict["Win_Height"] = 490

    # UI Widgets
    """ For Fransforming UI Widgets and Set Their Functions in ui.py """
    _UI_All_Widgets = _global_dict["UI_All_Widgets"] = {}
    _UI_All_Widgets["Length"] = None
    _UI_All_Widgets["Width"] = None
    _UI_All_Widgets["Min_Angle"] = None
    _UI_All_Widgets["Max_Angle"] = None
    _UI_All_Widgets["Count"] = None
    _UI_All_Widgets["Row"] = None
    _UI_All_Widgets["Area"] = None

    _UI_All_Widgets["Month"] = None
    _UI_All_Widgets["Day"] = None
    _UI_All_Widgets["Year"] = None
    _UI_All_Widgets["Hour1"] = None
    _UI_All_Widgets["Hour2"] = None
    _UI_All_Widgets["SunR"] = None
    _UI_All_Widgets["Type"] = None
    _UI_All_Widgets["Color"] = None
    _UI_All_Widgets["Reload"] = None

    _UI_All_Widgets["Main_Slider"] = None

    # Status
    """ Call _set_all_status, Then Create a List to Store Status (Type, Month, Hour, SunR, Time) with Tuple"""
    _global_dict["All_Status"] = _All_Status = []

    # Sunpath
    _global_dict["Sunpath_Statu_Bool"] = False
    _global_dict["Sunpath_Scale"] = 1.0
    _global_dict["Sunpath_Color"] = (1, 1, 1)
    _global_dict["Sunpath_Parameters"] = [231, 7, 1, 52.54, 13.40] # 0:一年中的第几天  1：小时  2：分钟  3：纬度  4：经度
    _global_dict["SunPath_Day"] = 21


# Methods
def set_value(key: str, value):
    _global_dict[key] = value


def set_sub_value(key: str, sub_key: str, value):
    _global_dict[key][sub_key] = value


def get_value(key: str):
    try:
        return _global_dict[key]
    except:
        print("Get " + key + " Fail\r\n")


def get_sub_value(key: str, sub_key: str):
    try:
        return _global_dict[key][sub_key]
    except:
        print("Get " + key + " Fail\r\n")


def set_item(key, i, value):
    _global_dict[key][i] = value