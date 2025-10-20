import argparse
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pathlib import Path

def main(xlsx_path, out_prefix, expected_col="Expected Gender", pred_col="T1 Predicted Gender"):
    xls = pd.ExcelFile(xlsx_path)
    results_dir = Path("Results")
    results_dir.mkdir(exist_ok=True)

    all_percents = {}

    pdf_path = results_dir / f"{out_prefix}_all.pdf"
    with PdfPages(pdf_path) as pdf:
        for sheet in xls.sheet_names:
            if sheet.lower() in {"stats"}:
                continue

            df = pd.read_excel(xls, sheet_name=sheet)
            df = df.dropna(subset=[expected_col, pred_col]).copy()
            df[expected_col] = df[expected_col].astype(str).str.strip().str.upper()
            df[pred_col] = df[pred_col].astype(str).str.strip().str.lower()

            df = df[df[expected_col].isin(["M", "F"])].copy()
            if df.empty:
                continue

            conf = pd.crosstab(df[expected_col], df[pred_col])
            conf_pct = conf.div(conf.sum(axis=1), axis=0) * 100
            all_percents[sheet] = conf_pct

            ax = conf_pct.plot(kind="bar", stacked=True, figsize=(7, 5), colormap="tab20c")
            plt.title(f"Expected vs T1 Predicted Gender – {sheet}")
            plt.ylabel("Percentage (%)"); plt.xlabel("Expected Gender")
            plt.ylim(0, 100)
            plt.legend(title="T1 Predicted", bbox_to_anchor=(1.05, 1), loc="upper left")

            for container in ax.containers:
                ax.bar_label(container, fmt="%.1f%%", label_type="center", color="white", fontsize=8)

            plt.tight_layout()
            png_path = results_dir / f"{out_prefix}_{sheet.replace(' ', '_')}.png"
            plt.savefig(png_path, dpi=150, bbox_inches="tight")
            pdf.savefig()
            plt.close()

    # Excel with percentages
    xlsx_out = results_dir / f"{out_prefix}_percentages.xlsx"
    with pd.ExcelWriter(xlsx_out) as writer:
        for sheet, table in all_percents.items():
            table.to_excel(writer, sheet_name=f"{sheet}_percent")
        if all_percents:
            combined_pct = pd.concat(all_percents, axis=0)
            combined_pct.to_excel(writer, sheet_name="All_Percentages")

    print(f"Saved PDF: {pdf_path}")
    print(f"Saved Excel: {xlsx_out}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--xlsx", required=True, help="Path to input XLSX (multiple sheets).")
    ap.add_argument("--out_prefix", default="Expected_vs_T1")
    ap.add_argument("--expected_col", default="Expected Gender")
    ap.add_argument("--pred_col", default="T1 Predicted Gender")
    args = ap.parse_args()
    main(args.xlsx, args.out_prefix, args.expected_col, args.pred_col)
