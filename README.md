# 連續血糖數據分析與圖形化應用 (Continuous Glucose Data Analysis and Visualization CGDAV)

## Aplication

本應用可實現抓取Glimp儲存在Dropbox之血糖數據，並且將其繪製成圖表。
> [!NOTE]
> 需先建立一Dropbox應用程式，並且取得其金鑰。


### Usage
下載所有程式檔，並且將其存放到同一資料夾。
使用終端機輸入下方指令(請注意路徑是否為先前檔案存放位置)
```console
 $ python main.py
```
依指示輸Dropbox金鑰(一段時間後須重新生成)
程式就會生成三張圖表與一數據文字檔。
若需更改路徑，請使用`cd`(change dictionary)

```console
  $ cd "your full dictionary path"
```
