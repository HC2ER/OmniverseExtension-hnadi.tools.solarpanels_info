import omni.usd
import omni.kit.commands
import omni.timeline
from pxr import Usd, Sdf, UsdShade 

from .SP_utils import map_data
from . import SP_gol


class SolarPanelPrimController:
    def __init__(self) -> None:
        pass


    def _get_SolarPanel_prim(self):
        stage = omni.usd.get_context().get_stage()
        SP_prim_path: pxr.Sdf.Path = Sdf.Path("/World/OV_SunlightPanelsSim/Geometry/SunlightPanels/SunlightPanels_")
        SP_prim: pxr.Usd.Prim = stage.GetPrimAtPath(SP_prim_path) # SP_prim_path 和 String 均可进行检索
        if SP_prim:
            SP_gol.set_value("SolarPanels_Flag", True)
            SP_gol.set_value("SolarPanels_Prim", SP_prim)
            SP_gol.set_value("SolarPanels_PrimPath", SP_prim_path)

            # composedBindingAPI = UsdShade.MaterialBindingAPI(SP_prim)
            # SP_material_prim = composedBindingAPI.GetDirectBinding().GetMaterial()
            # SP_material_path = Sdf.Path("/World/OV_SunlightPanelsSim/Looks/SimulationTimestamp")
            # SP_gol.set_value("Material_Prim", SP_material_prim)
            # SP_gol.set_value("Material_Path", SP_material_path)

            # LoadCounts = SP_gol.get_value("Load_Counts")
            # LoadCounts += 1
            # SP_gol.set_value("Load_Counts", LoadCounts)
            return
        else:
            print("Core Function Error: Cannot Find SolarPanels Prim, Plz Reload or Rename it")
            return


    def _set_timeline(self, time_codes = 30):
        flag: bool = SP_gol.get_value("SolarPanels_Flag")

        if flag == True:
            # Set Timeline Basic Settings
            SP_prim = SP_gol.get_value("SolarPanels_Prim")
            time_codes_per_sec = time_codes

            data_default = SP_prim.GetAttribute('primvars:sim_data').Get()
            data_StartFrame = data_default[0]
            data_FramesPerNumber = data_default[1]
            data_Number = data_default[2]

            data_FrameLength = data_Number * data_FramesPerNumber
            data_EndFrame = data_StartFrame + data_FrameLength

            timeline = omni.timeline.get_timeline_interface()
            omni.timeline.ITimeline.set_time_codes_per_second(timeline, time_codes_per_sec)

            start_time = omni.usd.get_frame_time(data_StartFrame, time_codes_per_sec)
            omni.timeline.ITimeline.set_start_time(timeline, start_time)

            end_time = omni.usd.get_frame_time(data_EndFrame, time_codes_per_sec)
            omni.timeline.ITimeline.set_end_time(timeline, end_time)

            SP_gol.set_value("TimeLine", timeline)
            SP_gol.set_value("TimeLine_StartFrame", data_StartFrame)
            SP_gol.set_value("TimeLine_EndFrame", data_EndFrame)
            SP_gol.set_value("TimeLine_TimeCodesUnit", time_codes)
            return 
        else:
            print("Core Function Error: _set_timeline Error")
            return 


    def _control_timeline(self, offset_value):
        flag: bool = SP_gol.get_value("SolarPanels_Flag")
        timeline = SP_gol.get_value("TimeLine")

        if flag == True and timeline != None:
            StartFrame = SP_gol.get_value("TimeLine_StartFrame")
            EndFrame = SP_gol.get_value("TimeLine_EndFrame")
            max = SP_gol.get_value("Max")
            min = SP_gol.get_value("Min")
            time_codes = SP_gol.get_value("TimeLine_TimeCodesUnit")

            # Control TimeLine
            current_handle_frame = map_data(offset_value, min, max, StartFrame, EndFrame)
            current_handle_time = omni.usd.get_frame_time(current_handle_frame, time_codes)
            omni.timeline.ITimeline.set_current_time(timeline, current_handle_time)
            SP_gol.set_value("CurrentTime", current_handle_time)
            return
        else:
            print("Core Function Error: _control_timeline Error")
            return 


    def _get_SolarPanels_RuntimeData_Fill_UI(self):
        flag: bool = SP_gol.get_value("SolarPanels_Flag")
        timeline = SP_gol.get_value("TimeLine")
        SP_prim = SP_gol.get_value("SolarPanels_Prim")
        time_codes_per_sec = SP_gol.get_value("TimeLine_TimeCodesUnit")
        current_handle_time = SP_gol.get_value("CurrentTime")

        if flag == True and timeline != None and current_handle_time != None:
            # A Get Current Data
            current_frame = omni.usd.get_frame_time_code(current_handle_time, time_codes_per_sec)
            current_data = SP_prim.GetAttribute('primvars:sim_data').Get(current_frame)
            # print(current_data)
            # current data ✔
            current_data_Type = int(current_data[4])
            current_data_Length = round(current_data[5], 2)
            current_data_Width = round(current_data[6], 2)

            current_data_AngleMin = round(current_data[7], 2)
            if current_data_Type == 1:
                current_data_AngleMax = 0.00
            else:
                current_data_AngleMax = round(current_data[8], 2)

            current_data_Count = current_data[9]
            current_data_Row = current_data[10]
            current_data_Area = current_data[11]

            current_data_Year = current_data[13]
            current_data_Month = int(current_data[14])
            current_data_Day = current_data[15]
            current_data_Hour = int(current_data[16])
            current_data_SunR = round(current_data[17], 2)

            # B Fill All Other UI Widgets
            Length = SP_gol.get_sub_value("UI_All_Widgets", "Length")
            Length.model.set_value(current_data_Length)

            Width = SP_gol.get_sub_value("UI_All_Widgets", "Width")
            Width.model.set_value(current_data_Width)
            
            Min_Angle = SP_gol.get_sub_value("UI_All_Widgets", "Min_Angle")
            Min_Angle.model.set_value(current_data_AngleMin)

            Max_Angle = SP_gol.get_sub_value("UI_All_Widgets", "Max_Angle")
            Max_Angle.model.set_value(current_data_AngleMax)

            Count = SP_gol.get_sub_value("UI_All_Widgets", "Count")
            Count.model.set_value(current_data_Count)

            Row = SP_gol.get_sub_value("UI_All_Widgets", "Row")
            Row.model.set_value(current_data_Row)

            Area = SP_gol.get_sub_value("UI_All_Widgets", "Area")
            Area.model.set_value(current_data_Area)

            Year = SP_gol.get_sub_value("UI_All_Widgets", "Year")
            Year.model.set_value(current_data_Year)

            Month = SP_gol.get_sub_value("UI_All_Widgets", "Month")
            Month.model.set_value(current_data_Month)

            Day = SP_gol.get_sub_value("UI_All_Widgets", "Day")
            Day.model.set_value(current_data_Day)

            Hour1 = SP_gol.get_sub_value("UI_All_Widgets", "Hour1")
            Hour1.model.set_value(current_data_Hour)

            Hour2 = SP_gol.get_sub_value("UI_All_Widgets", "Hour2")
            Hour2.model.set_value(current_data_Hour)

            SunR = SP_gol.get_sub_value("UI_All_Widgets", "SunR")
            SunR.model.set_value(current_data_SunR)

            Type = SP_gol.get_sub_value("UI_All_Widgets", "Type")
            Type.model.set_value(current_data_Type)
            return

        else:
            print("Core Function Error: _get_SolarPanels_RuntimeData_Fill_UI Error")
            return 


    def _set_all_status(self):
        flag: bool = SP_gol.get_value("SolarPanels_Flag")
        timeline = SP_gol.get_value("TimeLine")

        if flag == True and timeline != None:
            SP_prim = SP_gol.get_value("SolarPanels_Prim")
            StartFrame = int(SP_gol.get_value("TimeLine_StartFrame"))
            EndFrame = int(SP_gol.get_value("TimeLine_EndFrame"))
            max = SP_gol.get_value("Max")
            # print(StartFrame)
            # print(EndFrame)

            for single_frame in range(StartFrame, EndFrame+1, 1):
                # print(single_frame)
                single_frame_data = SP_prim.GetAttribute('primvars:sim_data').Get(single_frame)
                single_frame_Type = int(single_frame_data[4])
                single_frame_Month = int(single_frame_data[14])
                single_frame_Hour = int(single_frame_data[16])
                single_frame_SunR = round(single_frame_data[17], 2)
                single_frame_Time = map_data(single_frame, StartFrame, EndFrame, 0, max)
                tuple = (single_frame_Type, single_frame_Month, single_frame_Hour, single_frame_SunR, single_frame_Time)
                SP_gol.get_value("All_Status").append(tuple)
            return  

        else:
            print("Core Function Error: _set_all_status Error")
            return 


    def _get_statu(self, Type, Month, Hour1):
        all_status = SP_gol.get_value("All_Status")

        if len(all_status) > 0:
            Type = Type
            Month = Month
            Hour1 = Hour1

            Hour2 = SP_gol.get_sub_value("UI_All_Widgets", "Hour2")
            SunR = SP_gol.get_sub_value("UI_All_Widgets", "SunR")
            Main_Slider = SP_gol.get_sub_value("UI_All_Widgets", "Main_Slider")

            Type_value = Type.model.get_value_as_int()
            Month_value = Month.model.get_value_as_int()
            Hour_value = Hour1.model.get_value_as_int()
            tuple = (Type_value, Month_value, Hour_value)
            # print(tuple)

            A = []
            for single_statu in all_status:
                check_tuple = (single_statu[0], single_statu[1], single_statu[2])

                if check_tuple == tuple:
                    Hour2.model.set_value(single_statu[2])
                    SunR.model.set_value(single_statu[3])
                    Time = single_statu[4]
                    # print(Time)
                    Main_Slider.model.set_value(Time)
                    A.append(1)
            
            if len(A) == 0:
                # TODO FIX BUG
                # print("Invalid Input, Plz enter exist status")
                return 
                
        else:
            print("Core Function Error: _get_statu Error")
            return 


    def _set_color(self, bool):
        SP_prim = SP_gol.get_value("SolarPanels_Prim")
        SP_primpath = SP_gol.get_value("SolarPanels_PrimPath")

        SP_material_path = SP_gol.get_value("Material_Path")
        composedBindingAPI = UsdShade.MaterialBindingAPI(SP_prim)
        current_material = composedBindingAPI.GetDirectBinding().GetMaterial()
        current_material_path = current_material.GetPath()
        # print(current_material)


        if str(current_material_path) == str(SP_material_path):
            # 如果是指定颜色，去色为None
            omni.kit.commands.execute('BindMaterial',
                                    material_path=None,
                                    prim_path=[SP_primpath],
                                    strength=['weakerThanDescendants'])
                
        else:
            # 如果是None或其他颜色，上指定颜色
            omni.kit.commands.execute('BindMaterial',
                        material_path=SP_material_path,
                        prim_path=[SP_primpath],
                        strength=['weakerThanDescendants'])
        return


    def _update_model(self, bool):
        self._get_SolarPanel_prim()
        return