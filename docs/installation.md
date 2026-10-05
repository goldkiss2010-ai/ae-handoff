# AE Handoff 1.15 — Windows x64 試験版

Mac版（Apple Silicon）の導入は[Mac用の手順](installation-macos.md)を参照してください。

FLD1に保存した粒子状態をAfter Effectsで描画し、時間・視点・色・サイズ・合成を編集します。
このZIPにはビルド済みプラグインと、小さな確認用キャッシュを収録しています。
既存キャッシュの再生には、Python、Visual Studio、AE SDKは不要です。

Windows x64の試験版です。1.15は2026-10-05に作者環境でビルドし、AE基本動作、View Depth Split、Focus Depthを確認済みです。
1.15では独立したMask Gateを廃止し、View / Cameraに画面平行の深度分割を追加しました。
対応するAEの版の範囲、保存・再起動、別PCでの動作は継続確認項目です。

## インストール

1. After Effectsを終了します。
2. ZIPを解凍します。
3. 次の場所にAEHandoffフォルダを作り、`AEHandoff.aex`をコピーします。

   ```text
   C:\Program Files\Adobe\Adobe After Effects <使用するバージョン>\Support Files\Plug-ins\AEHandoff\AEHandoff.aex
   ```

   After Effectsを別の場所へインストールしている場合は、そのSupport Files\Plug-insを使用します。
   Program Filesへのコピー時には、Windowsから管理者の確認を求められる場合があります。
4. 更新の場合は、既存のAEHandoff.aexを置き換えます。同じエフェクトの複数コピーを置かないでください。
5. After Effectsを起動し、エフェクト検索で「AE Handoff」を探します。

確認用FLD1はPlug-insへ入れる必要はありません。制作データと一緒に保管してください。
アンインストールはAEを終了し、コピーしたAEHandoff.aexを取り除きます。

## ランタイム

このバイナリはMicrosoft Visual C++ランタイムを使用します。
MSVCP140.dll、VCRUNTIME140.dll、VCRUNTIME140_1.dllの不足や、プラグインの読み込み失敗が
発生した場合は、Microsoft公式のVisual C++ v14再頒布可能パッケージ（x64）を導入してください。
使用するランタイムはビルド時のツールセットと同じか新しい版が必要です。

- 公式の説明：https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist/
- 公式のx64版：https://aka.ms/vc14/vc_redist.x64.exe

## 最初の確認

1. 1920×1080などのコンポジションを作り、コンポジションサイズの平面にAE Handoffを適用します。
2. 最上段のAE Handoff → Select File → Choose...で、
   `samples/orbit-sample-index.fld1`を選択します。FLD1をAEのフッテージとして読み込む必要はありません。
3. ModeをDotにします。
4. RenderingはDensity=100%、Size Multiplier=1、Speed Brightness=0、Velocity Streak=0から始めます。
5. PlaybackをSamples / Second=12、Sample Offset=0にします。
6. タイムラインの0〜2秒を移動すると円運動を再生し、2秒以降は終点を保持します。

確認用は128粒子・25サンプルで、流体シミュレーションではありません。
JSONは座標・微分・推奨再生設定の説明です。AEが設定を自動適用するファイルではありません。
キャッシュを選ぶまでは描画が透明です。File Info → Show...で選択情報を確認できます。

## 操作の要点

- 保存サンプル番号 = AE時間 × Samples / Second + Sample Offset。
- Samples / Second=0でSample Offsetをアニメーションさせると、任意の時間配分にできます。
- 密度の調整はRenderingのDensity。ファイル内の粒子数や状態は変わりません。
- 視点・回転・配置・色・サイズはAE側で調整します。視点操作はプラグイン独自のものです。
- 同じパスのFLD1を外部で更新したらRefresh File → Reloadを押します。
- View Depth Split=Front / Backで、画面と平行なFocus Depth面を境に粒子を前後へ分けられます。2枚のAE Handoffの間へ通常のAEレイヤーを置く用途を想定しています。

## キャッシュとプロジェクト

キャッシュ本体は.aepへ埋め込みません。制作時には.aepとFLD1を一緒に保管してください。
別PCではFLD1をコピーし、Choose...で再選択します。自動探索・相対パス解決・Collect Filesへの
自動収集は未実装です。

## 検証記録

- 2026-10-05：1.15のWindows x64ビルド、AE基本動作、View Depth Split、Focus Depthを作者確認済み。
- パッケージ確認：配布ZIP内のAEHandoff.aexは確認済みビルドと同一です。
- 確認用FLD1：ヘッダー・サイズ・全レコードの有限値を検査しました。
- 今後の確認：.aep保存後の再起動・参照復元、複製、Undo/Redo、別PC、各粒子場の見た目。

詳しい版・依存DLL・SHA-256とファイル別ハッシュは、プラグインZIP内のBUILD_INFO.jsonとSHA256SUMS.txtを参照してください。

## 開発と利用条件

自作部分はMIT、付属素材はCC0-1.0です。このZIPは試験版です。対応環境の範囲と残る実機確認は検証記録を参照してください。
大容量の粒子場は別パッケージです。このZIPには.aep、SDK本体、ランタイムのインストーラーを含みません。

- AE Handoff：https://github.com/goldkiss2010-ai/ae-handoff
- FLD1：https://github.com/goldkiss2010-ai/fld1

インストール先の参考：
https://helpx.adobe.com/jp/after-effects/kb/cq02250243.html

## 配布範囲

プラグインはビルド済みWindows x64版で配布する方針です。C++ソース・ビルド設定・
開発履歴は非公開で維持します。FLD1仕様・参照ツール・粒子場生成コードは別の配布対象です。
任意の方法で粒子場を生成してFLD1へ書き出すために、プラグインの改造は不要です。
このパッケージはWindows x64の試験版です。自作部分はMIT、付属素材はCC0-1.0に確定しました。Adobe由来部分は対象外で、提供されたSDK表示一覧の照合を完了し、全44表示を原文で同梱しました。

## ライセンス

プラグインの自作部分はMIT、確認用キャッシュとJSONはCC0-1.0です。
LICENSE、LICENSE_SCOPE.md、LICENSES/CC0-1.0.txt、EULA.md、THIRD_PARTY_NOTICES.mdを参照してください。
Adobe由来部分はMITの対象外です。ソースは非公開のままです。映像への作者クレジットは不要です。
