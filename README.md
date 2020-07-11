[日本語](https://github.com/daisuke-t-jp/strgen/blob/master/README.ja.md)

# strgen

## Overview

<img src="https://raw.githubusercontent.com/daisuke-t-jp/strgen/master/images/strgen.png" width="700px">

The **strgen** can create iOS / Android strings file from CSV file.


## Install
 
https://pypi.org/project/strgen/

The strgen can install using `pip`.

```sh
$ pip install strgen
```


## Usage

### 1. Prepare input files

Prepare input files.

#### CSV file

The source file of multi language strings.

- [Format](#CSV-format)
- [Sample](https://github.com/daisuke-t-jp/strgen/blob/master/sample/source.csv)


#### YAML file

The config file.

- [Format](#YAML-format)
- [Sample](https://github.com/daisuke-t-jp/strgen/blob/master/sample/strgen.yml)



### 2. Run `strgen`

```sh
$ strgen strgen.yml 
```

Run with argument of YAML file path.  
If not specified, `strgen.yml` in the current directory will be used.

The following files will be generated under the `build` folder.

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

in `apple` folder(for iOS/macOS),  
`LocalizableStrings.swift` that enumerated the key names is also generated.

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


## Sample

There are sample that you can easily try.

[Sample](https://github.com/daisuke-t-jp/strgen/tree/master/sample)

1. Clone project.
    ```sh
    $ git clone https://github.com/daisuke-t-jp/strgen 
    ```
1. Change the current directory to `strgen/sample`.
1. Run
    ```sh
    $ strgen strgen.yml 
    ```
1. Check `build` folder.



## Input file format

### CSV format

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


#### Header

Start the header line with `id`.  
Next, add the language (language and country code).


#### Body

The `id` string will be the key to reference on iOS / Android.  
Enter the localized string for each language.

You can leave the localized string blank.  
In that case, no localized strings are generated for that language.


### YAML format

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

##### `input_file_path` (Required)

Input CSV file path.

##### `output_path` (Optional)

Output path.  
Default directory is current directory


#### `google`

##### `strings_file_name` (Optional)

Generated strings file's name.  
Default is `strings.xml`.


#### `apple`

##### `strings_file_name` (Optional)

Generated strings file's name.  
Default is `Localizable.strings`.

##### `swift_file_name` (Optional)

Generated swift file's name.  
Default is `LocalizableStrings.swift`.

##### `swift_class_name` (Optional)

Generated swift class name.  
Default is `LocalizableStrings`.

