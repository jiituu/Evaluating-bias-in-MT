# Evaluating-bias-in-MT

# MLM Fine-tuning (Afriberta & mBERT)

All experiments share the same configuration file (`config.json`).
Only the following fields change per run:
- `model_name_or_path`
- `tokenizer_name`
- `train_file` / `validation_file`
- `output_dir`

## Example (Colab)
```bash
!python run_mlm.py \
  --model_name_or_path bert-base-multilingual-cased \
  --tokenizer_name /path/to/custom_tokenizer \
  --train_file /content/drive/MyDrive/LocalMachineTranslation/Datasets/nllb/om/train.txt \
  --validation_file /content/drive/MyDrive/LocalMachineTranslation/Datasets/nllb/om/validation.txt \
  --output_dir ./mbert_oromo_finetuned \
  --config_name config.json

