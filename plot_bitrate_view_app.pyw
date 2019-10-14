# coding=gbk
from   Tkinter import *
import tkFont
from   tkFileDialog import *
import ttk
import codecs
from tool import *

button_relief = 'solid'   # button looks
text_relief   = 'solid'
lt_ipady      = 8         # ipady for Label and Text
wid_sticky    = W+E+N+S
msg_key_idx   = 0
msg_value_idx = 1

class APPPlotBitRateViewTool():
    def openSourceFileDialog(self):
        org_file_dir = os.path.dirname(self.t_source.get('0.0', END)[0:-1])
        options = {}
        options['initialdir'] = org_file_dir
        src_path = askopenfilename(**options)
        if src_path != "":
            self.t_source.delete('0.0', END)        # clear contents first
            self.t_source.insert('0.0', src_path)

    def openOutputFileDialog(self):
        org_file_dir = os.path.dirname(self.t_output.get('0.0', END)[0:-1])
        options = {}
        options['initialdir'] = org_file_dir
        file_path = asksaveasfilename(initialfile="plot.pdf", defaultextension=".pdf")
        if file_path != "":
            self.t_output.delete('0.0', END)        # clear contents first
            self.t_output.insert('0.0', file_path)

    def checkHistory(self):  # fill texts with history values if exists
        if CheckFile(".history"):
            f_history   = open(".history", "r")
            source_file = f_history.readline()[8:-1]
            output_file = f_history.readline()[8:-1]
            enc_id      = f_history.readline()[8:-1]
            frame_rate  = f_history.readline()[8:-1]
            check_interval  = f_history.readline()[8:-1]
            vbv_bufsize = f_history.readline()[8:-1]
            vbv_bitrate = f_history.readline()[8:-1]
            vbv_initime = f_history.readline()[8:-1]
            self.t_source.insert('0.0', source_file)
            self.t_output.insert('0.0', output_file)
            self.t_enc_id.insert('0.0', enc_id)
            self.t_frame_rate.insert('0.0', frame_rate)
            self.t_interval.insert('0.0', check_interval)
            self.t_vbv_bufsize.insert('0.0', vbv_bufsize)
            self.t_vbv_max_bitrate.insert('0.0', vbv_bitrate)
            self.t_vbv_init_time.insert('0.0', vbv_initime)
        else:
            self.t_source.insert('0.0', r"D:/input.log")
            self.t_output.insert('0.0', r"D:/output.img")
            self.t_enc_id.insert('0.0', "")
            self.t_frame_rate.insert('0.0', "25")
            self.t_interval.insert('0.0', "1")
            self.t_vbv_bufsize.insert('0.0',     "1000")
            self.t_vbv_max_bitrate.insert('0.0', "1000")
            self.t_vbv_init_time.insert('0.0',   "1000")

    def saveHistory(self):
        f_history = codecs.open(".history", 'w', 'utf-8')   # write 中文内容
        f_history.write(u"Source: %s\n"%self.t_source.get('0.0', END)[0:-1])
        f_history.write(u"Output: %s\n"%self.t_output.get('0.0', END)[0:-1])
        f_history.write(u"encid : %s\n"%self.t_enc_id.get('0.0', END)[0:-1])
        f_history.write(u"frate : %s\n"%self.t_frame_rate.get('0.0', END)[0:-1])
        f_history.write(u"intval: %s\n"%self.t_interval.get('0.0', END)[0:-1])
        f_history.write(u"vbvbfs: %s\n"%self.t_vbv_bufsize.get('0.0', END)[0:-1])
        f_history.write(u"vbvbtr: %s\n"%self.t_vbv_max_bitrate.get('0.0', END)[0:-1])
        f_history.write(u"vbvint: %s\n"%self.t_vbv_init_time.get('0.0', END)[0:-1])
        f_history.close()

    def updateOptionFrame(self, var):
        if self.str_log_type.get() == u'hm_log' or self.str_log_type.get() == u'ashevc_log':
            self.l_frame_rate.grid(row = 1, column = 1, padx = 2, pady = 3)
            self.t_frame_rate.grid(row = 1, column = 2, padx = 5, pady = 3)
            if self.str_plot_type.get() == u'vbvbuffer view':
                self.l_interval.grid_remove()
                self.t_interval.grid_remove()
                self.l_vbv_bufsize.grid(row = 1, column = 3, padx = 5, pady = 3)
                self.t_vbv_bufsize.grid(row = 1, column = 4, padx = 5, pady = 3)
                self.l_vbv_max_bitrate.grid(row = 2, column = 1, padx = 5, pady = 3)
                self.t_vbv_max_bitrate.grid(row = 2, column = 2, padx = 5, pady = 3)
                self.l_vbv_init_time.grid(row = 2, column = 3, padx = 5, pady = 3)
                self.t_vbv_init_time.grid(row = 2, column = 4, padx = 5, pady = 3)
            else:
                self.l_interval.config(text=u'check interval\n(frames)')
                self.l_interval.grid(row = 1, column = 3, padx = 2, pady = 3)
                self.t_interval.grid(row = 1, column = 4, padx = 5, pady = 3)
                self.l_vbv_init_time.grid_remove()
                self.t_vbv_init_time.grid_remove()
                self.l_vbv_max_bitrate.grid_remove()
                self.t_vbv_max_bitrate.grid_remove()
                self.l_vbv_bufsize.grid_remove()
                self.t_vbv_bufsize.grid_remove()
        elif self.str_log_type.get() == u'arcvideo_log':
            self.l_enc_id.grid(row = 1, column = 1, padx = 2, pady = 3)
            self.t_enc_id.grid(row = 1, column = 2, padx = 15, pady = 3)
            self.l_frame_rate.grid(row = 1, column = 3, padx = 2, pady = 3)
            self.t_frame_rate.grid(row = 1, column = 4, padx = 5, pady = 3)
            self.l_interval.config(text=u'check interval\n(seconds)')
            self.l_interval.grid(row = 2, column = 1, padx = 2, pady = 3)
            self.t_interval.grid(row = 2, column = 2, padx = 5, pady = 3)
            if self.str_plot_type.get() == u'vbvbuffer view':
                self.l_vbv_bufsize.grid(row = 3, column = 1, padx = 5, pady = 3)
                self.t_vbv_bufsize.grid(row = 3, column = 2, padx = 5, pady = 3)
                self.l_vbv_max_bitrate.grid(row = 3, column = 3, padx = 5, pady = 3)
                self.t_vbv_max_bitrate.grid(row = 3, column = 4, padx = 5, pady = 3)
                self.l_vbv_init_time.grid(row = 4, column = 1, padx = 5, pady = 3)
                self.t_vbv_init_time.grid(row = 4, column = 2, padx = 5, pady = 3)
            else:
                self.l_vbv_init_time.grid_remove()
                self.t_vbv_init_time.grid_remove()
                self.l_vbv_max_bitrate.grid_remove()
                self.t_vbv_max_bitrate.grid_remove()
                self.l_vbv_bufsize.grid_remove()
                self.t_vbv_bufsize.grid_remove()

    def __init__(self, master):
        self.font = tkFont.Font(family="Courier", size=9)

        ##### Define Main Frames
        self.OpenFileFrame = LabelFrame(master, text=u"选择文件", padx = 5, pady = 5)
        self.OpenFileFrame.grid(row = 0, column = 0, columnspan = 2, sticky = W+E+N+S, padx = 5, pady = 5)
        self.OptionsFrame = LabelFrame(master, text="Options", padx = 5, pady = 5)
        self.OptionsFrame.grid(row = 1, column = 0, sticky = W+E+N+S, padx = 5, pady = 5)
        self.OperationsFrame = LabelFrame(master, padx = 0, pady = 5)
        self.OperationsFrame.grid(row = 2, column = 0, sticky = W+E+N+S, padx = 5, pady = 5)

        ##### Define widgets within OpenFileFrame
        self.l_source  = Label (self.OpenFileFrame, text=u'source log', fg='red')
        self.l_output  = Label (self.OpenFileFrame, text=u'output img', fg='blue')
        self.t_source  = Text  (self.OpenFileFrame, height = 2, width = 45, relief = text_relief, fg='red', font=self.font)
        self.t_output  = Text  (self.OpenFileFrame, height = 2, width = 45, relief = text_relief, fg='blue', font=self.font)
        self.b_source  = Button(self.OpenFileFrame, text=u'Open   ', relief=button_relief, command=lambda: self.openSourceFileDialog())
        self.b_output  = Button(self.OpenFileFrame, text=u'Save As', relief=button_relief, command=lambda: self.openOutputFileDialog())

        ##### Define widgets within OptionsFrame
        self.l_plot_type = Label(self.OptionsFrame, text=u'      plot type', fg='blue')
        self.str_plot_type = StringVar()
        self.str_plot_type.set(u'bitrate viewer')
        self.o_plot_type = OptionMenu(self.OptionsFrame, self.str_plot_type, u'bitrate   view', u'vbvbuffer view', command=self.updateOptionFrame) # set update function to update UI
        self.l_vbv_init_time = Label(self.OptionsFrame, text=u'vbv_init_time\n(ms)', fg='blue')
        self.t_vbv_init_time = Text (self.OptionsFrame, height = 1, width = 15, relief = text_relief, fg='blue', font=self.font)
        self.l_vbv_max_bitrate = Label(self.OptionsFrame, text=u'vbv_bitrate\n(kbps)', fg='blue')
        self.t_vbv_max_bitrate = Text (self.OptionsFrame, height = 1, width = 15, relief = text_relief, fg='blue', font=self.font)
        self.l_vbv_bufsize = Label(self.OptionsFrame, text=u'vbv_bufsize\n(kbits)', fg='blue')
        self.t_vbv_bufsize = Text (self.OptionsFrame, height = 1, width = 15, relief = text_relief, fg='blue', font=self.font)

        self.l_log_type = Label(self.OptionsFrame, text=u'      log type', fg='blue')
        self.str_log_type = StringVar()
        self.str_log_type.set(u'hm_log')
        self.o_log_type = OptionMenu(self.OptionsFrame, self.str_log_type, u'hm_log', u'ashevc_log', u'arcvideo_log', command=self.updateOptionFrame) # set update function to update UI
        self.l_enc_id = Label(self.OptionsFrame, text=u'    enc id', fg='blue')
        self.t_enc_id = Text (self.OptionsFrame, height = 1, width = 15, relief = text_relief, fg='blue', font=self.font)
        self.l_frame_rate = Label(self.OptionsFrame, text=u'    frame rate', fg='blue')
        self.t_frame_rate = Text (self.OptionsFrame, height = 1, width = 15, relief = text_relief, fg='blue', font=self.font)
        self.l_interval   = Label(self.OptionsFrame, text=u'check interval\n(seconds)', fg='blue')
        self.t_interval   = Text (self.OptionsFrame, height = 1, width = 15, relief = text_relief, fg='blue', font=self.font)

        ##### Place widgets within OpenFileFrame
        self.l_source.grid (row = 0, column = 0, padx = 5, pady = 5, sticky = wid_sticky, ipady = lt_ipady)
        self.t_source.grid (row = 0, column = 1, padx = 5, pady = 5, sticky = wid_sticky, ipady = lt_ipady)
        self.b_source.grid (row = 0, column = 2, padx = 5, pady = 5, ipady = 1)
        self.l_output.grid (row = 1, column = 0, padx = 5, pady = 5, sticky = wid_sticky, ipady = lt_ipady)
        self.t_output.grid (row = 1, column = 1, padx = 5, pady = 5, sticky = wid_sticky, ipady = lt_ipady)
        self.b_output.grid (row = 1, column = 2, padx = 5, pady = 5, ipady = 1)

        ##### Place widgets within OptionFrame
        self.l_log_type.grid(row = 0, column = 1, padx = 2, pady = 3)
        self.o_log_type.grid(row = 0, column = 2, padx = 2, pady = 3)
        self.l_plot_type.grid(row = 0, column = 3, padx = 2, pady = 3)
        self.o_plot_type.grid(row = 0, column = 4, padx = 2, pady = 3)
        self.updateOptionFrame(self.str_log_type.get()) # update detailed options

        ##### Place widgets within OperationsFrame
        self.progressbar = ttk.Progressbar(self.OperationsFrame, orient=HORIZONTAL, length = 380, mode='determinate')
        self.progressbar.grid(row = 0, column = 1, columnspan = 2, ipady = lt_ipady, sticky = W+E+N+S, padx = 4, pady = 5)
        self.progress = 0
        self.b_Collect = Button(self.OperationsFrame, relief=button_relief, bg='green', text = u'Start Plot', width = 10, command=self.StartPlotThread)
        self.b_Collect.grid (row = 0, column = 0, ipady = 1, padx = 2, pady = 3)
        self.checkHistory()

    def StartPlotThread(self):
        source_file = self.t_source.get('0.0', END)[0:-1]
        output_file = self.t_output.get('0.0', END)[0:-1]
        self.saveHistory()
        enc_id = self.t_enc_id.get('0.0', END)[0:-1]
        frame_rate  = (int)(self.t_frame_rate.get('0.0', END)[0:-1])
        check_interval = (float)(self.t_interval.get('0.0', END)[0:-1])
        vbv_init_time  = (int)(self.t_vbv_init_time.get('0.0', END)[0:-1])
        init_frames    = (int)(vbv_init_time * frame_rate / 1000.0)
        vbv_bitrate    = 1000 * (int)(self.t_vbv_max_bitrate.get('0.0', END)[0:-1])
        vbv_bufsize    = 1000 * (int)(self.t_vbv_bufsize.get('0.0', END)[0:-1])
        self.progressbar['value'] = 100.0
        xlabel_type = 0

        if self.str_log_type.get() == u'hm_log' or self.str_log_type.get() == u'ashevc_log':
            xlabel_type = 0
            if self.str_plot_type.get() == u'bitrate   view':
                time_array, bitrate_array = extract_hm_ashevc_bitrate(source_file, frame_rate, check_interval)
                plot_arrays(time_array, bitrate_array, output_file, check_interval, xlabel_type)
            elif self.str_plot_type.get() == u'vbvbuffer view':
                time_array, vbv_array = extract_hm_ashevc_vbvinfo(source_file, frame_rate, vbv_init_time, vbv_bitrate)
                plot_vbv_arrays(time_array, vbv_array, output_file, vbv_bufsize, init_frames)
        elif self.str_log_type.get() == u'arcvideo_log':
            xlabel_type = 1
            time_array, bitrate_array = extract_bitrate(source_file, enc_id, frame_rate, check_interval)
            plot_arrays(time_array, bitrate_array, output_file, check_interval, xlabel_type)

if __name__ == "__main__":
    root = Tk()
    root.title(u'Hevc Bitrate Viewer Based on python')
    root.resizable(0, 0) # can't resize
    root.rowconfigure   (0, weight=1)
    root.columnconfigure(0, weight=1)
    APPPlotBitRateViewTool(root)
    root.mainloop()