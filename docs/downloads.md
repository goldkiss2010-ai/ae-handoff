# ダウンロード

[Windows x64プラグインZIP](https://github.com/goldkiss2010-ai/ae-handoff/releases/download/v1.14-preview.1/AEHandoff_1.15_Windows_x64_preview.zip) · [導入手順](installation.md)

Windows版1.15は2026-10-05にビルド、AE基本動作、View Depth Split、Focus Depthを作者確認済みです。Mac版1.15（Apple Silicon）はarm64ビルド済みです。1.14は2026-10-05にM4 Pro / macOS Tahoe 26.5.1 / AE 26.5で基本動作確認済みです。
[Mac版の導入・初回許可の手順](installation-macos.md)を参照してください。[Mac用ZIP](https://github.com/goldkiss2010-ai/ae-handoff/releases/download/v1.14-preview.1/AEHandoff_1.15_macOS_arm64_test.zip)を公開しました。
Mac用ZIPを展開して、`AEHandoff.plugin`とREADMEを取り出してください。
粒子場のFLD1はWindows・Mac共通です。

## 完成粒子場

個別ZIPは[Releases](https://github.com/goldkiss2010-ai/ae-handoff/releases/tag/v1.14-preview.1)からダウンロードできます。

| ZIP | 容量（約MB） | Samples / Second | Rotation X |
|---|---:|---:|---:|
| `AEHandoff_VortexRing_20K_v01.zip` | 27.8 | 12 | 0° |
| `AEHandoff_SmokePointSource_20K_v01.zip` | 12.7 | 12 | -75° |
| `AEHandoff_RippleSheet_20K_v01.zip` | 18.6 | 12 | 15° |
| `AEHandoff_WindTunnel_20K_v01.zip` | 22.2 | 12 | 0° |
| `AEHandoff_PlaneToTorus_20K_v01.zip` | 26.2 | 12 | 0° |
| `AEHandoff_VortexRing_1M_v01.zip` | 409.6 | 4 | 0° |

2万粒子版は49サンプル、100万粒子版は17サンプルです。Sample Offset=0とし、上記設定では4秒で終点を保持します。
その他の表示設定は既定値から始めます。設定JSONは説明用で、AEへの自動適用ではありません。
各ZIPにFLD1、JSON、参照プレビュー、CC0本文、チェックサムを同梱します。既存キャッシュの再生にPythonやSDKは不要です。

また、[生成手順](../assets/README.md)で同じ粒子場モデルを生成できます。異なる生成環境でのバイト一致は保証しません。
