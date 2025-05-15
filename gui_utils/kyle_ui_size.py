
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

# 获取屏幕尺寸
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()
# print(screen_width, screen_height)
# screen_width = 1920
# screen_height = 1080
screen_width = 2560
screen_height = 1440
print(screen_width, screen_height)

# 计算窗口大小和位置
# window_width = max(900, screen_width * 4 // 5)  # 4/5
# window_height = max(200, screen_height // 6)
window_width = screen_width * 4 // 5 # == 4/5
window_height = screen_height // 4
print( window_width, window_height)

# 计算位置， 保证窗口出现先中心偏下位置
x_position = (screen_width - window_width) // 2  # 256
y_position = (screen_height - window_height) * 5 // 6 #900
# x_position = (screen_width - window_width) // 8
# y_position = min((screen_height - window_height) * 5 // 6, screen_height - window_height - 50)
print(x_position, y_position)  # 256 900


#############################################################################################
############################# main two frames 的 size #######################################
#############################################################################################
# Horizontal direction: window_width = gap1 + frame1_width + gap2 + frame2_width(==350) + gap3
# vertical direction: window_height = gap4 + frame1_height + gap5
gap_window_frame = 5 # frame 和 window 之间的间隔 gap_window_frame = 5
gap_between_frames = 5 # frame之间的间隔 gap_between_frames = 5



################################################################################
################################################################################
text_frame1_w = window_width - (gap_window_frame + gap_between_frames + 350 + gap_window_frame)
text_frame1_h = window_height - (gap_window_frame + gap_window_frame)

text_frame2_w = 350
text_frame2_h = text_frame1_h

text_frame3_w = 150
text_frame3_h = text_frame1_h

################################################################################
################################################################################
frame1_place_x = gap_window_frame
frame1_place_y = gap_window_frame

frame2_place_x = frame1_place_x + text_frame1_w + gap_window_frame
frame2_place_y = gap_window_frame

frame3_place_x = frame1_place_x + + text_frame1_w + gap_window_frame
frame3_place_y = gap_window_frame
################################################################################
################################################################################
frame3_1_w = text_frame3_w-40
frame3_1_h = text_frame3_h-100 -70

frame3_1_place_x = gap_window_frame
frame3_1_place_y = gap_window_frame

button_AIchat_w = text_frame3_w-10
button_AIchat_h = ((text_frame3_h - frame3_1_h - gap_window_frame*2 -60) )//2

button_AIchat_place_x = gap_window_frame
button_AIchat_place_y = gap_window_frame + frame3_1_h + gap_window_frame + 50


button_more_w = text_frame3_w-10
button_more_h = button_AIchat_h

button_more_place_x = gap_window_frame
button_more_place_y = button_AIchat_place_y + button_AIchat_h + gap_window_frame

################################################################################
################################################################################



# 创建外部 Frame1

# 在 customtkinter（CTk）中，不能把 width 和 height 参数传给 .place(...)，而是要在创建控件的时候就指定这两个属性。
############################################################################
######################### frame1 ###########################################
############################################################################
gap_frame1_textbox = 5
scrollbar_text_width = 25

textbox_w = text_frame1_w - (gap_frame1_textbox + gap_frame1_textbox + scrollbar_text_width)  # scrollbar_text_width==25 是滚动条的width
textbox_h = text_frame1_h - (gap_frame1_textbox + gap_frame1_textbox )







############################################################################
######################### frame2 #### width=350 ############################
############################################################################

gap_frame_widgets= 5

label_arrows_width = 40
label_arrows_height = 60

option_menu_width = 140
option_menu_height = 50

label_place_x = gap_frame_widgets*2 + option_menu_width + gap_frame_widgets

option_menu_1_place_x = gap_frame_widgets*2
option_menu_1_place_y = gap_frame_widgets

option_menu_2_place_x = gap_frame_widgets*2 + option_menu_width + gap_frame_widgets + label_arrows_width + gap_frame_widgets
option_menu_2_place_y = gap_frame_widgets


####################################################################################33
tabview_w = 350 - gap_frame_widgets*2 - gap_frame_widgets*2 #330
tabview_h = 220

tabview_place_x = gap_frame_widgets*2
tabview_place_y = gap_frame_widgets + min(label_arrows_height,option_menu_height) + gap_frame_widgets

segemented_button_w = tabview_w
segemented_button_h = tabview_place_y

segemented_button_place_x = tabview_place_x
segemented_button_place_y = tabview_place_y + tabview_h + gap_frame_widgets



frame2_1_w = tabview_w - gap_frame_widgets*2 #320
frame2_1_y = 160
Model_tab_scroll_frame_w = 280



frame2_2_w = tabview_w - gap_frame_widgets*2
frame2_2_y = 160

Audio_tab_scrollframe_w = Model_tab_scroll_frame_w



frame2_3_w = tabview_w - gap_frame_widgets*2
frame2_3_y = 160

Theme_tab_scrollframe_w =Model_tab_scroll_frame_w


####################################################################################33















############################################################################
######################### frame3 #### width=350 ############################
############################################################################

