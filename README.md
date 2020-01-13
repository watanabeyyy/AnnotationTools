# Annotation Assist Tools

### Auto Annotation
検出モデルでの推論とPascalVoc形式で結果の保存を行う。
labelimgでそのまま使用可能。
Tensorflow Object Detection APIで作成したモデルを./exported_graphs/frozen_inference_graph.pbに保存されていることを想定。
```
python detection_and_toxml.py ^
    --input_dir=png_dir ^
    --output_dir=xml_dir
```
labelimgのOpen Dirでinput_dirを指定し、Change Save Dirでoutput_dirを指定すれば自動アノテーション結果が確認できる。

### Hash Rename
画像をwhash値にリネームする。
```
python img_rename_hash.py \
    --input_dir=input/img
```

### Augument
画像を白黒反転し対応するラベルも反転し保存する。白黒予測特化。
```
python bitwise_not_augument.py ^
    --img_input_dir=png_dir ^
    --xml_input_dir=xml_dir ^
    --output_dir=out_dir
```
