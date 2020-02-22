import os

import matplotlib.pyplot as plt
import pandas as pd


def plot_signal(df, x_label, y_label):
    plt.plot(df.iloc[:, 0], df.iloc[:, 1])
    plt.xlabel(x_label)
    plt.ylabel(y_label)


def output_fig_current_battery_can(data_path, output_path, signal_dict):
    data_list = {}
    for root, dirs, files in os.walk(data_path):
        for __ in files:
            if __[-4:] == '.csv':
                data = pd.read_csv(os.path.join(root, __), sep=',', header=0, engine='python')
                data_list[str(__[:-4])] = data

    plt.rcParams['axes.labelsize'] = 7
    plt.rcParams['axes.titlesize'] = 7
    plt.rcParams['font.size'] = 7
    plt.rcParams['figure.figsize'] = [12, 8]

    plot_signal(data_list[signal_dict['current']], 'Time/s', 'Current/A')

    plt.savefig(os.path.join(output_path + '_summary.png'), dpi=600)
    plt.close()




def output_fig(data_path, output_path, signal_dict):
    data_list = {}
    for root, dirs, files in os.walk(data_path):
        for __ in files:
            if __[-4:] == '.csv':
                data = pd.read_csv(os.path.join(root, __), sep=',', header=0, engine='python')
                data_list[str(__[:-4])] = data

    plt.rcParams['axes.labelsize'] = 7
    plt.rcParams['axes.titlesize'] = 7
    plt.rcParams['font.size'] = 7
    plt.rcParams['figure.figsize'] = [12, 8]

    plt.subplot(2, 2, 1)
    plot_signal(data_list[signal_dict['max_cell_voltage']], 'Time/s', 'Voltage/V')
    plot_signal(data_list[signal_dict['min_cell_voltage']], 'Time/s', 'Voltage/V')

    plt.subplot(2, 2, 2)
    plot_signal(data_list[signal_dict['current']], 'Time/s', 'Current/A')

    plt.subplot(2, 2, 3)
    plot_signal(data_list[signal_dict['soc']], 'Time/s', 'SOC')
    plt.subplot(2, 2, 4)
    plot_signal(data_list[signal_dict['relay_status']], 'Time/s', 'relay_status')
    plt.savefig(os.path.join(output_path + '_summary.png'), dpi=600)
    plt.close()

    # plt.subplot(2, 1, 1)
    # plot_signal(data_list[signal_dict['max_cell_voltage']], 'Time/s', 'Voltage/V')
    # plot_signal(data_list[signal_dict['min_cell_voltage']], 'Time/s', 'Voltage/V')
    #
    # plt.subplot(2, 1, 2)
    # plot_signal(data_list[signal_dict['current']], 'Time/s', 'Current/A')
    #
    # plt.savefig(os.path.join(output_path + '_cell_voltage.png'), dpi=600)
    # plt.close()

    # plt.subplot(2, 1, 1)
    # plot_signal(data_list[signal_dict['max_temp']], 'Time/s', 'temp/degC')
    # plot_signal(data_list[signal_dict['min_temp']], 'Time/s', 'temp/degC')
    # plot_signal(data_list[signal_dict['inlet_temp']], 'Time/s', 'temp/degC')
    #
    # plt.subplot(2, 1, 2)
    # plot_signal(data_list[signal_dict['current']], 'Time/s', 'Current/A')
    # plt.savefig(os.path.join(output_path + '_temp.png'), dpi=600)
    # plt.close()

    # plt.subplot(2, 1, 1)
    # plot_signal(data_list[signal_dict['insulation_resistance']], 'Time/s', 'kOhm')
    #
    # plt.subplot(2, 1, 2)
    # plot_signal(data_list[signal_dict['relay_status']], 'Time/s', 'relay_status')
    # plt.savefig(os.path.join(output_path + '_insulation_status.png'), dpi=600)
    # plt.close()


