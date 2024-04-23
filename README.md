## 概要
メッシュで分割された個別の領域の面積を計算し、エクセルファイルに出力するプログラムです。

## 作成の経緯
前世代のプログラムは「Ruby」を用いてフルスクラッチ(0から全て作成)で作成していました。速度の遅いスクリプト言語によるフルスクラッチですので速度が非常に遅いという問題があり、
今回から「Python」を使用し、かつ実行速度の向上のため幾何学計算のパッケージ「Shapely」を使用することにしました。よって、前世代のプログラムの更新は停止いたします。

## ライセンス
幾何学計算の全てを外部の「Shapely」というパッケージで計算するので、自力で組んだ箇所は、その出力を整形してファイル保存するところだけです。
よって、ライセンスは「Shapely」と同等になり、以下の通りです。

「Creative Commons Attribution 3.0 United States License.」

です。

要約すると、以下となります。
* どのようなメディアやフォーマットでも資料を複製したり、再配布できます。 営利目的も含め、どのような目的でも。
* マテリアルをリミックスしたり、改変したり、別の作品のベースにしたりできます。 営利目的も含め、どのような目的でも。

## プログラム環境
開発の環境は以下のとおり。

Python 3.12.2

必要なパッケージ類は、main.py 及び utils.py　を確認の上、インストールしてください。

