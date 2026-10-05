# AE Handoff 1.15 — macOS / Apple Silicon プレビュー版

FLD1をAfter Effectsで描画する1.15 Mac移植版です。Apple Silicon（M1以降）向けのarm64ビルドで、Intel Macには対応していません。
プラグインは `AEHandoff.plugin`、粒子場のFLD1と設定説明JSONはWindows版と共通です。変換は不要です。

## 動作確認環境

1.14は2026-10-05に以下の環境で基本動作を確認済みです。1.15 arm64ビルドも作成済みで、View Depth Split / Focus Depthを含む実機確認を継続しています。

| 項目 | 確認環境 |
|---|---|
| チップ | Apple M4 Pro |
| macOS | Tahoe 26.5.1 |
| After Effects | 26.5 |
| 結果 | 基本動作確認済み。初回に「プライバシーとセキュリティ」で個別許可を実施 |

その他の環境は未検証です。すべてのモード、保存・再起動後の参照復元、Undo/Redo、長時間の安定性まで確認済みという意味ではありません。
ビルド下限はmacOS 12.0ですが、利用するAE本体の対応OSも満たす必要があります。

## インストールと初回許可

この版はアドホック署名で、Developer ID署名・Appleの公証は未実施です。
そのため、初回にmacOSがプラグインをブロックし、AEの起動が途中で止まる場合があります。
提供元とファイルを確認し、このテスト版を利用する場合は次の手順で個別に許可してください。

1. AEを終了し、プラグインZIPをFinderで展開します。
2. `AEHandoff.plugin` を、使用するAEのPlug-insフォルダへ丸ごとコピーします。内部のファイルだけを取り出さないでください。

   AE 2026の標準インストール先の例：

   ```text
   /Applications/Adobe After Effects 2026/Plug-ins/AEHandoff.plugin
   ```

   コピーは1個だけにします。以前にEffectsなどのサブフォルダへ入れたコピーも確認してください。
3. AEを起動します。「AppleではAEHandoff.pluginを検証できない」という警告が出た場合は「完了」を押します。
4. AEを終了します。応答しなければ、Command＋Option＋EscでAfter Effectsを強制終了します。
5. Mac画面左上のAppleメニュー → **システム設定** → **プライバシーとセキュリティ**を開きます。AE内の設定ではありません。
6. 下へスクロールし、AEHandoffのブロック表示にある「このまま開く」を選んで認証します。再確認が出たら内容を確認して「開く」を選びます。
7. プラグインを置いたまま、AEを起動し直します。

「このまま開く」が表示されない場合や、異なる警告が出る場合は、警告の全文とmacOS・AEのバージョンを報告してください。
この手順は対象ソフトウェアの個別許可です。Mac全体のセキュリティ機能を無効化する必要はありません。

[Apple公式：Macでアプリを安全に開く](https://support.apple.com/ja-jp/102445)

## 最初の描画確認

1. コンポジションとコンポジションサイズの平面を作り、平面にAE Handoffを適用します。
2. Select Fileから確認用の `orbit-sample-index.fld1` を選びます。FLD1をフッテージとして読み込む必要はありません。
3. Mode=Dot、Samples / Second=12、Sample Offset=0にし、0〜2秒の円運動を確認します。
4. 回転、粒子サイズ、Densityを変更して確認します。

FLD1はPlug-insへ入れる必要はありません。制作データと一緒に保管してください。
公開済みの粒子場も共通で使えます。推奨設定は[ダウンロード案内](downloads.md)を参照してください。
Windowsで保存したプロジェクトをMacへ移す場合、キャッシュのパスはSelect Fileで選び直します。

## 起動を元に戻す・アンインストール

AEを終了して `AEHandoff.plugin` をPlug-insの外へ丸ごと移動し、AEを起動します。
Effectsなどの既存フォルダ自体は削除しないでください。
警告が残る場合は、Effects内や共通のMediaCoreフォルダなどに別のコピーがないか確認します。

```text
/Library/Application Support/Adobe/Common/Plug-ins/7.0/MediaCore
```

AEの再インストールだけでは、残っているプラグインが取り除かれない場合があります。
不具合の報告には、Macのチップ・macOS・AEの版、操作と警告文を添えてください。


## 1.15の追加確認

1.15ではView Depth Split / Focus Depthを追加し、独立したMask Gateを廃止しました。
基本描画を確認した後、View Depth SplitをFront / Backへ切り替え、Focus Depthで画面平行の分割面が前後へ移動することを確認してください。
