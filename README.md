![AE Handoff — From computation to composition.](branding/key-visual.jpg)

# AE Handoff

**粒子の状態を渡し、After Effectsで制作を続ける。**

FLD1に保存した粒子場をAEで描画し、時間・視点・色・サイズ・合成を編集します。
数式、シミュレーション、画像からの点群、手続き生成など、生成方法は自由です。
Pythonは付属の生成ツールの実装言語であり、FLD1の必須条件ではありません。

AE Handoff 1.14のWindows x64試験版・macOS Apple Siliconプレビュー版、使い方、SDK非依存の粒子場生成ツールを提供します。
AEプラグインはビルド済みバイナリを別パッケージで配布します。
プラグインのC++ソース、ビルド設定、Adobe SDK、非公開の開発履歴は含めません。

## 使う・作る・持ち込む

1. **使う**：プラグインと完成済みFLD1を用意し、AEで制作します。Python・Visual Studio・SDKは不要です。
2. **作り替える**：付属の粒子場生成コードを変更し、新しいFLD1を書き出します。
3. **持ち込む**：任意の言語・ソルバーからFLD1を書き出します。AEプラグインのソースは不要です。

## AEで始める

[Windows x64プラグインZIP](https://github.com/goldkiss2010-ai/ae-handoff/raw/refs/heads/main/downloads/AEHandoff_1.14_Windows_x64_preview.zip)をダウンロードし、
[導入手順](docs/installation.md)に従って`AEHandoff.aex`をインストールします。
平面にAE Handoffを適用し、最上段のSelect FileでFLD1を選択します。
`samples/orbit-sample-index.fld1`は128粒子・25サンプルの小さな確認用です。
Mode=Dot、Samples / Second=12、Sample Offset=0で、0〜2秒の円運動を確認できます。
ファイルを選ぶまで描画は透明です。FLD1は制作データと一緒に保管してください。

[粒子場のダウンロード案内](docs/downloads.md)に個別パッケージと推奨設定を記載しています。
大容量キャッシュは[Releases](https://github.com/goldkiss2010-ai/ae-handoff/releases/tag/v1.14-preview.1)から取得できます。生成ツールでも同じモデルのFLD1を作れます。
配布済みキャッシュだけを使う場合、下記の生成環境は不要です。
Mac版はApple Silicon向けプレビュー版を実機で基本動作確認済みです（M4 Pro / macOS Tahoe 26.5.1 / AE 26.5、2026-10-05）。
[Mac版の導入・初回許可の手順](docs/installation-macos.md)を参照してください。[Mac用ZIP](https://github.com/goldkiss2010-ai/ae-handoff/releases/download/v1.14-preview.1/AEHandoff_1.14_macOS_arm64_test.zip)を公開しました。
Mac用ZIPを展開して、`AEHandoff.plugin`とREADMEを取り出してください。
FLD1はWindows・Macで共通です。

## 配布用の粒子場

[アセットの説明](assets/README.md)に生成方法、初期表示、モデルの限界を記載しています。

| 素材 | 最初のRotation X |
|---|---:|
| Vortex Ring | 0° |
| Smoke Plume（一点から発生） | -75° |
| Ripple Sheet | 15° |
| Wind Tunnel | 0° |
| Plane to Torus | 0° |

他の表示設定はプラグイン既定値から始めます。確認用2万粒子・49サンプルは
Samples / Second=12、100万粒子Vortex Ring・17サンプルは4で、いずれも4秒で終点に達します。
付属JSONは説明用で、AEの設定へ自動適用されません。
煙・風洞は手続き流れのモデルで、厳密な流体ソルバーの結果ではありません。

## 粒子場を生成する

Python 3.10以降とNumPyを使用します。ZIPにはFLD1参照ツールを`core/`に収録しているため、
サブモジュールの取得は不要です。このフォルダのルートで実行します。

```sh
python -m pip install -r assets/requirements.txt
python assets/generators/make_fields.py --asset all --preset quick --out output
python assets/generators/make_fields.py --asset vortex-ring --preset hero --out output
python -m unittest discover -s core/tests -v
python -m unittest discover -s assets/tests -v
```

任意の粒子数・サンプル数・seedは`--count`、`--samples`、`--seed`で指定します。
環境の作り方とWindowsの仮想環境のコマンドは[アセットの説明](assets/README.md)を参照してください。
既存キャッシュの検査例：`python core/examples/inspect_cache.py samples/orbit-sample-index.fld1`。

## FLD1の基本規約

`point3-pv`は右手系XYZ・Z-up、全サンプルで粒子数と順序が固定です。
1粒子あたり`x y z vx vy vz visibility scalar0`の8個のfloat32を保存します。
新規キャッシュはsample_rate=1、速度欄は保存サンプル番号に対する位置の微分です。
秒への対応はAE側で決めます。通常再生はSamples / SecondとSample Offsetを使います。

[固定規約](core/docs/contract-v1.md)・[バイト配置](core/docs/format.md)・
[AE側の操作](docs/player-design.md)・[自作アセット](docs/asset-authoring.md)・
[提案の方針](CONTRIBUTING.md)を参照してください。

[FLD1リポジトリ](https://github.com/goldkiss2010-ai/fld1)で仕様・参照ツール・将来の検討を管理します。
このリポジトリにはその参照ツールと粒子場生成コードを収録しています。
AEプラグイン本体のソース公開と改造版のビルドは、今回の配布範囲には含めません。
コード・文書とプラグインの自作部分はMIT、配布素材はCC0-1.0です。
[適用範囲](LICENSE_SCOPE.md)、[MIT本文](LICENSE)、[CC0本文](LICENSES/CC0-1.0.txt)、
[プラグインの利用条件](EULA.md)、[第三者の表示](THIRD_PARTY_NOTICES.md)を参照してください。
Adobe由来部分はMITに含めず、プラグイン全体をオープンソースとは表示しません。
提供されたSDK表示一覧（99ファイル・44表示）の照合と同梱を完了しました。
SDKや依存先を変更する場合は、第三者表示も更新します。
