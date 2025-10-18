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
  --train_file /path/to/train.txt \
  --validation_file /path/to/validation.txt \
  --output_dir /path/to/output/dir \
  --config_name config.json


## Annotations & Benchmark

- Human annotations and labeling guidelines are stored in [`Annotations/`](Annotations/).  
  Includes:
  - Annotated Excel files (`Am`, `Om`, `Ti`)
  - The annotation guideline (`Annotation_Guideline.docx`)

