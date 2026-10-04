# ライセンスの適用範囲

2026-10-04に、権利者Bungaku Yokotaが以下の対象についてライセンスを確定しました。
プラグインソースと過去の開発履歴は非公開で維持します。本リポジトリは公開対象のみの新しい履歴です。

| 対象 | 条件 |
|---|---|
| FLD1仕様・参照コード・付属文書 | MIT。core/LICENSEを参照 |
| assets/generators、assets/tests、toolsの自作コード | MIT。LICENSEを参照 |
| README、CONTRIBUTING、docs、assets/README、distributionの自作文書 | MIT |
| この配布物のassets/settingsのJSON、samplesのFLD1とJSON、assets/previewsのPNG／MP4 | CC0 1.0 Universal |
| 配布用の完成粒子場FLD1、その付属設定JSON、PNG・MP4プレビュー | CC0 1.0 Universal |
| 配布済みAEHandoff.aexのBungaku Yokotaによる自作部分 | MIT。EULA.mdとTHIRD_PARTY_NOTICES.mdも参照 |
| plugin/以下の非公開ソース・ビルド設定、開発履歴 | 今回の公開許諾の対象外 |
| branding/のロゴ・キービジュアル | MIT・CC0の対象外。branding/README.mdを参照 |
| Adobe SDK由来部分・第三者のコードや素材 | 上記MIT・CC0の対象外。各権利者の条件が適用 |

## コードと素材

MITは商用利用・改変・再配布を許可します。コードやソフトウェアのコピーを配布するときは、
著作権表示とMITライセンス文を残してください。ソース公開の義務はありません。
ツールを使って制作した映像に、MITライセンス文を表示する義務はありません。

CC0の対象素材は、商用映像への使用・加工・再配布に作者のクレジットを要求しません。
Bungaku Yokotaは上記の配布素材について、保有する著作権および関連する権利を
CC0 1.0 Universalに従って放棄します。許されない法域では同条項の代替ライセンスが適用されます。
全文はLICENSES/CC0-1.0.txt、正式URLはhttps://creativecommons.org/publicdomain/zero/1.0/です。
権利放棄は原則として撤回できません。第三者の権利や商標・特許には適用しません。

## 利用者が新しく作るデータ

生成ツールのMITライセンスは、その出力を自動的にCC0にするものではありません。
利用者が生成・持ち込む新しい素材のライセンスは、その権利者が決めます。
付属ジェネレーターは指定がない場合、出力のasset_licenseをnullとします。
自分が許諾権限を持つ素材をCC0として書き出す場合に限り、--asset-license CC0-1.0を指定できます。
既存配布キャッシュと設定にはCC0-1.0を明記しています。

## プラグインとAdobe SDK

プラグインのMIT許諾は自作部分についてのみ行います。Adobeのサンプル、ヘッダー、
補助実装などをMITへ変更したり、そのソースの再配布権を与えたりするものではありません。
SDK本体とプラグインのソースは配布しません。Adobeの必要な表示は別途保持します。
プラグイン全体をオープンソースと表示しません。

コード・素材・自作プラグイン部分のライセンス選択は完了しています。
提供されたSDK表示一覧の照合と原文同梱は完了しました。THIRD_PARTY_NOTICES.mdの
確認範囲を参照してください。公開・配布方法と残る実機確認は別途決めます。
