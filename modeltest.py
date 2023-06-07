import torch
import pandas as pd
import numpy as np
from transformers import AutoTokenizer

MODEL_PATH = "./model.pt"
MODEL_NAME = "beomi/KcELECTRA-base"

def test(test_sample):
    model = torch.load(MODEL_PATH, map_location=torch.device('cpu'))
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    device = torch.device('cpu')

    test_sample = test_sample.drop(['Transliteration'], axis=1)
    test_sample['label'] = np.nan

    # Iterate over each row and update the 'label' values
    for i, row in test_sample.iterrows():
        model.eval()

        token_ = tokenizer.encode_plus(
            row['Subtitle'],
            truncation=True,
            add_special_tokens=True,
            max_length=128,
            padding="max_length",
            return_tensors='pt'
        )

        input_ids = token_['input_ids'].to(device)
        attention_mask = token_['attention_mask'].to(device)

        with torch.no_grad():
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs[0]
            logits = logits.detach().cpu()
            probabilities = torch.sigmoid(-logits)
            result = probabilities.squeeze().tolist()

        test_sample.loc[i, 'label'] = result[0]

    with pd.ExcelWriter("result.xlsx") as w:
        test_sample.to_excel(w, index=False)

    return test_sample


def evaluate(test_samples):
    result = []
    result_y = []
    real_result = []
    for i in range(len(test_samples['label'].values) - 3):
        # print(test_sample['label'].values[i])
        sum_R = 0
        for j in range(3):
            sum_R = sum_R + test_samples['label'].values[i + j]

        if sum_R / 3 > 0.3:  # 기준 값
            result.append(test_samples['Time'].values[i])
            result_y.append(sum_R / 3)

    aggressive_count = len(result)
    total_count = len(test_samples['label'].values)
    aggressive_percent = 100 * aggressive_count / total_count

    real_result.append("Aggressive per 3 sentence over is {:.2f}%".format(aggressive_percent))

    # 연령 분류
    age_category = ''
    if aggressive_percent >= 9:
        age_category = '19 years old'
    elif aggressive_percent >= 3.5:
        age_category = '15 years old'
    else:
        age_category = 'All'

    real_result.append("Age category: {}".format(age_category))
    return real_result



if __name__ == "__main__":
    TEST_NAME = "마이네임_1화.xlsx"
    test_sample = test(TEST_NAME)
    print(test_sample)
