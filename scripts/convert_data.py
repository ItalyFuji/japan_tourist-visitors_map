"""
データ変換スクリプト
====================
以下の変換をまとめて実行する：

1. 観光CSVの文字コード変換（Shift-JIS → UTF-8）
2. 人口ExcelのCSV変換（各年の都道府県合計行を抽出）

使い方:
    cd japan_tourist-visitors_map
    python scripts/convert_data.py
"""

import csv
import os
import glob

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


# ================================================================
# 1. 観光CSV: Shift-JIS → UTF-8 変換
# ================================================================

def convert_tourism_csvs():
    # 変換対象パターン（city2021.csv, city202601.csv など）
    patterns = [
        "city20[0-9][0-9].csv",       # 年単位ファイル（2021〜2025）
        "city2026[0-9][0-9].csv",      # 月単位ファイル（202601〜）
    ]

    converted = 0
    for pattern in patterns:
        for src in sorted(glob.glob(os.path.join(DATA_DIR, pattern))):
            basename = os.path.splitext(os.path.basename(src))[0]
            dst = os.path.join(DATA_DIR, f"{basename}_utf8.csv")

            try:
                with open(src, encoding="shift-jis", errors="replace") as f:
                    content = f.read()
                with open(dst, encoding="utf-8", newline="") as _:
                    pass  # 既存ファイルの確認（不要なら削除可）
            except FileNotFoundError:
                pass  # 既存チェックはスキップ

            try:
                with open(src, encoding="shift-jis", errors="replace") as f:
                    content = f.read()
                with open(dst, "w", encoding="utf-8", newline="") as f:
                    f.write(content)
                print(f"  [観光CSV] 変換完了: {os.path.basename(src)} → {os.path.basename(dst)}")
                converted += 1
            except Exception as e:
                print(f"  [観光CSV] エラー: {os.path.basename(src)} - {e}")

    print(f"  観光CSV: {converted} ファイル変換")


# ================================================================
# 2. 人口Excel: 都道府県合計行を抽出してCSV保存
# ================================================================

def extract_population_from_excel(xlsx_path, csv_path, year):
    """
    人口Excelから都道府県合計行（地域コードXX000X形式）を抽出してCSV保存。
    XX000X = 都道府県コード2桁 + 000 + 検査数字1桁
    """
    try:
        import openpyxl
    except ImportError:
        print("  ⚠ openpyxl が未インストールです: pip install openpyxl")
        return False

    try:
        wb = openpyxl.load_workbook(xlsx_path, read_only=True, data_only=True)
        ws = wb.active

        rows_out = [["都道府県名", "人口", "年"]]
        found = 0

        for row in ws.iter_rows(min_row=7, values_only=True):
            code = str(row[0]).strip() if row[0] else ""
            name = str(row[1]).strip() if row[1] else ""

            # 地域コードの3〜5文字目が "000" = 都道府県合計行
            if len(code) == 6 and code[2:5] == "000" and name:
                # 人口合計（列5 = 計）。数値でない場合はスキップ
                pop_raw = row[4]
                try:
                    pop = int(str(pop_raw).replace(",", "").replace(" ", ""))
                except (ValueError, TypeError):
                    continue
                rows_out.append([name, pop, year])
                found += 1

        wb.close()

        if found == 0:
            print(f"  ⚠ 都道府県行が見つかりません: {os.path.basename(xlsx_path)}")
            return False

        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows_out)

        print(f"  [人口Excel] 変換完了: {os.path.basename(xlsx_path)} → {os.path.basename(csv_path)} ({found}件)")
        return True

    except Exception as e:
        print(f"  [人口Excel] エラー: {os.path.basename(xlsx_path)} - {e}")
        return False


def convert_population_excels():
    converted = 0
    pattern = os.path.join(DATA_DIR, "[0-9][0-9][0-9][0-9]_population_prefecture.xlsx")
    for xlsx_path in sorted(glob.glob(pattern)):
        basename = os.path.basename(xlsx_path)
        year = basename[:4]  # "2026_population_prefecture.xlsx" → "2026"
        csv_path = os.path.join(DATA_DIR, f"population_pref_{year}.csv")
        if extract_population_from_excel(xlsx_path, csv_path, year):
            converted += 1

    print(f"  人口Excel: {converted} ファイル変換")


# ================================================================
# メイン処理
# ================================================================

if __name__ == "__main__":
    print("データ変換を開始します...\n")

    print("【観光CSV 文字コード変換】")
    convert_tourism_csvs()

    print("\n【人口Excel → CSV変換】")
    convert_population_excels()

    print("\n完了しました。")
    print(f"出力先: {os.path.abspath(DATA_DIR)}")
