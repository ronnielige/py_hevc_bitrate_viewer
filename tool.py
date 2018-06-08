
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import os

def extract_bitrate(inf_name, enc_id, frame_rate, check_interval):
    bitrate_array = []
    inf        = open(inf_name, 'r')
    line       = inf.readline()
    frame_idx  = 0
    accum_bits = 0
    bitrate_array = []
    time_array    = []
    interval_frms = check_interval * frame_rate
    while line:
        try:
            line = line.encode("UTF-8")
        except Exception, e:
            line = inf.readline()
            print "line %s transcoder to utf-8 error"%line
            continue

        enc_id_pos = line.find("%s::DELIVER:ThreadID"%enc_id)
        if enc_id_pos >= 0:
            len_pos = line.find("length")
            if len_pos < 0:
                print "Encounter an abnormal line: %s, can't find length"%(line[:-1])
                line = inf.readline()
                continue

            frame_bits = (int)(line[len_pos:].split()[2]) * 8
            accum_bits = accum_bits + frame_bits
            frame_idx  = frame_idx + 1
            if frame_idx % interval_frms == 0:  # accumalated 1 seconds
                bitrate_array.append(accum_bits / check_interval / 1000)
                time_array.append(frame_idx / frame_rate)
                accum_bits = 0

        line = inf.readline()

    return time_array, bitrate_array

def plot_arrays(time_array, bitrate_array, out_img, bitrate_interval):
    font_set = FontProperties(fname=r"c:\windows\fonts\calibri.ttf", size=15)
    category_f0 = plt.figure(0, figsize=(20, 10))
    fileformat  = os.path.splitext(out_img)[1][1:]
    avg_bitrate = sum(bitrate_array) / len(bitrate_array)
    avg_br_arr  = [avg_bitrate, ] * len(bitrate_array)
    max_bitrate = max(bitrate_array)
    max_avg_rat = (float)(max_bitrate) / avg_bitrate
    plt.ylim(0, max(bitrate_array) * 1.5)
    plt.plot(time_array, bitrate_array, marker='+')
    plt.plot(time_array, avg_br_arr)
    plt.xlabel("time(second)", fontproperties=font_set, fontsize = 14)
    plt.ylabel("bitrate(kbp/s)", fontproperties=font_set, fontsize = 14)
    plt.title("Bitrate interval %d seconds\n Average, Maximum bitrate = %d kbps, %d kbps\n max / avg = %4.2f"%(bitrate_interval, avg_bitrate, max_bitrate, max_avg_rat), fontproperties=font_set, fontsize = 12)
    plt.grid(True)

    #for cat_value in category_array:
    #    cat_idx = category_array.index(cat_value)
    #    ax      = plt.subplot(2, 2, cat_idx + 1)
    #    plt.xlabel(x_title, fontproperties=font_set, fontsize = 14)
    #    plt.ylabel(y_title, fontproperties=font_set, fontsize = 14)
    #    plt.xticks(fontsize=12)
    #    plt.yticks(fontsize=12)
    #    corcoef = get_corrcoef(x_array[cat_idx], y_array[cat_idx])[0][1]
    #    plt.title(category_title + " = %s, corrcoef = %5.3f"%(cat_value, corcoef), fontproperties=font_set, fontsize = 12)
    #    plt.scatter(x_array[cat_idx], y_array[cat_idx], c='red', marker='+')
    #    plt.grid(True)
    #plt.subplots_adjust(left=0.123, right=0.9, bottom=0.1, top=0.9, wspace=0.2, hspace=0.2)
    plt.show()
    #plt.savefig(out_img, format=fileformat, dpi=150)

def CheckFile(FileName):
    if not os.path.exists(FileName):
        return 0
    return 1