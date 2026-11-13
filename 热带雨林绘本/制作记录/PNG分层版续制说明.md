# PNG分层版续制

全书授权范围为40页。目前P1—P30齐全；P32另有新版无字图。P31—P40保留旧完整PNG，待任务完成后再替换。用户最新要求：无字源图1254×1254经CUnet两倍超分后，直接保存2508×2508推理输出，不再插值到3000px；最终缩放由用户排版时决定。标题与百科透明PNG保留原样。

`PNG分层版待续制任务.json`包含19项未完成的图像生成请求。参考路径相对于仓库根目录，使用时解析成实际本地路径。第一张文字样式参考已经改为仓库内的P16确认稿，不依赖未上传的本地试样。按原请求的`transparent_background`生成，不能为避开额度而改用电脑字体、涂抹场景或冒充已完成。

生成结果按行写入JSONL，每项包含`id`、`page`、`kind`（scene或sheet）、`path`（实际生成PNG）。页面文案与裁切角色见`PNG分层版页面清单.json`。

使用`制作PNG分层版.py`导出：

```bash
python 热带雨林绘本/制作记录/制作PNG分层版.py \
  --pages 热带雨林绘本/制作记录/PNG分层版页面清单.json \
  --results /实际续制工作目录/results.jsonl \
  --output 热带雨林绘本/超清版 \
  --cpu /实际路径/cpu_upscale \
  --model /实际路径/models-cunet \
  --expected 19
```

共用代码与构建说明见[根目录CUnet工具](../../CUnet/README.md)，CPU适配器源码为[src/cpu_upscale.cpp](../../CUnet/src/cpu_upscale.cpp)；使用CUnet的`scale2.0x_model`、noise=-1。新版导出脚本要求1254×1254原生输入，输出`01-原图-2508px.png`（300 PPI），并保存`插画原图-1254px.png`。超分后只转换PNG格式，不再resize；脚本逐像素校验交付PNG与CUnet原始PPM推理输出一致。图像内容编辑仍须使用图像生成工具。

剩余页逐页核对最终PNG字形、手部和完整背景。P37保留填写线、勾选框和空白画图区；P38不印版权占位符；P39纸签为亲子延伸，P40为回想提示。确认齐全后，移除各页旧整页和1254px中间参考，更新文件清单、预览、根索引、完成状态与Git。
