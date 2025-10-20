import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pathlib import Path

def main(xlsx_path, out_prefix="T5_Distribution_MF", expected_col="Expected Gender"):
    t5_cols = ["T5 Male", "T5 Female", "T5 Neutral", "Wrong"]
    xls = pd.ExcelFile(xlsx_path)
    results_dir = Path("Results"); results_dir.mkdir(exist_ok=True)

    all_t5_percent = {}
    long_rows = []

    pdf_path = results_dir / f"{out_prefix}_all.pdf"
    with PdfPages(pdf_path) as pdf:
        for sheet in xls.sheet_names:
            if sheet.lower() in {"expectedgendercounts"}:
                continue

            df = pd.read_excel(xls, sheet_name=sheet)
            req_cols = [expected_col] + t5_cols
            if any(c not in df.columns for c in req_cols):
                print(f"Skipping {sheet}: missing one of {req_cols}")
                continue

            df = df.dropna(subset=[expected_col]).copy()
            df[expected_col] = df[expected_col].astype(str).str.strip().str.upper()
            for c in t5_cols:
                df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)

            df = df[df[expected_col].isin(["M", "F"])].copy()
            if df.empty: 
                continue

            sums = df[t5_cols].sum(axis=1)
            norm = df[t5_cols].div(sums.replace(0, np.nan), axis=0) * 100.0
            norm[expected_col] = df[expected_col].values

            t5_pct = norm.groupby(expected_col)[t5_cols].mean().round(2)
            all_t5_percent[sheet] = t5_pct

            for exp in t5_pct.index:
                for col in t5_cols:
                    long_rows.append({
                        "Sheet": sheet,
                        "Expected": exp,
                        "Predicted": col.replace("T5 ", "").lower(),
                        "Percent": float(t5_pct.loc[exp, col])
                    })

            ax = t5_pct.plot(kind="bar", stacked=True, figsize=(7, 5))
            plt.title(f"T5 Distribution (%) when Expected = M/F — {sheet}")
            plt.ylabel("Average Percentage (%)"); plt.xlabel("Expected Gender")
            plt.ylim(0, 100)
            plt.legend(title="Predicted (T5)", bbox_to_anchor=(1.05, 1), loc="upper left")
            for container in ax.containers:
                ax.bar_label(container, fmt="%.1f%%", label_type="center", color="white", fontsize=8)

            plt.tight_layout()
            png_name = results_dir / f"{out_prefix}_{sheet.replace(' ', '_')}.png"
            plt.savefig(png_name, dpi=150, bbox_inches="tight")
            pdf.savefig()
            plt.close()

    xlsx_out = results_dir / f"{out_prefix}_percentages.xlsx"
    with pd.ExcelWriter(xlsx_out) as writer:
        for sheet, table in all_t5_percent.items():
            table.to_excel(writer, sheet_name=f"{sheet}_percent")
        if long_rows:
            pd.DataFrame(long_rows).to_excel(writer, sheet_name="All_Percentages_Long", index=False)

    print(f"Saved PDF: {pdf_path}")
    print(f"Saved Excel: {xlsx_out}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--xlsx", required=True, help="Path to input XLSX (multiple sheets).")
    ap.add_argument("--out_prefix", default="T5_Distribution_MF")
    ap.add_argument("--expected_col", default="Expected Gender")
    args = ap.parse_args()
    main(args.xlsx, args.out_prefix, args.expected_col)
