# Evaluating-bias-in-MT

This repository contains the scripts, configurations, and annotated data used to **evaluate gender bias** in Masked Language Models (MLMs) for **low-resource languages** — Amharic, Afan Oromo, and Tigrinya.  
It is a sub-repository of the broader *Evaluating Machine Translation Datasets for Low-Web Data Languages: A Gendered Lens 🔍* project.

---
## 📋 Project Overview

We evaluate gender bias in MLMs by analyzing top-1 and top-5 predictions for masked tokens in approximately 376 sentences across three Ethiopian languages. The project involves fine-tuning both mBERT and AfriBERTa models and comparing their predictions against human-annotated references to identify and quantify gender bias patterns.

## 📁 Repository Structure

### `Benchmark/`
Contains CSV files with benchmark data for each language used in our evaluation.

### `Annotations/`
Stores human-annotated data and labeling guidelines:
- Annotated Excel files for Amharic (Am), Afan Oromo (Om), and Tigrinya (Tir)
- Annotation guidelines (`Annotation_Guideline.docx`)
- Top-1 and top-5 annotated predictions for model evaluation

### `Code/`
Contains all implementation code:
- MLM training scripts and configuration (`config.json`)
- Prediction generation script (`get_predictions.py`)
- Visualization scripts for bias analysis:
  - `expected_vs_t1.py`: Compares expected vs top-1 predicted percentages
  - `t5_distribution.py`: Analyzes top-5 prediction distributions

## 🚀 Quick Start

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
  - Prediction and evaluation scripts are located in [`Code/get_predictions.py`] This script generates top-k predictions from base and fine-tuned models for comparison against annotated references.

## Example (Colab)
```bash
!python Code/get_predictions.py \
  --csv_file Annotations/annotations.csv \
  --models castorini/afriberta_small Bonnief/mbert-om-100k-finetuned \
  --output_path Results/ti_predictions.xlsx \
  --top_k 5
```

###  Visualizations
- Scripts in `Code/visualizations/` produce stacked bar plots and Excel summaries:
  - `expected_vs_t1.py` → per-sheet **Expected vs T1 Predicted** (%), saves PNGs + combined PDF and `*_percentages.xlsx`.
  - `t5_distribution.py` → per-sheet **Top-5 distribution** for Expected M/F (%), saves PNGs + combined PDF and `*_percentages.xlsx`.
- Example:
```bash
python Code/Visualizations/expected_vs_t1.py --xlsx Annotations/ti-annotated.xlsx --out_prefix Expected_vs_T1_ti
```

## 🤖 Models & Tokenizers

We used both **mBERT** and **AfriBERTa** models across **Afan Oromo**, **Amharic**, and **Tigrinya** to finetune and evaluate.
All fine-tuned checkpoints and tokenizers are publicly available on Hugging Face.

---

### 🔹 mBERT (Multilingual BERT)

| Language | Tokenizer | Fine-tuned Model |
|-----------|------------|-----------------|
| **Amharic** | [amharic-nllb-tokenizer](https://huggingface.co/Bonnief/amharic-nllb-tokenizer) | [mbert-am-100k-finetuned-II](https://huggingface.co/Bonnief/mbert-am-100k-finetuned-II) |
| **Afan Oromo** | [oromo-nllb-tokenizer](https://huggingface.co/Bonnief/oromo-nllb-tokenizer) | [mbert-om-100k-finetuned](https://huggingface.co/Bonnief/mbert-om-100k-finetuned) |
| **Tigrinya** | [tigrinya-nllb-tokenizer](https://huggingface.co/Bonnief/tigrinya-nllb-tokenizer) | [mbert-ti-100k-finetuned](https://huggingface.co/Bonnief/mbert-ti-100k-finetuned) |

---

### 🔹 AfriBERTa

| Language | Fine-tuned Model |
|-----------|-----------------|
| **Amharic** | [Afriberta-100k-am](https://huggingface.co/Bonnief/Afriberta-100k-am) |
| **Afan Oromo** | [afriberta-om-finetuned](https://huggingface.co/Bonnief/afriberta-om-finetuned) |
| **Tigrinya** | [afriberta-ti-finetuned](https://huggingface.co/Bonnief/afriberta-ti-finetuned) |

---

## 📚 Literature Review

### Linguistic Studies

1. **Comparative analyses of linguistic sexism in Afan Oromo, Amharic, and Gamo**  
   *Amanuel Raga Yadate* (2015) [[Paper]](https://www.researchgate.net/publication/338956038_Comparative_analyses_of_linguistic_sexism_in_Afan_Oromo_Amharic_and_Gamo)
   Examines how cultural gender bias reflects through language structures in Ethiopian languages. The study highlights grammatical obligations where some verbs collocate only with gender-specific nouns, such as verbs meaning "to be left unmarried" that only take feminine arguments. Also discusses lexical differences like separate verbs for "to marry" for males and females in Afan Oromo, where the feminine form carries negative connotations equivalent to "to be sold," reflecting cultural practices of bride prices.

3. **Gender bias ideology as manifested in the grammar of Afan Oromo**  
   [[Paper]](https://academicjournals.org/journal/jlc/article-full-text-pdf/ce8346f2264)  
   Defines gender and gender bias through multiple dimensions: gender categorization of nouns based on attributes, relative size, relative power, and social values of referents. Analyzes gendered administration and profession titles, including historical Gada administration system titles and post-Gada titles. Discusses the challenge that even when feminine forms of biased titles can be created, the binary gender system forces speakers to use one form as generic, perpetuating bias.

4. **Critical Discourse Analysis of Gender Conceptions in Preparatory Tigrigna Language Textbooks**  
   [[Paper]](https://journal.mu.edu.et/index.php/jebs/article/view/442)  
   Identifies two main ways femininity is rendered invisible in educational materials: (1) by portraying generic nouns in masculine terms, and (2) by representing gender-neutral nouns from a male perspective. The study also notes some androgynous conceptions of gender while highlighting predominant stereotypic roles and the marginalization of feminine representation.
