import torch
import pandas as pd
import numpy as np
from transformers import AutoTokenizer

MODEL_PATH = "./model.pt"
MODEL_NAME = "beomi/KcELECTRA-base"

model = torch.load(MODEL_PATH, map_location=torch.device('cpu'))
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
device = torch.device('cpu')


def test(test_sample):
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


if __name__ == "__main__":
    TEST_NAME = "마이네임_1화.xlsx"
    test_sample = test(TEST_NAME)
    print(test_sample)
