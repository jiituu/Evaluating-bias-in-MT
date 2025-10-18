import argparse
import pandas as pd
from transformers import pipeline, AutoTokenizer, AutoModelForMaskedLM
from tqdm import tqdm

def load_fill_mask_pipeline(model_path):
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForMaskedLM.from_pretrained(model_path)
    return pipeline("fill-mask", model=model, tokenizer=tokenizer), tokenizer

def run_predictions(pipe, tokenizer, sentences, top_k=5):
    predictions = []
    for sentence in tqdm(sentences, desc="Generating predictions"):
        masked_input = sentence.replace("[MASK]", tokenizer.mask_token)
        try:
            preds = pipe(masked_input, top_k=top_k)
            top_words = [p["token_str"].strip() for p in preds]
            predictions.append(" ||| ".join(top_words))
        except Exception as e:
            predictions.append(f"Error: {e}")
    return predictions

def predict_from_csv(csv_file, text_column, model_names, output_path, top_k=5):
    df = pd.read_csv(csv_file)
    sentences = df[text_column].dropna().tolist()
    df_out = pd.DataFrame({"masked_sentence": sentences})

    for model_name in model_names:
        print(f"🔄 Loading {model_name}")
        pipe, tokenizer = load_fill_mask_pipeline(model_name)
        preds = run_predictions(pipe, tokenizer, sentences, top_k=top_k)
        col_name = model_name.split("/")[-1]
        df_out[col_name] = preds

    df_out.to_excel(output_path, index=False)
    print(f"\n Predictions saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_file", required=True)
    parser.add_argument("--text_column", default="masked_sentence")
    parser.add_argument("--models", nargs="+", required=True)
    parser.add_argument("--output_path", default="predictions.xlsx")
    parser.add_argument("--top_k", type=int, default=5)
    args = parser.parse_args()

    predict_from_csv(args.csv_file, args.text_column, args.models, args.output_path, args.top_k)
