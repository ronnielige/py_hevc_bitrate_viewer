import sys
reload(sys)
sys.setdefaultencoding('utf8')

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import os

def extract_hm_ashevc_vbvinfo(inf_name, frame_rate, vbv_init_time, vbv_bitrate):
    accum_bits       = 0
    accum_bits_array = [0, ]
    time_array       = [0, ]
    frame_idx        = 1
    init_frames      = (int)(vbv_init_time * frame_rate / 1000.0)
    frame_avg_bits   = (int)(vbv_bitrate / frame_rate)
    inf              = open(inf_name, 'r')
    line             = inf.readline()
    # first accumate init frames
    while frame_idx <= init_frames:
        accum_bits = accum_bits + frame_avg_bits
        accum_bits_array.append(accum_bits)
        time_array.append(frame_idx)
        frame_idx = frame_idx + 1

    while line:
        bits_pos = line.find("bits [Y")
        if bits_pos >= 0:
            frame_bits = (int)(line.split()[11])
            accum_bits = accum_bits + frame_avg_bits  # receive bits
            accum_bits_array.append(accum_bits)
            time_array.append(frame_idx)

            accum_bits = accum_bits - frame_bits      # remove frame bits
            accum_bits_array.append(accum_bits)
            time_array.append(frame_idx)

            frame_idx = frame_idx + 1
        line = inf.readline()
    return time_array, accum_bits_array

def extract_hm_ashevc_bitrate(inf_name, frame_rate, check_interval_frames):
    bitrate_array = []
    inf        = open(inf_name, 'r')
    line       = inf.readline()
    frame_idx  = 0
    accum_bits = 0
    bitrate_array = []
    time_array    = []
    interval_frms = check_interval_frames
    while line:
        bits_pos = line.find("bits [Y")
        if bits_pos >= 0:
            frame_bits = (int)(line.split()[11])
            accum_bits = accum_bits + frame_bits
            frame_idx  = frame_idx + 1
            if frame_idx % interval_frms == 0: # accumulated N seconds
                bitrate_array.append(accum_bits / (check_interval_frames / frame_rate) / 1000)
                #time_array.append((frame_idx - 1) / frame_rate)
                time_array.append(frame_idx)
                accum_bits = 0
        line = inf.readline()
    return time_array, bitrate_array

def extract_bitrate(inf_name, enc_id, frame_rate, check_interval):
    bitrate_array = []
    inf        = open(inf_name, 'r')
    line       = inf.readline()
    frame_idx  = 0
    accum_bits = 0
    bitrate_array = []
    time_array    = []
    interval_frms = (int)(check_interval * frame_rate)
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
            if frame_idx % interval_frms == 0:  # accumulated N seconds
                bitrate_array.append(accum_bits / check_interval / 1000)
                time_array.append((frame_idx - 1) / frame_rate)
                accum_bits = 0

        line = inf.readline()

    return time_array, bitrate_array

def plot_arrays(time_array, bitrate_array, out_img, bitrate_interval, xlabel_type):
    font_set = FontProperties(fname=r"c:\windows\fonts\calibri.ttf", size=15)
    category_f0 = plt.figure(0, figsize=(20, 10))
    fileformat  = os.path.splitext(out_img)[1][1:]
    avg_bitrate = sum(bitrate_array) / len(bitrate_array)
    avg_br_arr  = [avg_bitrate, ] * len(bitrate_array)
    max_bitrate = max(bitrate_array)
    max_bitrate_idx  = bitrate_array.index(max_bitrate)
    max_bitrate_time = time_array[max_bitrate_idx]
    max_avg_rat = (float)(max_bitrate) / avg_bitrate
    yrange      = max_bitrate * 1.5
    xrange      = max(time_array) - min(time_array)
    plt.ylim(0, yrange)
    plt.xlim(min(time_array), max(time_array))

    plt.text(max_bitrate_time + xrange / 50, max_bitrate + yrange / 50, "%.2f kbps, time %s sec"%(max_bitrate, max_bitrate_time)) # show maxbitrate position
    plt.annotate('', xy=(max_bitrate_time, max_bitrate), xytext=(max_bitrate_time + xrange / 50, max_bitrate + yrange / 50), arrowprops=dict(arrowstyle="->",connectionstyle="arc3"))

    plt.plot(time_array, bitrate_array, marker='.')
    plt.plot(time_array, avg_br_arr)
    if xlabel_type == 0:
        plt.xlabel("frame number", fontproperties=font_set, fontsize = 14)
    elif xlabel_type == 1:
        plt.xlabel("time(second)", fontproperties=font_set, fontsize = 14)
    plt.ylabel("bitrate(kbp/s)", fontproperties=font_set, fontsize = 14)
    plt.title("Bitrate interval %3.1f seconds\n Average, Maximum bitrate = %d kbps, %d kbps\n max / avg = %4.2f"%(bitrate_interval, avg_bitrate, max_bitrate, max_avg_rat), fontproperties=font_set, fontsize = 12)
    plt.grid(True)
    plt.show()
    #plt.savefig(out_img, format=fileformat, dpi=150)

def plot_vbv_arrays(time_array, vbv_array, out_img, vbv_bufsize, init_frames):
    font_set = FontProperties(fname=r"c:\windows\fonts\calibri.ttf", size=15)
    category_f0 = plt.figure(0, figsize=(20, 10))
    fileformat  = os.path.splitext(out_img)[1][1:]
    vbv_bufsz_arr  = [vbv_bufsize, ] * len(vbv_array)
    vbv_bufzero_arr = [0, ] * len(vbv_array)
    max_bits = max(vbv_array)
    max_bits_idx  = vbv_array.index(max_bits)
    max_bits_time = time_array[max_bits_idx]
    min_bits = min(vbv_array[init_frames:])  # exclude the vbv init frames
    min_bits_idx = vbv_array.index(min_bits)
    min_bits_time = time_array[min_bits_idx]
    yuprange    = max_bits * 1.5
    ydownrange  = min(0, 1.2 * min_bits)
    xrange      = max(time_array) - min(time_array)
    plt.ylim(ydownrange, yuprange)
    plt.xlim(min(time_array), max(time_array))

    plt.text(max_bits_time + xrange / 50, max_bits + yuprange / 50, "%.2f kbit, frame %s"%(max_bits / 1000.0, max_bits_time)) # show maxbits position
    plt.annotate('', xy=(max_bits_time, max_bits), xytext=(max_bits_time + xrange / 50, max_bits + yuprange / 50), arrowprops=dict(arrowstyle="->",connectionstyle="arc3"))

    plt.plot(time_array, vbv_array, marker='.')
    plt.plot(time_array, vbv_bufsz_arr)

    plt.plot(time_array, vbv_array, marker='.')
    plt.plot(time_array, vbv_bufzero_arr)

    plt.xlabel("frame number", fontproperties=font_set, fontsize = 14)
    plt.ylabel("bits", fontproperties=font_set, fontsize = 14)
    plt.title("vbv max_value = %6.1f kbits, min_value = %6.1f kbits\n max - min = %6.1f kbits"%(max_bits / 1000.0, min_bits / 1000.0, (max_bits - min_bits) / 1000.0), fontproperties=font_set, fontsize = 12)
    plt.grid(True)
    plt.show()

def CheckFile(FileName):
    if not os.path.exists(FileName):
        return 0
    return 1