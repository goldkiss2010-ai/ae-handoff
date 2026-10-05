# AE配布版の操作と設計

## キャッシュの参照

AE Handoff 1.15では、最上段のAE HandoffにMode、Select File、
File Info、Refresh FileとSprite / Image Dots関連の設定をまとめています。独立したMask Gateは表示・評価しません。
任意の名前・場所のFLD1を選び、各エフェクトのプロジェクトデータに参照を保存します。
ファイル本体は埋め込みません。別PCではキャッシュを同梱し、Choose...で再選択します。
相対参照、自動探索、Collect Filesへの自動収集は今後の課題です。

参照保存にはArbitrary Data Parameterの11種のコールバックを実装しています。
ダイアログはユーザー操作時だけ開きます。WindowsビルドとAEでの基本動作は作者確認済みです。
保存・再起動、複製、Undo/Redo、別PCの確認は継続中です。
プラグインはビルド済み.aexの別パッケージで提供する方針です。
プラグインのソース・ビルド設定・開発履歴は公開用の配布物には含めません。

## 時間操作

新規エフェクトの保存サンプル番号は、
`AE時間 × Samples / Second + Sample Offset`です。
小数値は位置をHermite補間し、範囲外は端点保持します。自動ループはありません。
通常再生はSamples / Secondで指定します。
直接キーフレームや式で進行を指定する場合はSamples / Second=0とし、Sample Offsetを操作します。
専用のCache Position欄と時間モード選択は表示しません。
Samples / Second自体のアニメーションは現在値と時刻の積であり、速度の時間積分ではありません。

配布用の新規FLD1はsample_rate=1、微分は保存サンプル番号基準です。
旧キャッシュも読取時の補間間隔換算で扱います。
速度による明るさとストリークは現在、キャッシュ進行座標に対する速度を使用し、
再生時間への対応の微分は掛けません。正規化で速度値が変わると見た目も変わり得ます。

## 空間と表現

保存位置は生成側の座標。配置・回転・ピボット・視点・投影は表示側が持ちます。
現在の視点操作はプラグイン独自のもので、AEネイティブカメラ連携とは区別します。
描画モードはDot / Sprite / ImageDots。RenderingはPlaybackの前に置き、
粒子数の操作はDensityに集約しています。Densityはキャッシュの粒子を削除しません。


## View Depth Split

View Depth SplitはOff / Front / Backの3状態です。Focus Depthはcamera-space Zを直接指定し、
分割面は常にカメラのセンサー面／画面と平行です。X/Y位置は持ちません。
粒子は通常の配置・ピボット・回転・視点変換後のcamera-space ZでFront / Backへ分類されます。

同じFLD1を読むAE Handoffを2枚用意し、一方をBack、もう一方をFrontにして、その間へ通常のAEレイヤーを置くと、
粒子群の前後へ2D素材を挿入できます。これは完全なZ-bufferや粒子同士の遮蔽ではなく、
1枚の深度面による表示上の分割です。
