# AE Handoff 1.14 — Windows x64 Preview

From computation to composition.

FLD1に保存した粒子場をAfter Effectsで描画し、時間・視点・色・サイズ・合成を編集するWindows x64試験版です。
完成キャッシュの利用にPython・Visual Studio・Adobe SDKは不要です。

- プラグインZIP：AEHandoff.aex、導入手順、小さなOrbit、利用条件・第三者表示。
- 確認用5素材：Vortex Ring、一点から湧く煙、Ripple Sheet、Wind Tunnel、Plane to Torus。各2万粒子・49サンプル。
- 目玉：Vortex Ring 100万粒子・17サンプル（ZIP約410 MB）。

## 初期設定

Mode=Dot、Density=100%、Sample Offset=0。
確認用5素材はSamples / Second=12、100万粒子版は4。
煙のRotation X=-75°、Ripple SheetはX=15°、その他は0°。他の表示設定は既定値から始めます。
上記では4秒で終点を保持します。Orbitは12 samples/secondで2秒です。自動ループはありません。
JSONは説明用で、設定をAEへ自動適用するファイルではありません。

## 確認範囲と制約

Windowsでのビルドと、配布プラグインのAE基本動作は2026-10-04に作者確認済みです。
AE・Windowsの詳細な版番号、保存後の再起動・参照復元、Undo/Redo、別PC、各素材の描画確認は継続中です。
Mac版プラグインは未提供です。FLD1と生成ツールはAE以外の受け取り側にも利用できます。

解析式・幾何変形・手続き流れによる作例です。煙・風洞は厳密な流体ソルバーの結果ではありません。
キャッシュ本体は.aepへ埋め込まれません。別PCではキャッシュも保管・移動し、再選択してください。

## 利用条件

自作コード・文書・プラグインの自作部分はMIT。付属FLD1・設定JSON・PNG／MP4はCC0-1.0。
Adobe SDK由来部分はMITの対象外です。各ZIPの利用条件・第三者表示を参照してください。
プラグインソース・ビルド設定・開発履歴は収録しません。
FLD1仕様・参照実装：https://github.com/goldkiss2010-ai/fld1
