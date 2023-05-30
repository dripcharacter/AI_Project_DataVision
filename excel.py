import pandas as pd
import sys
import os


def excel_preprocess(file_name, hand_process_bool):
    df = pd.read_excel(file_name)
    if 'fixed_label' not in df.columns:
        df['fixed_label'] = -1
    if 'sigmoid_label' not in df.columns:
        df['sigmoid_label'] = 0
    tmp_sum = 0
    tmp_cnt = 0
    process_list = list()
    for idx, entry in enumerate(df['label']):
        if entry > 0.1:
            # print(idx)
            process_list.append(idx)
        else:
            df['fixed_label'][idx] = entry
            tmp_cnt = tmp_cnt + 1
            tmp_sum = tmp_sum + entry
    tmp_mean = tmp_sum / tmp_cnt
    print('mean: ' + str(tmp_mean))
    if not hand_process_bool:
        for entry in process_list:
            df['fixed_label'][entry] = tmp_mean
    for idx, entry in enumerate(df['fixed_label']):
        if entry >= 0.5:
            df['sigmoid_label'][idx] = 1

    with pd.ExcelWriter(file_name) as w:
        df.to_excel(w, index=False)


if __name__ == "__main__":
    data_dir = sys.argv[1]
    hand_process_bool = sys.argv[2]
    print(data_dir)
    file_list = os.listdir(data_dir)
    for name in file_list:
        print("start pre-process to " + name)
        excel_preprocess(data_dir + '/' + name, hand_process_bool)
        print("end pre-process to" + name)
