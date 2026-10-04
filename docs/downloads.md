# ダウンロード

[Windows x64プラグインZIP](https://github.com/goldkiss2010-ai/ae-handoff/raw/refs/heads/main/downloads/AEHandoff_1.14_Windows_x64_preview.zip) · [導入手順](installation.md)

WindowsビルドとAEでの基本動作は2026-10-04に作者確認済みです。Mac版は未提供です。

## 完成粒子場

個別ZIPを準備済みです。大容量キャッシュは[Releases](https://github.com/goldkiss2010-ai/ae-handoff/releases)への掲載を準備中です。

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

掲載前でも、[生成手順](../assets/README.md)で同じ粒子場モデルを生成できます。異なる生成環境でのバイト一致は保証しません。
