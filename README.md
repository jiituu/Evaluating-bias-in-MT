# Evaluating-bias-in-MT

This repository contains the scripts, configurations, and annotated data used to **evaluate gender bias** in Masked Language Models (MLMs) for **low-resource languages** — Amharic, Afan Oromo, and Tigrinya.  
It is a sub-repository of the broader *Evaluating Machine Translation Datasets for Low-Web Data Languages: A Gendered Lens 🔍* project.

---

# MLM Fine-tuning (Afriberta & mBERT)

All experiments share the same configuration file (`Code/config.json`).
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
```

## Annotations & Benchmark

- Human annotations and labeling guidelines are stored in [`Annotations/`](Annotations/).  
  Includes:
  - Annotated Excel files (`Am`, `Om`, `Ti`)
  - The annotation guideline (`Annotation_Guideline.docx`)
  - Prediction and evaluation scripts are located in [Code/get_predictions.py] This script generates top-k predictions from base and fine-tuned models for comparison against annotated references.

## Example (Colab)
```bash
!python Code/get_predictions.py \
  --csv_file Annotations/annotations.csv \
  --models castorini/afriberta_small Bonnief/mbert-om-100k-finetuned \
  --output_path Results/ti_predictions.xlsx \
  --top_k 5
```
