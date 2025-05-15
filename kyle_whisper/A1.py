import tkinter as tk
from tkinter import font
import os  # 用于检查文件是否存在

# 创建主窗口
root = tk.Tk()
root.title("DUAN_translating")

# 检查并设置窗口图标
icon_path = "img/plane.ico"
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

# 设置窗口属性
root.attributes('-alpha', 0.85)  # 设置透明度
root.attributes('-topmost', 1)  # 置顶窗口

# 获取屏幕尺寸
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()

# 计算窗口大小和位置
window_width = max(600, screen_width * 4 // 5)  # 4/5
window_height = max(200, screen_height // 6)
x_position = (screen_width - window_width) // 2
y_position = min((screen_height - window_height) * 5 // 6, screen_height - window_height - 50)

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
root.config(bg='black')
root.resizable(False, False)
root.minsize(window_width, window_height)

# 创建文本框的外部Frame
text_frame = tk.Frame(root, bg='blue')
text_frame_w,text_frame_h = window_width - 350,window_height -10
text_frame.place(x=5, y=5, width=text_frame_w, height= text_frame_h)

# 创建字体
custom_font = font.Font(family="Times New Roman", size=16)

# 创建Text小部件，并启用水平 & 垂直滚动
text_box = tk.Text(text_frame, bg='black', fg='white', insertbackground='white', bd=0, width=40, height=10,
                   font=custom_font,wrap="none" )  #  允许水平滚动
text_box.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

# 创建垂直滚动条，并绑定到Text
y_scrollbar = tk.Scrollbar(text_box, orient=tk.VERTICAL, command=text_box.yview, width=20, bg='black', cursor='hand2')
y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_box.config(yscrollcommand=y_scrollbar.set)  # 让Text同步滚动条

# 创建水平滚动条，并绑定到Text
x_scrollbar = tk.Scrollbar(text_box, orient=tk.HORIZONTAL, command=text_box.xview, width=20, bg='black', cursor='hand2')
x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
text_box.config(xscrollcommand=x_scrollbar.set)  # 让Text同步滚动条

####################################################################################################
##############################################################################################################
fun_frame = tk.Frame(root, bg='black')
fun_frame.place(x=5 + text_frame_w + 5, y=5, width= 340, height= window_height -10)

frame_cbs = tk.Frame(fun_frame, bg='Wheat')
frame_cbs.place(x=10, y=5,width=310, height=50)

def on_checkbutton_click():
    selected_options = [var1.get(), var2.get(), var3.get(), var4.get()]
    print(f"选中的选项: {selected_options}")




# 创建四个复选框的变量
var1 = tk.IntVar(value=1)  # 默认选中第一个复选框
var2 = tk.IntVar(value=0)
var3 = tk.IntVar(value=0)
var4 = tk.IntVar(value=0)
# 创建并放置复选框
checkbutton1 = tk.Checkbutton(frame_cbs, text="RECG", variable=var1, command=on_checkbutton_click,) # bg='black',fg='red',activebackground='black',activeforeground='red'
checkbutton1.place(x=0, y=5,width=70, height=40)

checkbutton2 = tk.Checkbutton(frame_cbs, text="TRANS", variable=var2, command=on_checkbutton_click)
checkbutton2.place(x=80, y=5,width=70, height=40)

checkbutton3 = tk.Checkbutton(frame_cbs, text="SAVE", variable=var3, command=on_checkbutton_click)
checkbutton3.place(x=160, y=5,width=70, height=40)

checkbutton4 = tk.Checkbutton(frame_cbs, text="REVISE", variable=var4, command=on_checkbutton_click)
checkbutton4.place(x=240, y=5,width=70, height=40)


##############################################################################################################
##############################################################################################################
frame_content = tk.Frame(fun_frame, bg='LightCyan')
frame_content.place(x=10, y=65,width=150, height=120)
index_move_content = ""
def b_up_click():
    index_move_content = "up"

def b_down_click():
    index_move_content = "down"

def b_top_click():
    index_move_content = "top"

def b_bottom_click():
    index_move_content = "bottom"


b_up = tk.Button(frame_content, text='Up', command=b_up_click)
b_up.place(x=10, y=10, width=60, height=45)

b_down = tk.Button(frame_content, text='Down', command=b_down_click)
b_down.place(x=10, y=65, width=60, height=45)

b_top = tk.Button(frame_content, text='Top', command=b_top_click)
b_top.place(x=80, y=10, width=60, height=45)

b_bottom = tk.Button(frame_content, text='Bottom', command=b_bottom_click)
b_bottom.place(x=80, y=65, width=60, height=45)


##############################################################################################################
##############################################################################################################
frame_setting = tk.Frame(fun_frame, bg='#7FFFAA')
frame_setting.place(x=170, y=65,width=150, height=120)

b_stop_re = tk.Button(frame_setting, text='开始/暂停', command="pass")
b_stop_re.place(x=10, y=65, width=60, height=50)

b_quit = tk.Button(frame_setting, text='退出程序', command="pass")
b_quit.place(x=75, y=65, width=60, height=50)


options = ["None", "音频文件", "视频文件", "实时-设备音响1", "实时-设备音响2", "实时-设备麦克风1", "实时-设备麦克风2"]
def op(frame_setting, options):
    def show_selection(selection):
        print(f"You selected: {selection}")
    # 创建一个OptionMenu
    # options = ["None", "音频文件", "视频文件", "实时-设备音响1", "实时-设备音响2", "实时-设备麦克风1",
    #            "实时-设备麦克风2"]
    # 创建一个变量来存储选择的值
    selected_input = tk.StringVar() # (root)  # 它的作用是 创建一个字符串变量，并将其与 root 窗口绑定
    selected_input.set("None")  # 设置默认值

    b_input = tk.OptionMenu(frame_setting, selected_input, *options, command=show_selection)
    '''
    在 tk.OptionMenu 中，command=show_selection 绑定了一个回调函数 show_selection。
    当用户在 OptionMenu 里选择一个新选项时，Tkinter 会自动将选中的值作为参数传递给 show_selection(selection)。
    '''
    b_input.place(x=10, y=10, width=135, height=50)

op(frame_setting,options)

root.mainloop()
