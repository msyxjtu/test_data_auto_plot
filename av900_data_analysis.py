# -*- coding: utf-8 -*-

import os
import time

import matplotlib.pyplot as plt
import pandas as pd


def average(target_list):
    sum = 0
    for _ in target_list:
        sum += _

    return sum / (len(target_list))


def summary_figure_output(file_dir, filename, time_unit='hour', replace=False, output_path=None):
    filepath = os.path.join(file_dir, filename)

    if os.path.exists(filepath + '_profile.png') and (not replace):
        pass
    else:
        data = pd.read_csv(filepath, sep='[,;\t]', header=0, engine='python')

        raw_capacity = data['ABCAh']

        if time_unit == 'seconds':
            time = data['TestTime']
            time_label_str = 'Time/s'
        elif time_unit == 'min':
            time = data['TestTime'] / 60
            time_label_str = 'Time/min'
        elif time_unit == 'hour':
            time = data['TestTime'] / 3600
            time_label_str = 'Time/h'

        try:
            pack_voltage = data['ABCVoltage']
            energy = 0
            current = data['ABCCurrent']
            max_cell_voltage = data['BATT_VOLT_MAX']
            min_cell_voltage = data['BATT_VOLT_MIN']
            voltage_difference_str = ''
            capacity_and_energy_str = ''
            temp_min, temp_max = data['CAN1BATT_TEMP_MIN'], data['CAN1BATT_TEMP']
        except KeyError:
            temp_min, temp_max = data['CAN2BATT_TEMP_MIN'], data['CAN2BATT_TEMP']

        for __ in range(1, len(current) - 1):
            if current[__] < 0 <= current[__ + 1]:
                pass
                # voltage_difference_str += '放电压差' + str(round((max_cell_voltage[__] - min_cell_voltage[__])*1000)) + 'mV ' + '\n'
            elif current[__] > 0 >= current[__ + 1]:
                pass
                # voltage_difference_str += '充电压差' + str(round((max_cell_voltage[__] - min_cell_voltage[__])*1000)) + 'mV ' + '\n'
        for __ in range(1, len(raw_capacity) - 1):
            if raw_capacity[__] > 0 >= raw_capacity[__ + 1]:
                capacity_and_energy_str += '充电容量：' + str(round(raw_capacity[__], 2)) + 'Ah '
                capacity_and_energy_str += '充电能量：' + str(round(energy / 1000, 3)) + 'kWh'
                capacity_and_energy_str += '\n'
                energy = 0
            elif raw_capacity[__] < 0 <= raw_capacity[__ + 1]:
                capacity_and_energy_str += '放电容量：' + str(round(0 - raw_capacity[__], 2)) + 'Ah '
                capacity_and_energy_str += '放电能量：' + str(round(-energy / 1000, 3)) + 'kWh'
                capacity_and_energy_str += '\n'
                energy = 0
            else:
                energy += (raw_capacity[__ + 1] - raw_capacity[__]) * pack_voltage[__]

        plt.rcParams['xtick.labelsize'] = 8
        plt.rcParams['ytick.labelsize'] = 8
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['lines.linewidth'] = 1
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        plt.subplot(221)
        plt.plot(time, current)
        plt.xlabel(time_label_str, fontsize=9)
        plt.ylabel('Current/A', fontsize=9)
        #    plt.savefig(os.path.join(root,_ + '_Current_profile.png'),dpi = 600)
        #    plt.close()
        #    plt.grid()
        plt.xlim(min(time), max(time))

        plt.subplot(224)
        plt.plot(time, temp_min, time, temp_max)
        plt.xlabel(time_label_str, fontsize=9)
        plt.ylabel('Temp/degC', fontsize=9)
        plt.xlim(min(time), max(time))
        #    plt.savefig(filepath + '_temp_profile.png'),dpi = 600)
        #    plt.close()
        #    plt.grid()

        plt.subplot(223)
        plt.plot(time, max_cell_voltage, time, min_cell_voltage)
        plt.xlabel(time_label_str, fontsize=9)
        plt.ylabel('Voltage/V', fontsize=9)
        plt.yticks([2.7, 3.0, 3.5, 4.0, 4.2])
        plt.ylim(2.5, 4.5)
        plt.xlim(min(time), max(time))
        plt.text(0, 4.45, voltage_difference_str, fontsize=5)
        plt.grid()

        plt.subplot(222)
        plt.plot(time, raw_capacity)
        plt.xlabel(time_label_str, fontsize=9)
        plt.ylabel('Capacity/Ah', fontsize=9)
        plt.xlim(min(time), max(time))
        plt.text(0, 40, capacity_and_energy_str, fontsize=5)
        plt.grid()

        if output_path == 'None':
            plt.savefig(filepath + '_profile.png', dpi=300)
        else:
            plt.savefig(os.path.join(output_path, filename + '_profile.png'), dpi=300)
        plt.close()


def aging_data_dcr_output(filepath, test_current=-120):
    data = pd.read_csv(filepath,
                       sep='\t',
                       header=0,
                       engine='python')

    pack_voltage = data['ABCVoltage']
    current = data['ABCCurrent']
    cell_v_max = data['BATT_VOLT_MAX']
    cell_v_min = data['BATT_VOLT_MIN']
    temp_max = data['CAN2BATT_TEMP']
    temp_min = data['CAN2BATT_TEMP_MIN']

    dcr_area_end = []
    dcr_area_start = []
    for _ in range(0, len(current) - 6):
        if test_current - 5 < current[_] < test_current + 5 and test_current - 5 < current[_ + 4] < test_current + 5:
            dcr_area_start.append(_ - 10)
            dcr_area_start.append(_ + 10)
            break

    for _ in range(0, len(current) - 6):
        if test_current - 5 < current[_] < test_current + 5 and -5 < current[_ + 4] < 5:
            dcr_area_end.append(_ - 10)
            dcr_area_end.append(_ + 10)
            break

    voltage_start = max(pack_voltage[dcr_area_start[0]:dcr_area_start[1]])
    voltage_end = min(pack_voltage[dcr_area_end[0]:dcr_area_end[1]])
    cell_v_max_start = max(cell_v_max[dcr_area_start[0]:dcr_area_start[1]])
    cell_v_max_end = min(cell_v_max[dcr_area_end[0]:dcr_area_end[1]])

    cell_v_min_start = max(cell_v_min[dcr_area_start[0]:dcr_area_start[1]])
    cell_v_min_end = min(cell_v_min[dcr_area_end[0]:dcr_area_end[1]])

    temp_max_dcr = average(temp_max[dcr_area_start[0]:dcr_area_start[1]])
    temp_min_dcr = average(temp_min[dcr_area_start[0]:dcr_area_start[1]])

    dcr = (voltage_start - voltage_end) / test_current
    return dcr, voltage_start, voltage_end, cell_v_max_start, cell_v_max_end, \
           cell_v_min_start, cell_v_min_end, temp_max_dcr, temp_min_dcr


if __name__ == '__main__':
    start_time = time.time()
    file_types = ['dat', 'csv']
    dir_temp = input('输入文件地址：')
    data_dir = dir_temp.replace('\\', '/')

    dcr = []
    voltage_start = []
    voltage_end = []
    cell_v_max_s = []
    cell_v_min_s = []
    cell_v_max_e = []
    cell_v_min_e = []
    temp_max = []
    temp_min = []
    for root, dirs, files in os.walk(data_dir):
        for _ in files:
            print(_)
            if _[-3:] in file_types:
                # summary_figure_output(root, _, time_unit='min', replace=True,
                #                       output_path=root)
                dcr_, voltage_start_, voltage_end_, cell_v_m_s, cell_v_m_e, cell_v_n_s, cell_v_n_e, temp_dcr_max, temp_dcr_min = aging_data_dcr_output(
                    os.path.join(root, _), test_current=-120)
                dcr.append(dcr_)
                voltage_end.append(voltage_end_)
                voltage_start.append(voltage_start_)
                cell_v_max_s.append(cell_v_m_s)
                cell_v_min_s.append(cell_v_n_s)
                cell_v_max_e.append(cell_v_m_e)
                cell_v_min_e.append(cell_v_n_e)
                temp_max.append(temp_dcr_max)
                temp_min.append(temp_dcr_min)
    print('total time: ', time.time() - start_time)
