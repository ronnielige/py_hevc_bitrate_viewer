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
            self.t_source.insert('0.0', source_file)
            self.t_output.insert('0.0', output_file)
            self.t_enc_id.insert('0.0', enc_id)
            self.t_frame_rate.insert('0.0', frame_rate)
            self.t_interval.insert('0.0', check_interval)
        else:
            self.t_source.insert('0.0', r"D:/input.log")
            self.t_output.insert('0.0', r"D:/output.img")
            self.t_enc_id.insert('0.0', "")
            self.t_frame_rate.insert('0.0', "25")
            self.t_interval.insert('0.0', "1")

    def saveHistory(self):
        f_history = codecs.open(".history", 'w', 'utf-8')   # write 中文内容
        f_history.write(u"Source: %s\n"%self.t_source.get('0.0', END)[0:-1])
        f_history.write(u"Output: %s\n"%self.t_output.get('0.0', END)[0:-1])
        f_history.write(u"encid : %s\n"%self.t_enc_id.get('0.0', END)[0:-1])
        f_history.write(u"frate : %s\n"%self.t_frame_rate.get('0.0', END)[0:-1])
        f_history.write(u"intval: %s\n"%self.t_interval.get('0.0', END)[0:-1])
        f_history.close()

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
        self.t_source  = Text  (self.OpenFileFrame, height = 1, width = 45, relief = text_relief, fg='red', font=self.font)
        self.t_output  = Text  (self.OpenFileFrame, height = 1, width = 45, relief = text_relief, fg='blue', font=self.font)
        self.b_source  = Button(self.OpenFileFrame, text=u'Open   ', relief=button_relief, command=lambda: self.openSourceFileDialog())
        self.b_output  = Button(self.OpenFileFrame, text=u'Save As', relief=button_relief, command=lambda: self.openOutputFileDialog())

        ##### Define widgets within OptionsFrame
        self.l_enc_id = Label(self.OptionsFrame, text=u'          enc id', fg='blue')
        self.t_enc_id = Text (self.OptionsFrame, height = 1, width = 15, relief = text_relief, fg='blue', font=self.font)
        self.l_frame_rate = Label(self.OptionsFrame, text=u'      frame rate', fg='blue')
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
        self.l_enc_id.grid(row = 0, column = 1, padx = 2, pady = 3)
        self.t_enc_id.grid(row = 0, column = 2, padx = 15, pady = 3)
        self.l_frame_rate.grid(row = 0, column = 3, padx = 2, pady = 3)
        self.t_frame_rate.grid(row = 0, column = 4, padx = 5, pady = 3)
        self.l_interval.grid(row = 1, column = 1, padx = 2, pady = 3)
        self.t_interval.grid(row = 1, column = 2, padx = 5, pady = 3)

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

        self.progressbar['value'] = 100.0

        time_array, bitrate_array = extract_bitrate(source_file, enc_id, frame_rate, check_interval)
        plot_arrays(time_array, bitrate_array, output_file, check_interval)


if __name__ == "__main__":
    root = Tk()
    root.title(u'Hevc Bitrate Viewer Based on python')
    root.resizable(0, 0) # can't resize
    root.rowconfigure   (0, weight=1)
    root.columnconfigure(0, weight=1)
    APPPlotBitRateViewTool(root)
    root.mainloop()