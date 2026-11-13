# CUnet CPU两倍超分工具

集中维护本仓库雨林、鸟类绘本共用的CUnet推理代码。使用waifu2x的现成模型，通过ncnn在CPU上以FP32推理；固定两倍放大、noise=-1，不额外降噪。

**当前规则：本工具仅保留供用户在自己电脑上手动使用。后续云端Agent不再执行任何超分，绘本导出只保存原尺寸场景。下列安装、编译与运行命令均为用户本地参考。**

**1254×1254输入直接输出2508×2508。超分之后只转换PNG格式、设置PPI，不再插值或resize；最终排版缩放由使用者决定。** 同样支持其他尺寸的RGB图，输出宽高均为输入的两倍。

## 目录

| 文件 | 用途 |
|---|---|
| [src/cpu_upscale.cpp](src/cpu_upscale.cpp) | 原共用CPU适配器：RGB PPM输入/输出，256px瓦片、18px边界、两线程 |
| [build.sh](build.sh) | 使用外部ncnn SDK编译，产物默认放入build/ |
| [upscale.py](upscale.py) | RGB图片转PPM、运行推理、转PNG，并校验原推理像素没有改变 |
| [models.json](models.json) | 模型与ncnn固定版本、下载地址、两个模型文件的SHA-256 |
| [requirements.txt](requirements.txt) | Python入口依赖，仅Pillow |
| [THIRD_PARTY.md](THIRD_PARTY.md) | 上游来源与许可文本 |

模型、ncnn SDK及本机编译产物由使用环境准备，Git中只保存代码、清单与说明。`models-cunet/`、`build/`已忽略。

## 1. 依赖与编译

Linux环境需要Python 3、GCC/G++（C++17与OpenMP）、ImageMagick 7（`magick`）、curl和unzip。

在仓库根目录执行：

```bash
python -m pip install -r CUnet/requirements.txt
curl -L --fail -o /tmp/cunet-ncnn.zip \
  https://github.com/Tencent/ncnn/releases/download/20250916/ncnn-20250916-ubuntu-2204-shared.zip
unzip /tmp/cunet-ncnn.zip -d /tmp/cunet-deps
bash CUnet/build.sh /tmp/cunet-deps/ncnn-20250916-ubuntu-2204-shared
```

也可直接使用已有SDK：`bash CUnet/build.sh /实际SDK路径`。该目录应包含`include/ncnn/net.h`和`lib/libncnn.so`。构建时写入该SDK的运行时库路径；移动SDK后需重新编译。可用`CXX`选择编译器，用第二个位置参数指定构建目录。

## 2. 模型

本项目使用waifu2x-ncnn-vulkan **20250915**发布包中的`models-cunet/scale2.0x_model`：

```bash
curl -L --fail -o /tmp/cunet-waifu2x.zip \
  https://github.com/nihui/waifu2x-ncnn-vulkan/releases/download/20250915/waifu2x-ncnn-vulkan-20250915-linux.zip
mkdir -p CUnet/models-cunet
unzip -j /tmp/cunet-waifu2x.zip \
  '*/models-cunet/scale2.0x_model.bin' \
  '*/models-cunet/scale2.0x_model.param' -d CUnet/models-cunet
sha256sum CUnet/models-cunet/scale2.0x_model.*
```

将输出与[models.json](models.json)的两个校验值对照。也可把已有的同版模型文件复制到此目录，或运行时用`--models`指定位置。

## 3. 使用

```bash
python CUnet/upscale.py 输入.png CUnet/output/输出-2508px.png
```

默认调用`CUnet/build/cpu_upscale`与`CUnet/models-cunet/`，输出PNG标记300 PPI，并打印输入尺寸、输出尺寸和原推理像素SHA-256。

显式指定依赖或覆盖已有输出：

```bash
python CUnet/upscale.py 输入.png 输出.png \
  --cpu /实际路径/cpu_upscale \
  --models /实际路径/models-cunet \
  --dpi 300 --overwrite
```

输入为RGB图片；透明标题、正文和百科素材应独立保留，不传入本工具。工具不生成场景、不修字，也不裁切或移动人物。AI新增细节由模型推测，不称为原生高分辨率重绘。

PNG写入临时文件，通过尺寸与像素校验后再替换目标。已有输出需加`--overwrite`。用户本地也可以调用`CUnet.upscale.upscale_image`。`CUnet/output/`已加入Git忽略；雨林[分层导出脚本](../热带雨林绘本/制作记录/制作PNG分层版.py)已停止调用本模块，只原样归档场景及裁切透明文字素材。

底层PPM接口仍为：

```bash
CUnet/build/cpu_upscale input.ppm output.ppm CUnet/models-cunet
```

历史3000px排版脚本可继续把此二进制作为`--native-cpu`参数；新版雨林场景采用本目录的直接两倍输出规范。

## 整理后的验证

2026-11-13：使用ncnn 20250916编译通过；独立CLI重跑P16、绘本导出入口重跑P15，1254px输入得到的2508px结果均与仓库已有成品逐像素完全一致，300 PPI保留。另检查了默认不覆盖已有文件、拒绝透明文字素材，以及文档链接。
