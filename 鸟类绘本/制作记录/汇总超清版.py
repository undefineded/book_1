#!/usr/bin/env python3
"""生成37张现有高清页的索引、总览及校对稿；可选合并逐页PDF。"""
import argparse
import json
from pathlib import Path
import subprocess
from 制作超清版 import ROOT, OUT, manuscript


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', type=Path, help='可选整书PDF输出路径，需约600 MiB空闲空间')
    args = parser.parse_args()
    pages = manuscript()
    checks = json.loads((ROOT/'制作记录/超清版技术复核.json').read_text())
    assert len(checks) == 37 and all(p['status'] == '通过' for p in checks), '请先通过37页技术复核。'
    cache = Path('/tmp/bird-hd/book-thumbnails');cache.mkdir(exist_ok=True)
    montage = ['magick', 'montage']
    for n,item in pages.items():
        png = item['folder']/(item['stem']+'-3000px.png')
        thumb = cache/f'P{n}.jpg'
        subprocess.run(['magick',str(png),'-thumbnail','240x240',str(thumb)],check=True)
        montage += ['-label',f'P{n}',str(thumb)]
    montage += ['-font','DejaVu-Sans','-pointsize','16','-geometry','240x240+6+6','-tile','8x5','-background','#fff9ed','-quality','90',str(OUT/'37张图页总览.jpg')]
    subprocess.run(montage,check=True)
    lines = ['# 《羽毛图书馆：会飞的鸟类大百科》超清版','','**现有37张正式图已处理：P1—P36与P40。** P1—P36采用最新扩图版，P40采用现有封底并补足边缘余量。P37—P39尚只有文稿，未将缺图页计入完成数。','','- [37张图页总览](37张图页总览.jpg) · [逐页校对文字](校对文字.md)','- PNG：3000×3000像素，300 PPI。','- 单页PDF：254×254 mm，文字独立排版、字体嵌入；插画为2508×2508像素。','- SVG：可编辑的文字和外链插画，同页目录保留1254px无字底图、2508px AI超分底图。编辑需安装[共享字体](字体/)，PNG与PDF无需安装。','','| 原页码与标题 | 3000px PNG | 矢量文字PDF | 编辑文件 |','| --- | --- | --- | --- |']
    for n,item in pages.items():
        s=item['stem']
        lines.append(f'| {s} | [PNG]({s}/{s}-3000px.png) | [PDF]({s}/{s}-矢量文字版.pdf) | [SVG]({s}/{s}-高清排版.svg) · [说明]({s}/README.md) |')
    lines += ['','## 文案与版本','','本次只处理分辨率，按原图对应的[40页精简排版稿](../文本/40页精简排版稿.md)核对文字，不套用尚未据此重绘的[v2重排稿](../文本/40页精简排版稿-v2.md)。P40保留现有封底已采用的长句：“百科不只在书里，也在你窗外的第一声鸟鸣里。”其与原短稿的差别记入校对文字，原稿保持原样。','','保留P15的三只火烈鸟、蓝灰色湖水及局部粉色倒影，P24笔记本三行符号，P30的坐姿，以及P33站立持本、P36坐姿听录音的已确认修改。原图、扩图版与文稿均未覆盖。','','## 制作与印刷','','先用图像编辑工具分离旧文字，再用waifu2x CUnet两倍模型和ncnn原生CPU FP32推理，将1254px底图提升至2508px；不额外降噪。随后使用霞鹜文楷v1.530重新排字，导出3000px PNG与嵌入字体的PDF。此为AI超分与文字重排。','','实际文字边界距画布四边至少12%；书脊与招牌小字亦以矢量补回。百科标题依纸片深浅选择颜色，字句按各页纸片大小断行。字体采用SIL OFL 1.1许可。','','254mm为本次画布尺寸；PDF插画约251 PPI，文字保持矢量。成品尺寸、装订与出血按印厂规格另定，本次未加入印厂出血或CMYK配置。Git提供全部逐页文件；需要整书PDF时可运行汇总脚本的`--pdf`选项，无损合并这些单页PDF。','','[复核记录](../制作记录/超清版复核记录.md) · [技术检查结果](../制作记录/超清版技术复核.json) · [排版导出脚本](../制作记录/制作超清版.py) · [版式参数](../制作记录/超清版版式.json) · [汇总脚本](../制作记录/汇总超清版.py) · [共用CPU推理源代码](../../CUnet/src/cpu_upscale.cpp)']
    (OUT/'README.md').write_text('\n'.join(lines)+'\n')
    proof = ['# 超清版逐页校对文字','','范围：P1—P36与P40，共37张现有图。正文与百科沿用对应v1稿；P40第一句沿用现有封底的长句，未改写原短稿。标题不打印页码。此文件由排版输入生成，断行以SVG/PDF为准。']
    for n,item in pages.items():
        f=item['fields']
        proof += ['',f'## {item["stem"]}','']
        if f['图内标题']:proof += ['**标题：** '+f['图内标题'],'']
        proof += ['**正文：**','',f['绘本文字'],'','**'+('亲子观察' if n==40 else '寻找提示' if n==1 else '鸟类小百科')+'：**','',f['百科文字']]
    (OUT/'校对文字.md').write_text('\n'.join(line.rstrip() for line in '\n'.join(proof).splitlines())+'\n')
    if args.pdf:
        from pypdf import PdfReader, PdfWriter
        writer = PdfWriter();parent = None
        chapters = {1:'开篇',3:'第一章：飞向世界',17:'第二章：寻找最美鸟鸣',25:'第三章：隐身大师与特技演员',31:'第四章：老街、山谷与奇妙的朋友',40:'封底'}
        for position,(n,item) in enumerate(pages.items()):
            writer.append(PdfReader(item['folder']/(item['stem']+'-矢量文字版.pdf')),import_outline=False)
            if n in chapters:parent=writer.add_outline_item(chapters[n],position)
            writer.add_outline_item(item['stem'],position,parent=parent)
        writer.add_metadata({'/Title':'羽毛图书馆：会飞的鸟类大百科｜现有37张超清版','/Subject':'原页码P1—P36、P40；P37—P39未制图。254mm方形，独立矢量文字与AI超分插画。'})
        writer.page_layout='/SinglePage';writer.page_mode='/UseOutlines'
        args.pdf.parent.mkdir(parents=True,exist_ok=True)
        with args.pdf.open('wb') as stream:writer.write(stream)
        writer.close()
        assert len(PdfReader(args.pdf).pages)==37
    print('37张图页索引、总览与校对文字已生成。')


if __name__=='__main__':main()
