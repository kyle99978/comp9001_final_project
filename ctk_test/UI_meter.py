import psutil,time,threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
root = ttk.Window()
ttk.Meter(
        master=root,
        bootstyle=DEFAULT,
        metertype="semi",#将仪表显示为:full 是整圆，semi 是半圆
        wedgesize=5, #设置弧周围的指示器楔形长度,如果大于 0，则此楔形设置为以当前仪表值为中心的指示器
        amounttotal=50, #仪表的最大值，默认100
        amountused=10, #仪表的当前值
        metersize=200,#仪表大小
        showtext=True, #指示是否在仪表上显示左、中、右文本标签
        interactive=True, #是否可以手动调节数字的大小
        textleft='左边', #插入到中心文本左侧的短字符串
        textright='右边',
        textfont="-size 30", #中间数字大小
        subtext="文本",
        subtextstyle=DEFAULT,
        subtextfont="-size 20",#文本大小
        ).pack(side=ttk.LEFT, padx=5)
# def _():
#         meter = ttk.Meter(
#                 metersize=180,
#                 padding=50,
#                 amountused=0,
#                 metertype="semi",
#                 subtext="当前网速(kB/s)",
#                 subtextstyle="warning",
#                 interactive=False,
#                 bootstyle='primary',
#                 )
#         meter.pack(side=ttk.LEFT, padx=5)
#         while True:
#                 meter.configure(amountused=round(getNet(),2))
# def getNet():
#     recv_before = psutil.net_io_counters().bytes_recv
#     time.sleep(1)
#     recv_now = psutil.net_io_counters().bytes_recv
#     recv = (recv_now - recv_before)/1024
#     return recv
# #
# # t = threading.Thread(target=_)
# t.start()
root.mainloop()
