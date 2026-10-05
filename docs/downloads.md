# ダウンロード

[Windows x64プラグインZIP](https://github.com/goldkiss2010-ai/ae-handoff/releases/download/v1.15-preview.1/AEHandoff_1.15_Windows_x64_preview.zip) ·
[macOS Apple Silicon ZIP](https://github.com/goldkiss2010-ai/ae-handoff/releases/download/v1.15-preview.1/AEHandoff_1.15_macOS_arm64_test.zip) ·
[導入手順](installation.md)

## FLD1 Asset Pack

完成済み粒子場は個別ZIPではなく、1つのホスト非依存パッケージに統合しています。

[**FLD1_Asset_Pack_v01.zip**](https://github.com/goldkiss2010-ai/ae-handoff/releases/download/v1.15-preview.1/FLD1_Asset_Pack_v01.zip)

- ZIP size: 517,123,175 bytes（約494 MiB）
- SHA-256: `ce09286cf06acf06e7465b2f310a0145ab4c5589694984ac9fbe23146f755c80`
- License: CC0-1.0

| Asset | Particles | Samples | Suggested Samples / Second | Initial Rotation X |
|---|---:|---:|---:|---:|
| Vortex Ring | 20,000 | 49 | 12 | 0° |
| Smoke Point Source | 20,000 | 49 | 12 | -75° |
| Ripple Sheet | 20,000 | 49 | 12 | 15° |
| Wind Tunnel | 20,000 | 49 | 12 | 0° |
| Plane to Torus | 20,000 | 49 | 12 | 0° |
| Vortex Ring | 1,000,000 | 17 | 4 | 0° |

各フォルダにはFLD1本体、設定・プレビュー等の既存配布物と、ホスト非依存に書き直した日本語／英語READMEを収録しています。設定JSONのAE専用推奨欄も、再パッケージ時に `suggested_playback` / `suggested_view` へ整理しています。

Samples / Secondと初期回転はDCC側の表示例であり、絶対的な上映時間やカメラ姿勢をFLD1へ固定するものではありません。AE Handoff、Fusion Handoff、その他のFLD1 readerで同じ粒子状態を利用できます。

2万粒子版は49サンプル、100万粒子版は17サンプルです。上記の表示速度ではいずれも4秒で終点を保持します。シームレスループ素材ではありません。

煙・風洞は手続き流れのモデルで、厳密な流体ソルバー結果ではありません。

同じ粒子場モデルは[生成手順](../assets/README.md)から再生成できます。異なる生成環境でのバイト一致は保証しません。
