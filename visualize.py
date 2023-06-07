import json
import matplotlib.pyplot as plt

json_string = '''{
    "series_name": "testseries",
    "episode_num": 765,
    "current_classify": "19",
    "evaluation": {
        "0s": 0.041,
        "23s": 0.196,
        "1:34": 0.04,
        "1:57": 0.517,
        "2:10": 0.753,
        "2:36": 0.535,
        "3:10": 0.752,
        "3:36": 0.695,
        "4:10": 0.653,
        "4:36": 0.289,
        "5:0": 0.535,
        "5:30": 0.862,
        "6:0": 0.648,
        "6:30": 0.075,
        "7:0": 0.414,
        "7:30": 0.917,
        "8:0": 0.569,
        "8:30": 0.375,
        "9:0": 0.6065,
        "9:30": 0.587,
        "10:0": 0.156,
        "10:30": 0.152,
        "11:07": 0.3836,
        "11:26": 0.723,
        "12:0": 0.212,
        "12:45": 0.262,
        "13:0": 0.651,
        "13:34": 0.173,
        "14:06": 0.2607,
        "14:49": 0.6705,
        "15:37": 0.2413
    }
}'''


def colormap_generate(min_color, max_color, target_list):
    colors = [0] * len(target_list)
    for idx in range(len(target_list)):
        ratio = (target_list[idx] - min(target_list)) / (max(target_list) - min(target_list))
        colors[idx] = (
            ratio * min_color[0] + (1 - ratio) * max_color[0], ratio * min_color[1] + (1 - ratio) * max_color[1],
            ratio * min_color[2] + (1 - ratio) * max_color[2])
    return colors


def object_visualize(json_object, file_path):
    key_list = list(json_object['Time'])

    value_list = list(json_object['label'])
    mean_list = list(json_object['label'])
    for key_idx, key_entry in enumerate(key_list):
        tmp = key_entry.split(':')
        if len(tmp) == 1:
            tmp = key_entry.split('s')
            key_list[key_idx] = int(tmp[0])
        else:
            key_list[key_idx] = int(tmp[0]) * 60 + int(tmp[1])
        if key_idx == 0:
            tmp = 0
        else:
            tmp = mean_list[key_idx - 1]
        mean_list[key_idx] = value_list[key_idx] + tmp
    for idx in range(len(mean_list)):
        mean_list[idx] = mean_list[idx] / (idx + 1)

    colors = colormap_generate((1.0, 0, 0), (0, 0, 1.0), value_list)

    plt.figure(figsize=(20, 4))
    plt.bar(key_list, value_list, label='individual_val', width=5.0, color=colors, edgecolor='black')
    plt.xlabel('time')
    plt.ylabel('result_label')
    plt.xlim([key_list[0] - 60, key_list[-1] + 60])
    plt.ylim([0, 1])
    plt.plot(key_list, mean_list, label='mean_val')
    plt.legend()
    plt.savefig(file_path)
    plt.close()


if __name__ == '__main__':
    json_object = json.loads(json_string)
    object_visualize(json_object)
