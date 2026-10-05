# 粒子場アセット — 新規制作 v01

生成コード、設定、参照画像を収録しています。完成FLD1は、ホスト非依存の `FLD1_Asset_Pack_v01.zip` または再生成で用意します。
生成コードはMIT、配布する粒子場・設定JSON・PNG／MP4プレビューはCC0-1.0です。
FLD1アセット自体はAE専用ではなく、AE Handoff、Fusion Handoff、その他のFLD1 readerで利用できます。
.aexや.aepはアセットパックに含みません。

## 収録アセット

| アセット | 内容 | 確認用データ | 初期回転XYZ（度） |
|---|---|---|---|
| Vortex Ring | 波打つトーラス内の循環と断面の旋回 | 2万粒子・49サンプル | 0, 0, 0 |
| Smoke Plume | 一点から順次発生して湧き上がる煙 | 2万粒子・49サンプル | -75, 0, 0 |
| Ripple Sheet | 平面点群の進行波、たなびき | 2万粒子・49サンプル | 15, 0, 0 |
| Wind Tunnel | 円柱を避ける流れと、後方の揺れる流れ | 2万粒子・49サンプル | 0, 0, 0 |
| Plane to Torus | 同じ点群が平面からトーラスへ変形 | 2万粒子・49サンプル | 0, 0, 0 |

[settings](settings/)に、seed、環境、座標範囲、微分の規約、表示上の推奨値、SHA-256を記録したJSONがあります。
生成するとキャッシュの隣にもJSONを保存します。
JSONは説明用で、DCCへ設定を自動適用するものではありません。
2026-10-04の作者確認に基づき、煙はX=-75°、Ripple SheetはX=15°、他の表示設定はプラグイン既定値を初期設定とします。
[一覧画像](previews/overview.png)と各PNGを参照してください。MP4は粒子場の個別配布ZIPに同梱します。
プレビューは完成FLD1から一部の粒子を抽出した参照描画で、AEの出力ではありません。

目玉の**100万粒子Vortex Ring・17サンプル**は、生成コマンドまたは統合済みの`FLD1_Asset_Pack_v01.zip`で用意します。
解凍後のFLD1は544,000,032バイト（約544MB）。確認用との座標・進行範囲は揃えています。
同じseedで粒子数を増やしても、既存の先頭粒子の対応を保ちます。
サンプル数が異なる版はSamples / Secondも揃えて換算してください。

## DCC側での最初の表示例

1. AE HandoffまたはFusion Handoffで好きなFLD1を選択します。
2. Dot表示から始め、Density=100%、Speed Brightness=0、Velocity Streak=0を初期値の目安とします。
3. 確認用はSamples / Second=12、Sample Offset=0。100万粒子版は4と0です。
4. 煙はRotation X=-75°、Ripple SheetはX=15°を初期姿勢の目安とします。Y/Zと他の素材の回転は0°です。
5. その他の表示設定は各host adapterの既定値から始めます。色・サイズ・View Scaleなどの調整は任意です。

推奨設定では4秒で終点に達して保持します。シームレスループ素材ではありません。
時間はFLD1に固定していません。Samples / Second=0としSample Offsetを
0からF-1へ動かせば、任意の時間配分で再生できます。
表示速度や初期姿勢はDCC側の推奨例であり、FLD1そのものに固定されません。

### 平面からトーラスへの画像変形

Plane to Torusの最初のサンプルはXY平面です。Mode=ImageDotsとし、
Image Sourceに画像レイヤーを指定すると、初期位置に基づいた画像の点群を立体へ変形させる入口になります。
現行のマッピングは初期XY範囲であり、粒子ごとの任意UVをFLD1に保存する機能ではありません。
縦横比や向きはAEで確認・調整してください。これは実機未確認の使用例です。

## 生成方法と物理的な意味

Vortex RingとRipple Sheetは解析式、Plane to Torusは幾何学的な対応による変形です。
Smoke Plumeは原点から粒子が順次発生する手続きモデルです。発生前は原点に静止・非表示とし、
発生後は上昇流れと粒子ごとの分散で広がります。密度・浮力・圧力は解きません。
発生時点は粒子IDごとに固定し、再利用しません。位置と微分の立ち上がりを滑らかにしています。
visibilityの連続値をどのように描画へ反映するかはreader側の実装事項です。
Wind Tunnelは円柱まわりのポテンシャル流れと、手続き的な非定常流れの組み合わせです。
後流の揺れはNavier–Stokesから計算したカルマン渦ではなく、CFDや実験との定量比較には使えません。
粒子移流にはRK4を使用します。粒子の途中再生成やIDの再利用はありません。

これらは粒子場の編集と制作を試すための素材です。実際の流体ソルバーによる煙・風洞は別の追加課題です。

## 生成コードを使う

Python 3.10以降とNumPyを使用します。CUDA・PyTorchは不要です。
`ae-handoff`フォルダから実行します。coreには参照ツールの実体を収録しており、サブモジュール取得は不要です。NumPy 2.3.5 / Python 3.12.14で今回生成しました。
実際の生成環境は各JSONに記録しています。異なる環境でのバイト一致は保証しません。

```sh
python -m venv .venv
```

Windowsでは次のように仮想環境内のPythonを直接指定できます。

```bat
.venv\Scripts\python.exe -m pip install -r assets\requirements.txt
.venv\Scripts\python.exe assets\generators\make_fields.py --asset all --preset quick --out output
.venv\Scripts\python.exe assets\generators\make_fields.py --asset vortex-ring --preset hero --out output
```

macOS / Linuxは`.venv/bin/python`を使います。
任意の粒子数・サンプル数は`--count`、`--samples`、seedは`--seed`で変更できます。
同名の成果物を上書きする場合は`--overwrite`を指定します。
3百万粒子までを現在のAE読取上限に合わせています。

49サンプルなら推奨12サンプル/秒、17なら4です。
保存した微分は常にサンプル番号基準に換算し、sample_rate=1で出力します。
サンプル数を増やすと位置の補間精度と容量が変わります。演算モデル内の進行範囲は同じです。
元の設定を再現するにはJSONのcount・samples・seedをコマンドに指定してください。

テスト：`python -m unittest discover -s assets/tests -v`。
プレビューを再生成する場合だけPillowとffmpegを追加し、
`python assets/generators/preview_fields.py output --out previews`を実行します。
既存のFLD1をAEで使う場合は、これらの生成環境は不要です。

## 同梱ファイルの扱い

大容量のFLD1はGitHub Releaseの `FLD1_Asset_Pack_v01.zip` でまとめて配布します。Gitへ完成キャッシュを直接追加することは想定していません。
制作に使う元画像などの第三者素材は含みません。
[ライセンスの適用範囲](../LICENSE_SCOPE.md)を参照してください。
CC0素材は商用利用・改変・再配布が可能で、クレジットは不要です。
生成ツールのMITは、利用者の新しい出力を自動的にCC0にはしません。
出力のライセンスは権利者が決めます。指定しない場合、JSONのasset_licenseはnullです。
自分が権利を持つ出力をCC0にする場合は`--asset-license CC0-1.0`を指定します。

公開パックの容量を抑えるため、100万粒子の完成版は17サンプルです。
`--samples 33`で33サンプル版（FLD1本体約1.06GB、推奨8サンプル/秒）を生成できます。
