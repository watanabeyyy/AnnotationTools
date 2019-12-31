# Annotation Assist Tools

### Auto Annotation
検出モデルでの推論とPascalVoc形式で結果の保存を行う。
labelimgでそのまま使用可能。
Tensorflow Object Detection APIで作成したモデルの使用を想定。
```
python detection_and_toxml.py \
    --input_dir=input/img \
    --output_dir=output/xml
```

### Hash Rename
画像をwhash値にリネームする。
```
python img_rename_hash.py \
    --input_dir=input/img
```

### Augument
画像を白黒反転し対応するラベルも反転し保存する。白黒予測特化。
```
python bitwise_not_augument.py \
    --img_input_dir=input/img \
    --xml_input_dir=input/xml \
    --output_dir=output
```