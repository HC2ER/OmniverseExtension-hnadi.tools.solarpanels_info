from os import path
from functools import partial

from pxr import UsdGeom, Tf, Usd
import omni.ui as ui

from data.SP_image_path import SP_image_path
from . import SP_gol
from .SP_core import SolarPanelPrimController
# from .viewport_scene import ChangeScene (Aborted)
from .SP_style import HNADI_window_style, white

class SolarPanelsINFO_Window(ui.Window):
    """ The Class Representing the Window for all UI """

    def __init__(self, title: str, delegate1, delegate2, delegate3, delegate4, **kwargs):
    # def __init__(self, title: str, **kwargs):
        """ Set Inital Data in need & Inital Settings """
        super().__init__(title, **kwargs)

        # Call this Function to Build Widgets when the Window is Visible
        self.frame.set_build_fn(self._build_fn) 

        # Call this function to Apply Uniform Style to all Widgets in this Window
        self.frame.style = HNADI_window_style

        # Delegate Functions
        self.ChangeSceneFunction_sunpath_toggle = delegate1
        self.ChangeSceneFunction_scale = delegate2
        self.ChangeSceneFunction_color = delegate3
        self.ChangeSceneFunction_time = delegate4


    def destroy(self):
        """ The Method that is Called when the Window is Closed """
        # print("Main Window Closed")
        super().destroy()
        return
    

    def _build_fn(self):
        """ The Method that is Called to Build All the UI once the Window is Visible """
        SolarPanelPrimController()._get_SolarPanel_prim()
        SolarPanelPrimController()._set_timeline(time_codes = 30)
        with ui.VStack(height=0):
            self._build_basic_information_UI()
            self._build_carbon_emssions_sim_UI()
            self._build_sunpath_editor_UI()
            self._build_main_control_handle_slider()
            self._build_callback_widgets_functions()
        return


    def _build_basic_information_UI(self):
        """ Build the UI Widgets of the "Basic Information" Group """
        # A Build Basic Information UI Widgets
        with ui.CollapsableFrame("Basic Information", name="group", build_header_fn=self._build_collapsable_header):
            with ui.VStack():
                ui.Spacer(height=8)
                with ui.HStack():

                    # Size & Angle 
                    with ui.VStack(height=90):
                        ui.Spacer(height=5)
                        with ui.HStack():
                            ui.Spacer(width=5)
                            ui.Label("Size", name="attribute_name", width = 20, height = 25, tooltip="Size of Single Panel")
                            ui.Spacer(width=5)

                            Length = self._build_labelled_floatfield("Len", label_color=0xFF5555AA, label_height=26, number_height=26, 
                            tooltip1="Single Panel Length", tooltip2="meter")

                            ui.Spacer(width=10)

                            Width = self._build_labelled_floatfield("Wid", label_color=0xFF76A371, label_height=26, number_height=26,
                            tooltip1="Single Panel Width", tooltip2="meter")

                        ui.Spacer(height=13)
                        with ui.HStack():
                            ui.Label("Angle", name="attribute_name", width = 20, height = 25, tooltip="Angle Range of Array")

                            Min_Angle = self._build_labelled_floatfield("Min", label_color=0xFF5555AA, label_height=26, number_height=26,
                            tooltip1="Array Min Angle", tooltip2="degree")
    
                            ui.Spacer(width=10)

                            Max_Angle = self._build_labelled_floatfield("Max", label_color=0xFF76A371, label_height=26, number_height=26,
                            tooltip1="Array Max Angle", tooltip2="degree")

                        ui.Spacer(height=18)

                    ui.Spacer(width=10)

                    # Counts & Array 
                    with ui.VStack(height=85, width=101):
                        Count = self._build_intfield("Count", space=0, label_width=5, label_height=25, number_height=25, tooltip1 ="Total Number", tooltip2="" )
                        Row = self._build_intfield("Row", space=11, label_width=5, label_height=25, number_height=25, tooltip1 ="Rows of Array", tooltip2="")
                        Area = self._build_intfield("Area", space=9, label_width=5, label_height=25, number_height=25, tooltip1 ="Total Area", tooltip2="square meter" )
                    ui.Spacer(width=7)

        ui.Spacer(height=0)

        # B Transform All UI Widgets to SP_gol         
        SP_gol.set_sub_value("UI_All_Widgets", "Length", Length)
        SP_gol.set_sub_value("UI_All_Widgets", "Width", Width)
        SP_gol.set_sub_value("UI_All_Widgets", "Min_Angle", Min_Angle)
        SP_gol.set_sub_value("UI_All_Widgets", "Max_Angle", Max_Angle)
        SP_gol.set_sub_value("UI_All_Widgets", "Count", Count)
        SP_gol.set_sub_value("UI_All_Widgets", "Row", Row)
        SP_gol.set_sub_value("UI_All_Widgets", "Area", Area)
        return 
            

    def _build_carbon_emssions_sim_UI(self):
        """ Build the UI Widgets of the "Carbon Emissions Reduction Simulation" Group """
        # A Build Carbon Emssions Simulation UI Widgets            
        with ui.CollapsableFrame("Carbon Emssions Reduction Simluation", name="group", build_header_fn=self._build_collapsable_header):
            with ui.VStack():
                ui.Spacer(height=10)

                # Time to day 
                with ui.HStack():
                    ui.Spacer(width=2)
                    ui.Label("Date", name="attribute_name", width = 30, height = 25, tooltip="Sun Date")
                    ui.Spacer(width=3)

                    Month = self._build_labelled_intfield("Mth", label_color=0xFF76A371, label_height=26, number_height=26, tooltip1="Sun Date", tooltip2="month")
                    Month.model.set_value(7)
                    ui.Spacer(width = 12)

                    Day = self._build_labelled_intfield("D", label_color=0xFF76A371, label_height=26, number_height=26, tooltip1="Sun Date", tooltip2="day")
                    Day.model.set_value(21)
                    ui.Spacer(width = 12)

                    Year = self._build_labelled_intfield("Yr", label_color=0xFF76A371, label_height=26, number_height=26, tooltip1="Sun Date", tooltip2="year")
                    Year.model.set_value(2016)

                    ui.Spacer(width=6)

                ui.Spacer(height = 10)

                # Time to hour 
                with ui.HStack():
                    ui.Spacer(width=2)
                    Hour1 = self._build_intslider("Hour", label_width=38, label_height=25, tooltip1="Sun Date", tooltip2="hour")
                    ui.Spacer(width = 10)
                    Hour2 = ui.IntField(height=15, width=52, tooltip="hour")
                    ui.Spacer(width=6)

                ui.Spacer(height = 5)

                # Energy & Type & Color 
                with ui.HStack():
                    SunR = self._build_floatfield2("Enrg", label_width=36, label_height=26, number_height=25, tooltip1="Total Collected Energy per Hour", tooltip2="KW/h")
                    Type = self._build_intfield2("Type", label_width=30, label_height=26, number_height=25, tooltip1="Array Type", tooltip2="type of solar panel array")
                    Type.model.set_value(1)
                    ui.Spacer(width = 8)

                    Color = self._build_button("Gradient", button_width=55, button_height=31, tooltip="Color Gradient")
                    ui.Spacer(width = 4)
                    Reload = self._build_button("Reload",  button_width=57, button_height=31, tooltip="Reload Model")

                    ui.Spacer(width = 4)

        ui.Spacer(height=0)

        # B Transform All UI Widgets to SP_gol         
        SP_gol.set_sub_value("UI_All_Widgets", "Month", Month)
        SP_gol.set_sub_value("UI_All_Widgets", "Day", Day)
        SP_gol.set_sub_value("UI_All_Widgets", "Year", Year)
        SP_gol.set_sub_value("UI_All_Widgets", "Hour1", Hour1)
        SP_gol.set_sub_value("UI_All_Widgets", "Hour2", Hour2)
        SP_gol.set_sub_value("UI_All_Widgets", "SunR", SunR)
        SP_gol.set_sub_value("UI_All_Widgets", "Type", Type)
        SP_gol.set_sub_value("UI_All_Widgets", "Color", Color)
        SP_gol.set_sub_value("UI_All_Widgets", "Reload", Reload)
        return 


    def _build_sunpath_editor_UI(self):
        """ Build the UI Widgets for the "Sunpath Editor" Group """
        # A Build Sunpath Editor UI Widgets            
        with ui.CollapsableFrame("Sunpath Editor", name="group", build_header_fn=self._build_collapsable_header):
            with ui.HStack():
                ui.Spacer(width=3)
                with ui.VStack():
                    ui.Spacer(height=1)
                    ui.Label("Sun Path", name="attribute_name", width=10, height=20, tooltip="Set Sun Path Model")

                with ui.VStack():
                    ui.Spacer(height=3.5)
                    SunPathStatu = ui.CheckBox()
                    SunPathStatu.model.set_value(False)

                with ui.VStack():
                    ui.Spacer(height=1)
                    ui.Label("Scale", name="attribute_name", height=20, tooltip="Scale of Sun Path Model")
                SunPathScale = ui.IntField(width=42, name="attribute_field")
                SunPathScale.model.set_value(100)

                ui.Spacer(width=5)
                with ui.VStack():
                    ui.Spacer(height=1)
                    ui.Label("Color", name="attribute_name", width=30, height=20, tooltip="Color of Sun Path Model")

                ui.Spacer(width=0)
                R = ui.FloatField(name="attribute_field")
                ui.Spacer(width=1)
                G = ui.FloatField(name="attribute_field")
                ui.Spacer(width=1)
                B = ui.FloatField(name="attribute_field")

                ui.Spacer(width=3)
                SunPathColor = ui.ColorWidget(1, 1, 1, width=20, height=20)

                PathColorModel = SunPathColor.model
                R.model = PathColorModel.get_item_value_model(PathColorModel.get_item_children()[0])
                G.model = PathColorModel.get_item_value_model(PathColorModel.get_item_children()[1])
                B.model = PathColorModel.get_item_value_model(PathColorModel.get_item_children()[2])

                R_value = R.model.get_value_as_float()
                G_value = G.model.get_value_as_float()
                B_value = B.model.get_value_as_float()
                RGB_value = (R_value, G_value, B_value)
                SP_gol.set_value("Sunpath_Color", RGB_value)

                ui.Spacer(width = 6)
        ui.Spacer(height=0)

        # B Set SunPath UI Functions
        # V1 Extension Delegate
        SunPathStatu.model.add_value_changed_fn(lambda b: self.ChangeSceneFunction_sunpath_toggle(b.get_value_as_bool()))
        SunPathScale.model.add_value_changed_fn(lambda m: self.ChangeSceneFunction_scale(m.get_value_as_float()))
        R.model.add_value_changed_fn(lambda m: self.ChangeSceneFunction_color(R.model, G.model, B.model))
        G.model.add_value_changed_fn(lambda m: self.ChangeSceneFunction_color(R.model, G.model, B.model))
        B.model.add_value_changed_fn(lambda m: self.ChangeSceneFunction_color(R.model, G.model, B.model))

        # V2 Class (Aborted)
        # SunPathStatu.model.add_value_changed_fn(lambda b: ChangeScene().ChangeSceneFunction_sunpath_toggle(b.get_value_as_bool()))
        # SunPathScale.model.add_value_changed_fn(lambda m: ChangeScene().ChangeSceneFunction_scale(m.get_value_as_float()))
        # R.model.add_value_changed_fn(lambda m: ChangeScene().ChangeSceneFunction_color(R.model, G.model, B.model))
        # G.model.add_value_changed_fn(lambda m: ChangeScene().ChangeSceneFunction_color(R.model, G.model, B.model))
        # B.model.add_value_changed_fn(lambda m: ChangeScene().ChangeSceneFunction_color(R.model, G.model, B.model))
        
        return    


    def _build_main_control_handle_slider(self):
        """Build the UI Widget of the Main Control Handle Slider;
           Set its Function to Control the TimeLine and Fill the Data of Other UI Widgets
        """
        # A Build Main Slider UI
        with ui.CollapsableFrame("Solar Panels Controller", name="group", build_header_fn=self._build_collapsable_header):
            with ui.ZStack():
                # A1 Set a Background Image
                with ui.VStack():
                    ui.Spacer(height=2)
                    image = ui.Image(SP_image_path.backgroundZ, fill_policy=ui.FillPolicy.PRESERVE_ASPECT_CROP, alignment=ui.Alignment.CENTER, height=20.5,
                            style = {"border_radius":6})
                # A2 Build Transparent Main Slider
                MainSlider_style: dict = {
                    "border_radius": 6, "font_size": 14, "draw_mode":ui.SliderDrawMode.HANDLE, 
                    "background_color":0x00000000, # 背景颜色 黑 （0XFF：100 0X00：透明）
                    "secondary_color":0xFFDDDDDD, "secondary_selected_color":0xFF696969, # HANDLE滑杆颜色，滑杆选中颜色
                    "color":0X00FFFFFF # 字体颜色
                    }
                MainSlider_max = 1
                MainSlider_min = 0
                MainSlider = ui.FloatSlider (min=MainSlider_min, max=MainSlider_max, height=20, style=MainSlider_style)
                SP_gol.set_sub_value("UI_All_Widgets", "Main_Slider", MainSlider)
                SP_gol.set_value("Max", MainSlider_max)
                SP_gol.set_value("Min", MainSlider_min)

        # B Set Main Functions 
        MainSlider.model.add_value_changed_fn(lambda m: set_main_functions(m.get_value_as_float()))

        def set_main_functions(value):
            # Test
            # print(value)
            SolarPanelPrimController()._control_timeline(offset_value=value)
            SolarPanelPrimController()._get_SolarPanels_RuntimeData_Fill_UI()
            return


    def _build_callback_widgets_functions(self):
        """Build Callback Functions for Some Other Widgets"""
        # A Set Callback Functions for Other Widgets
        SolarPanelPrimController()._set_all_status()
        Type = SP_gol.get_sub_value("UI_All_Widgets", "Type")
        Month = SP_gol.get_sub_value("UI_All_Widgets", "Month")
        Hour1 = SP_gol.get_sub_value("UI_All_Widgets", "Hour1")

        # A1 MainController Callback
        Type.model.add_value_changed_fn(lambda m: SolarPanelPrimController()._get_statu(Type, Month, Hour1))
        Month.model.add_value_changed_fn(lambda m: SolarPanelPrimController()._get_statu(Type, Month, Hour1))
        Hour1.model.add_value_changed_fn(lambda m: SolarPanelPrimController()._get_statu(Type, Month, Hour1))

        # A2 SunPath Callback
        # V1 Extension Delegate
        Month.model.add_value_changed_fn(lambda m: self.ChangeSceneFunction_time(Hour1.model, Month.model))
        Hour1.model.add_value_changed_fn(lambda m: self.ChangeSceneFunction_time(Hour1.model, Month.model))

        # V2 Class (Aborted)
        # Month.model.add_value_changed_fn(lambda m: ChangeScene().ChangeSceneFunction_time(Hour1.model, Month.model))
        # Hour1.model.add_value_changed_fn(lambda m: ChangeScene().ChangeSceneFunction_time(Hour1.model, Month.model))


        # B Set Other Individual Functions
        Color = SP_gol.get_sub_value("UI_All_Widgets", "Color")
        Reload = SP_gol.get_sub_value("UI_All_Widgets", "Reload")

        Color.set_clicked_fn(lambda b=True: SolarPanelPrimController()._set_color(b))
        Reload.set_clicked_fn(lambda b=True: SolarPanelPrimController()._update_model(b))

        return

        

    # Build Types of UI Widgets for the Window 
    def _build_labelled_floatfield(self, label:str, label_color:str, label_height, number_height, tooltip1:str = "Default Information", tooltip2:str = "Default Information"):
        with ui.ZStack(width=26, height=label_height):
            ui.Rectangle(name="box")
            ui.Label(label, alignment=ui.Alignment.CENTER, tooltip = tooltip1, style={"color":white})
        with ui.VStack():
            floatfiled =ui.FloatField(name="attribute_field", min=-99999999.9, max=99999999.9, height = number_height, tooltip=tooltip2)
        return floatfiled


    def _build_labelled_intfield(self, label:str, label_color:str, label_height, number_height, tooltip1:str = "Default Information", tooltip2:str = "Default Information"):
        with ui.ZStack(width=26, height=label_height):
            ui.Rectangle(name="box")
            ui.Label(label, alignment=ui.Alignment.CENTER, tooltip = tooltip1, style={"color":white})
        with ui.VStack():
            intfield =ui.IntField(name="attribute_field", min=-99999999, max=99999999, height = number_height, tooltip=tooltip2)
        return intfield


    def _build_floatfield(self, label:str, label_width, label_height, number_height, tooltip1:str = "Default Information", tooltip2:str = "Default Information"):
        with ui.HStack():
            ui.Label(label, name="attribute_name", width=label_width, height=label_height, tooltip=tooltip1)
            ui.Spacer(width=2)
            floatfield = ui.FloatField(name="attribute_field", min=-99999999.9, max=99999999.9, height=number_height, tooltip=tooltip2)
        return floatfield


    def _build_floatfield2(self, label:str, label_width, label_height, number_height, tooltip1:str = "Default Information", tooltip2:str = "Default Information"):
        with ui.HStack():
            ui.Spacer(width=2)
            with ui.VStack(width=label_width):
                ui.Spacer(height=2)
                ui.Label(label, name="attribute_name", width=label_width, height=label_height, tooltip=tooltip1)
            ui.Spacer(width=4)
            with ui.VStack():
                ui.Spacer(height=2.8)
                floatfield = ui.FloatField(name="attribute_field", min=-99999999.9, max=99999999.9, height=number_height, tooltip=tooltip2)
        return floatfield


    def _build_intfield(self, label:str, space:int, label_width, label_height, number_height, tooltip1:str = "Default Information", tooltip2:str = "Default Information"):
        with ui.HStack():
            ui.Label(label, name="attribute_name", width=label_width, height=label_height, tooltip=tooltip1)
            ui.Spacer(width=space)
            intfield = ui.IntField(name="attribute_field", min=-99999999, max=99999999, height=number_height, tooltip=tooltip2)
        return intfield
    

    def _build_intfield2(self, label:str, label_width, label_height, number_height, tooltip1:str = "Default Information", tooltip2:str = "Default Information"):
        with ui.HStack():
            ui.Spacer(width=4)
            with ui.VStack(width=label_width):
                ui.Spacer(height=1.5)
                ui.Label(label, name="attribute_name", width=label_width, height=label_height, tooltip=tooltip1)
            ui.Spacer(width=2)
            with ui.VStack():
                ui.Spacer(height=2.8)
                intfield = ui.IntField(name="attribute_field", min=-99999999, max=99999999, height=number_height, tooltip=tooltip2)
        return intfield


    def _build_intslider(self, label:str, label_width, label_height, tooltip1:str = "Default Information", tooltip2:str = "Default Information"):
        ui.Label(label, name="attribute_name", width =label_width, height = label_height, tooltip = tooltip1)
        intslider = ui.IntSlider(name="attribute_int", min=7, max=18, tooltip = tooltip2)
        return intslider


    def _build_button(self, label:str, button_width, button_height, tooltip:str = "Default Information"):
        button = ui.Button(label, name="tool_button", height=button_height, width=button_width, tooltip=tooltip)
        return button


    def _build_collapsable_header(self, collapsed, title):
        """Build a custom title of CollapsableFrame"""
        with ui.VStack():
            ui.Spacer(height=5)

            with ui.HStack():
                ui.Label(title, name="collapsable_name")
                if collapsed:
                    image_name = "collapsable_opened"
                else:
                    image_name = "collapsable_closed"
                ui.Image(name=image_name, width=10, height=10)

            ui.Spacer(height=5)
            ui.Line(style_type_name_override="HeaderLine")