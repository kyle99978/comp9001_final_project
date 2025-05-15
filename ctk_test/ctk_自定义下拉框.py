import customtkinter as ctk
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass
# 禁用 DPI 自动适配（一般不建议），是否使用系统 DPI 缩放设置（比如 125%、150%）来自动放大界面
ctk.deactivate_automatic_dpi_awareness()

class CustomDropdown(ctk.CTkFrame):
    def __init__(self, master, options,
                 mainbutton_width=200, mainbutton_height=50, mainbutton_corner_radius=0,
                 mainbutton_place_x=0,
                 mainbutton_place_y=0,
                 mainbutton_place_anchor="nw",
                 mainbutton_border_width=0, mainbutton_border_spacing=4,
                 mainbutton_fg_color=("#3B8ED0", "#1F6AA5"),
                 mainbutton_hover_color=("#36719F", "#144870"),
                 mainbutton_border_color=("#DADADA", "#444444"),
                 mainbutton_text_color=("#000000", "#FFFFFF"),
                 mainbutton_text_color_disabled=("#A6A6A6", "#666666"),
                 mainbutton_text="Choose an option",
                 mainbutton_font=("Arial", -14),
                 mainbutton_textvariable=None,
                 mainbutton_image=None,
                 mainbutton_state="normal",
                 mainbutton_hover=True,
                 mainbutton_command=None,
                 mainbutton_compound="left",
                 mainbutton_anchor="center",

                 optionframe_width_max=300,
                 optionframe_height_max=250,
                 optionframe_corner_radius=10,
                 optionframe_border_width=0,
                 optionframe_border_color=("#DADADA", "#444444"),
                 optionframe_fg_color=("#F0F0F0", "#2B2B2B"),

                 optionbutton_text_color=("#000000", "#FFFFFF"),
                 optionbutton_font=("Arial", 12),
                 optionbutton_command=None,
                 optionbutton_fg_color=("#F0F0F0", "#2B2B2B"),
                 optionbutton_bg_color=("#F0F0F0", "#2B2B2B"),
                 optionbutton_corner_radius=10,
                 optionbutton_hover_color=("#36719F", "#144870"),
                 **kwargs):
        super().__init__(master, **kwargs)

        self.master = master
        self.options = options
        self.optionframe = ctk.CTkScrollableFrame(
            master=self.master,
            width=optionframe_width_max,
            height=optionframe_height_max,
            fg_color=optionframe_fg_color,
            corner_radius=optionframe_corner_radius,
            border_color=optionframe_border_color,
            border_width=optionframe_border_width,
            )

        self.mainbutton = ctk.CTkButton(
            master=self.master,
            width=mainbutton_width,
            height=mainbutton_height,
            corner_radius=mainbutton_corner_radius,
            border_width=mainbutton_border_width,
            fg_color=mainbutton_fg_color,
            hover=mainbutton_hover,
            hover_color=mainbutton_hover_color,
            border_color=mainbutton_border_color,
            text_color=mainbutton_text_color,
            text_color_disabled=mainbutton_text_color_disabled,
            text=mainbutton_text,
            font=mainbutton_font,
            textvariable=mainbutton_textvariable,
            image=mainbutton_image,
            state=mainbutton_state,
            command=self.create_optionframe,
            compound=mainbutton_compound,
            anchor=mainbutton_anchor,
        )
        self.mainbutton.place(x=mainbutton_place_x, y=mainbutton_place_y, anchor=mainbutton_place_anchor)

        # add optionbutton parameters
        self.optionframe_corner_radius = optionframe_corner_radius
        self.optionframe_fg_color = optionframe_fg_color
        self.optionframe_border_color = optionframe_border_color
        self.optionframe_border_width = optionframe_border_width
        self.optionbutton_corner_radius = optionbutton_corner_radius
        self.optionbutton_text_color = optionbutton_text_color
        self.optionbutton_font = optionbutton_font
        self.optionbutton_fg_color = optionbutton_fg_color
        self.optionbutton_hover_color = optionbutton_hover_color
        self.optionbutton_bg_color = optionbutton_bg_color

        self.dropdown_open=False

        for option in self.options:
            option_button = ctk.CTkButton(
                self.optionframe,
                text=option,
                command=lambda: self.select_option(option=option),
                corner_radius=self.optionbutton_corner_radius,
                font=self.optionbutton_font,
                fg_color=self.optionbutton_fg_color,
                hover_color=self.optionbutton_hover_color,
                text_color=self.optionbutton_text_color,
                bg_color=self.optionbutton_bg_color,
            )
            option_button.pack(fill="x", padx=0, pady=0)

        print("[Init] UI setup complete.")



    def create_optionframe(self):
        print("[Toggle] Main button clicked.")
        if self.dropdown_open:
            print("[Toggle] Dropdown is open → Hiding.")
            self.optionframe.place_forget()  # 藏起来
            self.dropdown_open = False
            self.master.unbind_all("<Button-1>")
        else: # show
            print("[Toggle] Dropdown is closed → Showing.")
             # 右下角坐标 right bottom  # widget.winfo_xy()返回控件左上角的横坐标（相对于父容器）
            # 获取主按钮在屏幕上的绝对位置（左上角） 
            #     ctypes.windll.shcore.SetProcessDpiAwareness(1)
            # #禁用 DPI 自动适配（一般不建议），是否使用系统 DPI 缩放设置（比如 125%、150%）来自动放大界面
            # ctk.deactivate_automatic_dpi_awareness()
            relative_x = self.mainbutton.winfo_x() # + self.mainbutton.winfo_width()
            relative_y = self.mainbutton.winfo_y() + self.mainbutton.winfo_height()
            self.optionframe.place(x=relative_x, y=relative_y,anchor="nw" )

            self.master.bind_all("<Button-1>", self._on_global_click, add="+")  # 全局监听点击事件的方式
            self.dropdown_open = True


    def select_option(self, option):
        self.mainbutton.configure(text=option)
        self.optionframe.place_forget()
        self.dropdown_open = False
        self.master.unbind_all("<Button-1>")


    def _on_global_click(self, event):
        self.optionframe.place_forget()
        self.dropdown_open = False
        self.master.unbind_all("<Button-1>")


if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("500x200")

    dropdown = CustomDropdown(
        master=app,
        options=[f"Option {i}" for i in range(1, 11)],
        mainbutton_text="Dropdown Button",
        mainbutton_place_x=10,
        mainbutton_place_y=10,
        mainbutton_place_anchor="nw",
    )


    app.mainloop()

