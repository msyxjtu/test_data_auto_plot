# -*- coding: utf-8 -*-
# import pandas as pd
import shutil

from can_function import *
from output_fig import *


def can_data_draw_pic(data_directory, signals_dict, dbc_path):
    for root, dirs, files in os.walk(data_directory):
        for _ in files:
            if _[-4:] == '.asc':
                output_file_path = os.path.join(root, _[:-4] + '_signals_folder')

                if not os.path.exists(output_file_path):
                    os.mkdir(output_file_path)
                else:
                    shutil.rmtree(output_file_path)
                    os.mkdir(output_file_path)

                asc2signals(dbc_path, os.path.join(root, _), output_file_path)
                output_fig(output_file_path, output_file_path, signals_dict)


if __name__ == '__main__':
    # input signals name and accordingly dbc signal name here
    to_plot_signals_dict = {'signal name': 'name in dbc'}

    dbc_path = 'input_dbc_path_here'

    can_data_draw_pic(input('please input data directory:').replace('\\', '/'), to_plot_signals_dict,
                      dbc_path)
