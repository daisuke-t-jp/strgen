[English](https://github.com/daisuke-t-jp/strgen/blob/master/README.md)

# strgen

## 概要

<img src="https://raw.githubusercontent.com/daisuke-t-jp/strgen/master/images/strgen.png" width="700px">

**strgen** は Android / iOS の多言語ファイルを CSV ファイルから作成できます。


## インストール

https://pypi.org/project/strgen/

`pip` を使ってインストールできます。

```sh
$ pip install strgen
```


## 使い方

### 1. 入力用のファイルを準備します。

入力用ファイルの準備。

#### CSV ファイル

多言語ファイルのソースファイルです。

- [フォーマット](#CSVフォーマット)
- [サンプル](https://github.com/daisuke-t-jp/strgen/blob/master/sample/source.csv)


#### YAML ファイル

設定ファイルです。

- [フォーマット](#YAMLフォーマット)
- [サンプル](https://github.com/daisuke-t-jp/strgen/blob/master/sample/strgen.yml)



### 2. `strgen` を実行

```sh
$ strgen strgen.yml 
```

YAML ファイルを引数にして、実行します。  
もし、指定がない場合、カレントディレクトリにある `strgen.yml` を使用することになります。

以下のファイルが `build` フォルダ以下に生成されます。

- build/
    - apple/
        - LocalizableStrings.swift
        - lproj/
            - en.lproj/Localizable.strings
            - ja-JP.lproj/Localizable.strings
            - ...
    - google/
        - values-en/strings.xml
        - values-ja-JP/strings.xml
        - ...

`apple` フォルダ(iOS/macOS 用)の中には、 キーが列挙された `LocalizableStrings.swift` も生成されます。

```swift
import Foundation

class LocalizableStrings {

    enum Key: String {
        case yes = "yes"
        case no = "no"
        case cancel = "cancel"
        case next = "next"
        case close = "close"
        case escape_test = "escape_test"
        case parameter_google = "parameter_google"
        case parameter_apple = "parameter_apple"
    }

}
```


## サンプル

簡単に試せるサンプルがあります。

[サンプル](https://github.com/daisuke-t-jp/strgen/tree/master/sample)

1. プロジェクトを clone します。
    ```sh
    $ git clone https://github.com/daisuke-t-jp/strgen
    ```
1. カレントディレクトリを `strgen/sample` フォルダに変更します。
1. 以下のコマンドを実行。
    ```sh
    $ strgen strgen.yml 
    ```
1. `build` フォルダを確認します。



## 入力ファイルフォーマット

### CSVフォーマット

| id | en | ja-JP | zh-Hans | zh-Hant | ... |
| ---- | ---- | ---- | ---- | ---- | ---- |
| hello_world | Hello world | こんにちは世界 | 你好，世界 | 你好，世界 | ... |
| yes | Yes | はい | 是 | 是 | ... |
| no | No | いいえ | 没有 | 沒有 | ... |
| cancel | Cancel | キャンセル | 取消 | 取消 | ... |
| next | Next | キャンセル | 下一个 | 下一個 | ... |
| close | Next | キャンセル | 下一个 | 下一個 | ... |
| escape_test | escape <'""&?@> test | | | | | ... |
| parameter_google | Parameter %1$s, %2$s. | | | | | ... |
| parameter_apple | Parameter %1$@, %2$@. | | | | | ... |


#### ヘッダ

ヘッダ行は `id` で開始します。  
次に、言語（言語と国コード）を追加します。


#### ボディ

`id` の文字列が iOS / Android 参照用のキーになります。  
各言語のローカライズされた文字列を入力します。

ローカライズ文字列を未入力にすることもできます。  
その場合は、その言語に対してのローカライズ文字列は生成されません。


### YAMLフォーマット

`strgen.yml`

```yml
general:
  input_file_path: ./source.csv
  output_path: ./
google:
  strings_file_name: strings.xml
apple:
  strings_file_name: Localizable.strings
  swift_file_name: LocalizableStrings.swift
  swift_class_name: LocalizableStrings
```

#### `general`

##### `input_file_path` (必須)

入力用 CSV ファイルのパス。

##### `output_path` (任意)

出力先パス。  
デフォルトは、カレントディレクトリになります。


#### `google`

##### `strings_file_name` (任意)

生成された多言語ファイルの名前。  
デフォルトは `strings.xml` です。


#### `apple`

##### `strings_file_name` (任意)

生成された多言語ファイルの名前。  
デフォルトは `Localizable.strings` です。

##### `swift_file_name` (任意)

生成された Swift ファイルの名前。  
デフォルトは `LocalizableStrings.swift` です。

##### `swift_class_name` (任意)

生成された Swift クラス名。  
デフォルトは `LocalizableStrings` です。

