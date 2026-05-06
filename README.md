# 日本 観光来訪者数マップ

日本全国の観光来訪者数をインタラクティブに可視化するウェブアプリです。

---

## 機能

- **都道府県コロプレスマップ**：来訪者数の多い都道府県ほど濃い赤で表示
- **2モード切り替え**：来訪者数の絶対数 / 人口あたりの比率をトグルスイッチで切り替え
- **沖縄インセット**：天気予報のように沖縄を左上に独立表示
- **ホバーツールチップ**：都道府県名・来訪者数・人口比を表示
- **市区町村ドリルダウン**：都道府県クリックで市区町村レベルの詳細を表示（実装中）

---

## データ出典

- 観光来訪者数：[デジタル観光統計オープンデータ](https://www.nihon-kankou.or.jp/home/jigyou/research/d-toukei/)（2026年3月利用）
- 都道府県別人口：[総務省 住民基本台帳人口](https://www.soumu.go.jp/main_sosiki/jichi_gyousei/daityo/jinkou_jinkoudoutai-setaisuu.html)（令和7年1月1日現在）
- 都道府県境界：[dataofjapan/land](https://github.com/dataofjapan/land)

---

## ローカルで動かす

```bash
git clone https://github.com/ItalyFuji/japan_tourist-visitors_map.git
cd japan_tourist-visitors_map
python -m http.server 8080
```

ブラウザで `http://localhost:8080` を開く。

> HTMLファイルをダブルクリックで開くとCSVが読み込めないため、ローカルサーバーが必要です。

---

## 技術構成

HTML + CSS + JavaScript（D3.js v7）のみ。フレームワーク・ビルドツール不使用。GitHub Pages でそのまま公開できる静的サイト。

詳細は [SPEC.md](SPEC.md) を参照。
