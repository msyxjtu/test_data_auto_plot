import csv
import os


class Signal:
    def __init__(self, signal_describe_content, signal_id):
        signal_info = signal_describe_content.split()
        self.id = signal_id
        self.name = signal_info[1]
        raw_start_position = int(signal_info[3].split('|')[0])
        actual_start_position = raw_start_position // 8 * 8 + 8 - raw_start_position % 8
        self.position = (actual_start_position, int(signal_info[3].split('|')[1].split('@')[0]))
        self.factor = eval(signal_info[4])[0]
        self.offset = eval(signal_info[4])[1]
        self.unit = signal_info[6]
        self.time_line = []
        self.value = []

    def update(self, time_stamp, value):
        self.time_line.append(time_stamp)
        try:
            self.value.append(self.offset + self.factor * (
                int(value[self.position[0] - 1: self.position[0] + self.position[1] - 1], 2)))
        except ValueError:
            pass


def dbc_resolve(dbc_path):
    """

    :param dbc_path: dbc file path
    :return:
        1. 包含了所有ID帧的字典，键为ID号，值为ID名称
        2. 包含了所有信号列表的list
    """

    # id_list = {'message_id':'message_name'}
    id_list = {}
    signal_list = []
    with open(dbc_path, 'r') as dbc_file:
        dbc_data = dbc_file.readlines()
        message_id = 'unknown'
        for _ in dbc_data:
            if _[0:3] == 'BO_':
                id_list[int(_.split()[1])] = _.split()[2]
                message_id = int(_.split()[1])
            if _[0:4] == ' SG_':
                # print(_)
                signal_list.append(Signal(_, message_id))

    return id_list, signal_list


def convert_can_message_content(can_message_list, base):
    can_bin = []
    # print(can_message_list)
    if can_message_list[-1] == '\n':
        can_message_list = can_message_list[0: -1]

    if base == 'dec':
        for _ in can_message_list:
            can_bin.append(bin(int(_)).replace('0b', '').zfill(8))
    elif base == 'hex':
        for _ in can_message_list:
            # print(_)
            can_bin.append(bin(int(_, 16)).replace('0b', '').zfill(8))
    message_bin_content = ''.join(can_bin)
    return message_bin_content


def asc_data_resolve(can_data_file, id_list):
    frame_list = {}
    for _ in id_list:
        frame_list[_] = []

    with open(can_data_file, 'r') as can_data:
        base = 'hex'

        x = 0
        for _ in can_data:
            x += 1

            if x < 7:
                pass
            else:
                try:
                    can_message = _.split(' ')
                    # print(can_message)
                    if can_message[2] == 'ErrorFrame' or can_message[2] == 'Statistic:':
                        pass
                    else:
                        frame_id = 'unknown'
                        #                        print(can_message)
                        try:
                            if base == 'hex':
                                # print(can_message)
                                frame_id = int(can_message[2][-3:], 16)
                            #                                print(frame_id)
                            elif base == 'dec':
                                frame_id = int(can_message[2][-3:], 10)
                            else:
                                print('unknown base')
                            if frame_id in id_list:
                                # print(can_message)
                                # print(can_message[7])
                                can_message_content = convert_can_message_content(can_message[6:14], base)
                                frame_list[frame_id].append([can_message[0], can_message_content])

                        #                        except ValueError:
                        except IndexError:
                            print(can_message[2])
                except IndexError:
                    print(can_message)
                # 需要增加代码，保证在出现程序当中没有考虑到的bug的时候，能够记录下log（报错信息），并让程序继续跑下去，不至于宕机。
    return frame_list


def asc2signals(dbc_path, can_data_file, output_file_path):
    id_list, signal_list = dbc_resolve(dbc_path)
    frame_list = asc_data_resolve(can_data_file, id_list)

    for _ in signal_list:
        for __ in frame_list[_.id]:
            _.update(__[0], __[1])

    for _ in signal_list:
        # if len(_.value) > 0:
        with open(os.path.join(output_file_path, _.name + '.csv'), 'w', newline='') as output_csv:
            writer = csv.writer(output_csv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['time', _.name])
            # print(_.name)
            for __ in range(len(_.time_line)):
                # print(__)
                # print(str(_.time_line[__]) + ',' + str(_.value[__]) + '\n')
                # output.write(_.time_line[__] + ',' + str(_.value[__]) + '\n')
                writer.writerow([_.time_line[__], _.value[__]])


