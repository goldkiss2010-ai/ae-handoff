# AE Handoff 1.15 — Windows x64 Preview

From computation to composition.

1.15はWindows x64向けのプレビュー更新です。FLD1の粒子場をAE内で描画し、
時間・視点・色・サイズ・合成を編集する基本構成は1.14を継承します。

## 1.15の変更

- View Depth Splitを追加しました。Off / Front / Backで表示側を選べます。
- Focus Depthを追加しました。camera-space Zを1値で指定し、分割面は常に画面／カメラセンサー面と平行です。
- 同じFLD1を読むBackとFrontのAE Handoffの間へ通常のAEレイヤーを置き、粒子群の前後へ2D素材を挿入できます。
- 独立したMask Gate / Mask Source / Mask Threshold / Mask Invertは廃止しました。
- 旧Maskの保存IDと登録スロットは既存プロジェクト互換のため非表示で保持します。

View Depth Splitは完全なZ-bufferや粒子同士の遮蔽ではなく、1枚の深度面による表示上の分割です。

## 検証

2026-10-05に作者環境でWindows x64ビルド、AE基本動作、View Depth Split、Focus Depthを確認済みです。
配布ZIP内のAEHandoff.aexは確認済みビルドと同一です。

Windows版ZIP：
[AEHandoff_1.15_Windows_x64_preview.zip](https://github.com/goldkiss2010-ai/ae-handoff/releases/download/v1.14-preview.1/AEHandoff_1.15_Windows_x64_preview.zip)

macOS Apple Silicon版は現在1.14です。FLD1キャッシュはWindows / Macで共通です。
