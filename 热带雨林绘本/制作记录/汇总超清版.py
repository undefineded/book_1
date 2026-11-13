#!/usr/bin/env python3
"""合并已导出的PDF并制作文件索引；保留每页原有位图和矢量文字。"""
from pathlib import Path
import json
import subprocess
from pypdf import PdfReader, PdfWriter
from 制作超清版 import ROOT, OUT, manuscript


pages = manuscript()
checks = json.loads((ROOT / '制作记录/超清版技术复核.json').read_text())
assert len(checks) == 40 and all(p['status'] == '通过' for p in checks), '请先通过40页技术复核。'
book = OUT / '热带雨林大冒险-40页超清版.pdf'
writer = PdfWriter()
chapter_starts = {1: '开篇与封面', 3: '第一章：走进绿色迷宫', 13: '第二章：树梢上的奇妙邻居', 23: '第三章：沿着河流找朋友', 31: '第四章：谁把夜晚点亮了', 37: '收尾与互动'}
parent = None
for n, item in pages.items():
    path = item['folder'] / (item['stem'] + '-矢量文字版.pdf')
    reader = PdfReader(path)
    assert len(reader.pages) == 1
    writer.append(reader, import_outline=False)
    if n in chapter_starts:
        parent = writer.add_outline_item(chapter_starts[n], n-1)
    writer.add_outline_item(item['stem'], n-1, parent=parent)
writer.add_metadata({'/Title': '热带雨林大冒险｜40页超清版', '/Subject': '254毫米方形页面，独立矢量文字与2508像素AI超分插画；保留原始图页。'})
writer.page_layout = '/SinglePage'
writer.page_mode = '/UseOutlines'
temporary = book.with_suffix('.tmp.pdf')
with temporary.open('wb') as stream:
    writer.write(stream)
writer.close()
assert len(PdfReader(temporary).pages) == 40
temporary.replace(book)
print(f'全书PDF：{book.stat().st_size/1024/1024:.1f} MiB', flush=True)

args = ['magick', 'montage']
preview_cache = Path('/tmp/rf-hd-batch/book-thumbnails')
preview_cache.mkdir(parents=True, exist_ok=True)
for n, item in pages.items():
    png = item['folder'] / (item['stem']+'-3000px.png')
    thumbnail = preview_cache / f'P{n}.jpg'
    subprocess.run(['magick', str(png), '-thumbnail', '240x240', str(thumbnail)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    args.extend(['-label', f'P{n}', str(thumbnail)])
args.extend(['-font', 'DejaVu-Sans', '-pointsize', '16', '-geometry', '240x240+6+6', '-tile', '8x5', '-background', '#fff9ed', '-quality', '92', str(OUT/'40页图页总览.jpg')])
subprocess.run(args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

lines = ['# 《热带雨林大冒险》超清版', '', '**P1—P40共40页已完成。** 沿用已确认P26试样的方法；P26文件保持原样，其余39页已完成去字、AI超分与独立文字排版。', '', '- 全书40页超清版PDF：`热带雨林大冒险-40页超清版.pdf`，包含章节与逐页书签，适合连续翻阅和打印。本地合集约'+str(round(book.stat().st_size/1024/1024))+' MiB；Git分发使用下表逐页PDF。', '- [40页图页总览](40页图页总览.jpg)', '- 每页提供3000×3000像素、300 PPI的PNG，以及保留嵌入字体的矢量文字PDF。', '- 每页保留可编辑SVG、1254px无字底图与2508px AI超分底图；共享字体保存在[P26字体目录](P26｜树叶做的午饭/字体/)，许可为SIL OFL 1.1。编辑SVG需安装字体；PNG、PDF无需另行安装。', '', '| 图页 | 3000px PNG | 矢量文字 PDF | SVG与说明 |', '| --- | --- | --- | --- |']
for n, item in pages.items():
    stem = item['stem']
    lines.append(f'| {stem} | [PNG]({stem}/{stem}-3000px.png) | [PDF]({stem}/{stem}-矢量文字版.pdf) | [SVG]({stem}/{stem}-高清排版.svg) · [说明]({stem}/README.md) |')
lines += ['', '## 制作与复核', '', '插画由图像编辑工具分离原有文字，再使用waifu2x CUnet的2倍放大模型，从1254×1254提升至2508×2508；不额外降噪。排字后导出3000px PNG。属于AI超分与重新排字，不是原生3000px重绘。', '', 'P1—P6使用waifu2x-ncnn-vulkan 20250915，P26沿用此前试样；其余页面使用同版CUnet权重与ncnn 20250916原生CPU FP32推理。CPU路径与试样对比的PSNR约55.3 dB，已目视核对轮廓与水彩纹理；无需改变角色或画面构图。', '', '字体使用霞鹜文楷v1.530；百科按纸片大小断行，深色标签使用浅色标题。P15保留修正后的站姿及《树枝间的小跳跃》标题；P37保留正式互动内容，P38不加入待确认版权占位符。', '', '技术检查覆盖40页的PNG尺寸与PPI、PDF页数与页面尺寸、字体嵌入、SVG与MD文案一致性、实际文字四边至少12%的余量及原图文件未变。另已逐页目视检查构图、双手与持物接触、站坐支撑和夜景光线；记录见[超清版复核记录](../制作记录/超清版复核记录.md)。', '', 'PDF每页为254×254 mm，插画约251 PPI，文字保持矢量。此尺寸为本次排版画布；成品尺寸、装订、出血与印刷色彩配置仍按印厂规格确定。原有1254px图页、40页阅读版PDF及MD排版稿保持原样。', '', '制作脚本：[排版与导出](../制作记录/制作超清版.py) · [版式参数](../制作记录/超清版版式.json) · [CPU推理](../../CUnet/src/cpu_upscale.cpp) · [技术检查](../制作记录/检查超清版.py)。']
(OUT/'README.md').write_text('\n'.join(lines)+'\n')
print('40页索引与总览已完成。', flush=True)
