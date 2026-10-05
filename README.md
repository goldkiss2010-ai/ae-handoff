![AE Handoff](branding/key-visual.jpg)

# AE Handoff

**粒子の状態を渡し、After Effectsで制作を続ける。**

AE Handoffは、外部で計算した粒子状態をFLD1で受け取り、After Effects内で再構成・投影・描画するプレビュー版プラグインです。

シミュレーションや手続き生成は外部で行い、**時間・視点・色・サイズ・密度・合成はAE側に残す**ことを目的にしています。Pythonは付属生成ツールの実装言語であり、FLD1やAE Handoffの必須条件ではありません。

AE Handoffは [DCC Handoff](https://github.com/goldkiss2010-ai/dcc-handoff) のAfter Effects実装です。同じFLD1を読む [Fusion Handoff](https://github.com/goldkiss2010-ai/fusion-handoff) も開発しています。

## 1.15 Preview

現在の公開版は **AE Handoff 1.15** です。

| Platform | Package | Status |
|---|---|---|
| Windows x64 | [AEHandoff_1.15_Windows_x64_preview.zip](https://github.com/goldkiss2010-ai/ae-handoff/releases/download/v1.15-preview.1/AEHandoff_1.15_Windows_x64_preview.zip) | ビルド・AE基本動作・View Depth Split確認済み |
| macOS Apple Silicon | [AEHandoff_1.15_macOS_arm64_test.zip](https://github.com/goldkiss2010-ai/ae-handoff/releases/download/v1.15-preview.1/AEHandoff_1.15_macOS_arm64_test.zip) | arm64ビルド済み。1.14でM4 Pro / AE 26.5基本動作確認、1.15実機確認を継続 |

[1.15 release notes](docs/release-notes-1.15-preview.md) · [Windows導入](docs/installation.md) · [macOS導入](docs/installation-macos.md) · [粒子場ダウンロード](docs/downloads.md)

## 何をしているか

```text
Python / C++ / solver / procedural generation
                    |
                    | particle state
                    v
                   FLD1
                    |
                    v
               AE Handoff
                    |
      +-------------+-------------+
      |             |             |
 interpolation   3D view      rasterization
      |             |             |
      +-------------+-------------+
                    |
                    v
               RGBA frame
                    |
                    v
          normal AE composition
```

AEから見ると1つのエフェクト／レイヤーですが、内部ではFLD1の3D粒子状態を読み、Hermite補間、3D変換、透視投影、粒子・ストリークのラスタライズを行っています。

100万粒子を100万個のAEオブジェクトへ展開する方式ではありません。

## 使う・作り替える・持ち込む

1. **使う** — プラグインと完成済みFLD1だけで制作します。Python、Visual Studio、AE SDKは不要です。
2. **作り替える** — 付属の生成コードを変更し、新しいFLD1を書き出します。
3. **持ち込む** — 任意の言語・ソルバー・解析コードからFLD1を書き出します。

生成方法は、解析式、物理シミュレーション、画像由来の点群、手続き生成など自由です。

## Quick start

1. OSに合う1.15 ZIPを取得してプラグインをインストールします。
2. AEでコンポジションサイズの平面を作り、**AE Handoff**を適用します。
3. 最上段の **Select File** からFLD1を選びます。
4. 付属の `orbit-sample-index.fld1` なら、Mode=Dot、Samples / Second=12、Sample Offset=0で0〜2秒の円運動を確認できます。
5. Rendering / Playback / Viewの値をAE側で変更します。

FLD1はフッテージとして読み込む必要はありません。キャッシュ本体は.aepへ埋め込まれないため、制作データと一緒に保管してください。

## 表示機能

現在の主要な表示機能：

- Dot / Sprite / Image Dots
- Density
- Particle Size / Color / Opacity
- Speed Brightness
- Depth Cue
- Velocity Streak
- Object Position / Pivot / Rotation
- Perspective / View Scale / Dolly / Screen Offset
- Samples / Second / Sample Offset
- **View Depth Split: Off / Front / Back**
- **Focus Depth**

### View Depth Split

Focus Depthはcamera-space Zを直接指定します。分割面は常に**画面／カメラセンサー面と平行**です。

同じFLD1を読むAE Handoffを2枚用意し、

```text
Back Handoff
2D layer / text / image / person
Front Handoff
```

の順に重ねると、通常のAEレイヤーを粒子群の前後へ挿入できます。

これは完全なZ-bufferや粒子同士の自己遮蔽ではなく、1枚の深度面による表示上の分割です。

## 時間の考え方

新規FLD1は保存サンプル番号

```text
q = 0, 1, 2, ...
```

を状態座標として扱います。AE側では

```text
q = AE time * Samples / Second + Sample Offset
```

として表示時間へ対応させます。

Samples / Second=0にするとSample Offsetを直接キーフレームや式で操作できるため、シミュレーション側の固定時間に制作を拘束されません。

## FLD1

現在の `point3-pv` 基本プロファイルは、1粒子・1保存サンプルにつき8個のfloat32を持ちます。

```text
x y z  vx vy vz  visibility  scalar0
```

右手系XYZ・Z-up、粒子数と粒子順は全サンプルで固定です。新規キャッシュは `sample_rate=1`、速度は保存サンプル番号に対する位置の微分 `dx/dq` とします。

仕様の正本は [FLD1 repository](https://github.com/goldkiss2010-ai/fld1) です。

[固定規約](core/docs/contract-v1.md) · [バイト配置](core/docs/format.md) · [AE側の操作](docs/player-design.md) · [自作アセット](docs/asset-authoring.md)

## FLD1 Asset Pack

確認・制作用の粒子場は、ホスト非依存の1パッケージへ統合しました。

[**FLD1_Asset_Pack_v01.zip**](https://github.com/goldkiss2010-ai/ae-handoff/releases/download/v1.15-preview.1/FLD1_Asset_Pack_v01.zip) — 約494 MiB

収録内容：

| Asset | Particles | Samples | Suggested Samples / Second | Initial Rotation X |
|---|---:|---:|---:|---:|
| Vortex Ring | 20K | 49 | 12 | 0° |
| Smoke Point Source | 20K | 49 | 12 | -75° |
| Ripple Sheet | 20K | 49 | 12 | 15° |
| Wind Tunnel | 20K | 49 | 12 | 0° |
| Plane to Torus | 20K | 49 | 12 | 0° |
| Vortex Ring | 1M | 17 | 4 | 0° |

パック内のREADMEとJSONはAE専用ではなく、FLD1の状態と表示上の推奨値を記述します。同じFLD1をAE Handoff、Fusion Handoff、その他のFLD1 readerで利用できます。

煙・風洞は手続き流れのモデルで、厳密な流体ソルバー結果ではありません。詳しくは [docs/downloads.md](docs/downloads.md) を参照してください。

## 粒子場を生成する

Python 3.10以降とNumPyを使う付属生成例：

```sh
python -m pip install -r assets/requirements.txt
python assets/generators/make_fields.py --asset all --preset quick --out output
python assets/generators/make_fields.py --asset vortex-ring --preset hero --out output
python -m unittest discover -s core/tests -v
python -m unittest discover -s assets/tests -v
```

任意の粒子数・サンプル数・seedは `--count`、`--samples`、`--seed` で指定できます。

## DCC Handoff family

- [DCC Handoff](https://github.com/goldkiss2010-ai/dcc-handoff) — 上位アーキテクチャとcross-hostの設計原則
- [FLD1](https://github.com/goldkiss2010-ai/fld1) — 状態交換フォーマット
- **AE Handoff** — After Effects実装
- [Fusion Handoff](https://github.com/goldkiss2010-ai/fusion-handoff) — Fusion / DaVinci Resolve実装

FLD1はAE専用形式ではありません。AE HandoffもFLD1仕様の正本ではありません。この分離を維持します。

## Distribution and license

AEプラグインはビルド済みバイナリとして配布します。公開パッケージにAdobe SDK、プラグインのC++ソース、非公開の開発履歴は含めません。

コード・文書とプラグインの自作部分はMIT、配布粒子素材はCC0-1.0です。Adobe由来部分はMITの対象外です。

[LICENSE_SCOPE.md](LICENSE_SCOPE.md) · [EULA.md](EULA.md) · [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) · [branding](branding/README.md)

Branding images are not covered by the MIT / CC0 grants.
