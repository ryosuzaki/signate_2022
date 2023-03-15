# 配布データと応募用ファイル作成方法について

## 学習用データ

学習用データは"train.zip"で, 解凍すると以下のようなディレクトリ構造のデータが作成される.

```bash
train
├─000
│   ├── 0.jpg
│   └── ...
├─001
...
```

- "000", "001"などのディレクトリ名は"型番"を表す.
- 各"型番"の下に対応する部材が写った画像が格納されている.
- 各画像はJPEG形式である.

## メタデータ

メタデータは"train_meta.json"で, 各"型番"に対応するメタ情報を記載したjson形式のデータである. フォーマットは以下の通り.

```bash
{
    "000":
    {
        "category": 戸車|クレセント,
        "color": 色情報
    },
    ...
}
```

- "型番"がkeyとなる.
- 各"型番"に対して"category"と"color"が対応していて, それぞれ部材の種別(戸車かクレセントか)と色情報が記載されている. 色情報の一覧は以下の通り. 同封してあるcolors.pngも参照すること.
  - YK: ブラック
  - K3: ブラック1
  - B7: カームブラック
  - DG: ダークグレイ
  - Q1: 和紙調グレイ
  - A7: グレイ
  - A3: カームグレイ
  - E5: グレイ(プラマードU等)
  - BB: ブラウン(ドアクローザー等)
  - YB: ブロンズ
  - B1: ブラウン
  - CC: 古美グレイ
  - YG: ゴールド
  - P6: 新柾目
  - LG: ひのき
  - E1: クリーム
  - HM: マットステン
  - H5: カームステン
  - H2: ステン１N
  - YH: ステン
  - GS: シャンパンゴールド
  - WB: ホワイトブロンズ
  - CH: ステン(ドアガード等)
  - YS: シルバー
  - YW: ホワイト
  - WM: シルキーホワイト
  - UA: ブリティッシュグリーン
  - UB: グランブルー
  - RB: ラフォレスタブロンズ
- encodingは"utf-8".

## 精度評価を行うためのプログラム

精度評価を行うためのプログラム一式は"evaluation.zip"で, 解凍すると以下のようなディレクトリ構造のデータが作成される.

```bash
evaluation
├── data          
│   ├── ans.json 正解ファイル
│   └── sub.json 予測ファイル
├── readme.md    説明書
└── evaluate.py  精度評価を行うスクリプト
```

詳細は"readme.md"を参照すること.

## 応募用ファイル

学習済みモデルを含めた推論を実行するためのソースコード一式をzipファイルでまとめたものとする.

### ディレクトリ構造

以下のようなディレクトリ構造となっていることを想定している.

```bash
.
├── model              必須: 学習済モデルを置くディレクトリ
│   └── ...
├── src                必須: Pythonのプログラムを置くディレクトリ
│   ├── predictor.py   必須: 最初のプログラムが呼び出すファイル
│   └── ...            その他のファイル (ディレクトリ作成可能)
└── requirements.txt   任意: 追加で必要なライブラリ一覧
```

- 学習済みモデルの格納場所は"model"ディレクトリを想定している.
  - 学習済みモデルを使用しない場合でも空のディレクトリを作成する必要がある.
  - 名前は必ず"model"とすること.
- Pythonのプログラムの格納場所は"src"ディレクトリを想定している.
  - 学習済みモデル等を読み込んで推論するためのメインのソースコードは"predictor.py"を想定している.
    - 名前は必ず"predictor.py"とすること.
  - その他推論を実行するために必要なファイルがあれば作成可能である.
  - 名前は必ず"src"とすること.
- 実行するために追加で必要なライブラリがあれば, その一覧を"requirements.txt"に記載することで, 評価システム上でも実行可能となる.
  - インストール可能で実行可能かどうか予めローカル環境で試しておくこと.
  - 評価システムの実行環境については, [こちら](https://github.com/signatelab/runtime-gpu)を参照すること.

### predictor.pyの実装方法

以下のクラスとメソッドを実装すること.

#### ScoringService

推論実行のためのクラス. 以下のメソッドを実装すること.

##### get_model

モデルや参照用データとそのメタ情報を取得するメソッド. 参照用データとメタ情報は評価システムのサーバーに保存されている. 以下の条件を満たす必要がある.

- クラスメソッドであること.
- 引数model_path(str型), reference_path(str型), reference_meta_path(str型)を指定すること.
  - model_pathは学習済みモデルが格納されているディレクトリのパスである.
  - reference_pathは参照用データで, "型番"に紐づいた画像データが格納されているディレクトリのパスである. 構造は配布している[学習用データ](#学習用データ)と同様.
  - reference_meta_pathは参照用データの"型番"に紐づいたメタ情報を記載したデータのパスである. 形式は配布している[メタデータ](#メタデータ)と同様.
- 学習済みモデルや参照用データとそのメタ情報の読み込みに成功した場合はTrue, 失敗した場合はFalseを返す.
  - モデル自体は任意の名前(例えば"model")で保存しておく.
  - 参照用データとメタ情報は適宜扱いやすい形に変換して任意の名前(例えば"reference", "reference_meta")で保存しておく.

##### predict

推論を実行するメソッド. 以下の条件を満たす必要がある.

- クラスメソッドであること.
- 引数input(str型)を指定すること.
  - 推論する対象となる画像ファイルのパスが渡される.
  - get_modelメソッドで読み込んだ学習済みモデルや参照用データとメタデータを用いて画像に対して推論を行う想定である.
- 以下のフォーマットで推論結果をdict型で返す.
  - keyは**拡張子を含まない**画像ファイル名.
  - 画像データに対応する"型番"を確信度が高い順にlistで記載する.
  - 候補となる"型番"の数は**最大10件**とする.
  - **評価用データには, 学習用データには存在しない"型番"が存在する.** そのような画像に対する推論は参照用データなどを用いて行うこと.

```bash
{
    画像ファイル名:
    [
        "000",
        "001",
        ...
    ]
}
```

以下は実装例.

```Python
import os

class ScoringService(object):
    @classmethod
    def get_model(cls, model_path, reference_path, reference_meta_path):
        """Get model method

        Args:
            model_path (str): Path to the trained model directory.
            reference_path (str): Path to the reference data.
            reference_meta_path (str): Path to the meta data.

        Returns:
            bool: The return value. True for success, False otherwise.
        """
        try:
            cls.model = load_model(os.path.join(model_path, 'my_model'))
            with open(reference_meta_path) as f:
                reference_meta = json.load(f)
            cls.reference = make_reference(reference_path, reference_meta, cls.model)

            return True
        except:
            return False

    @classmethod
    def predict(cls, input):
        """Predict method

        Args:
            input (str): path to the image you want to make inference from

        Returns:
            dict: Inference for the given input.
        """
        # load an image and get the file name
        image = read_image(input)
        sample_name = os.path.basename(input).split('.')[0]

        # do some preprocessing
        preprocessed = preprocess(image)

        # make prediction
        prediction = cls.model.predict(preprocessed)

        # make output
        prediction = postprocess(prediction, cls.reference)
        output = {sample_name: prediction}

        return output


def load_model(model_path):
    """
    load some model(s)
    """
    ...
    return model


def make_reference(reference_path, reference_meta, model):
    """
    make some features for reference data
    """
    ...
    return reference


def read_image(input):
    """
    read some image
    """
    ...
    return image


def preprocess(image):
    """
    preprocess some image
    """
    ...
    return preprocessed


def postprocess(prediction, reference):
    """
    post-process some prediction
    """
    ...
    return prediction
```

応募用サンプルファイル"sample_submit.zip"も参照すること.

### 推論テスト

推論を行うプログラムが実装できたら, 正常に動作するか確認する.

#### 環境構築

評価システムと同じ環境を用意する.

- https://github.com/signatelab/runtime-gpu

#### 推論の実行

モデル学習などを行い, 検証用の画像データを用意し, 推論を実行する.

```bash
$ cd /path/to/src
$ python
...
>>> from predictor import ScoringService # モジュールの読み込み
>>> ScoringService.get_model('../model', '/path/to/reference', '/path/to/reference_meta.json') # 学習済みモデルや参照用データとそのメタ情報の読み込み
True
>>> ScoringService.predict('/path/to/test/image.jpg') # 推論の実行
推論結果
```

### 精度評価

精度評価を行うためのプログラム(evaluation.zip)を利用して, 精度を確認する. 特に上記の[推論の実行](#推論の実行)の推論結果のフォーマットが評価する際の予測結果ファイルのフォーマットと整合するかどうか確認したうえで実行すること. 詳細は"evaluation.zip"の内容を参照.

### 応募用ファイルの作成

上記の[ディレクトリ構造](#ディレクトリ構造)となっていることを確認して, zipファイルとして圧縮する.
