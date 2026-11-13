#!/usr/bin/env python3
"""编排独立文字、调用原生超分与Inkscape导出；不重绘或程序擦除插画。"""
import argparse
from functools import lru_cache
import json
import os
from pathlib import Path
import re
import subprocess
import time
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '超清版'
SPEC = json.loads((ROOT / '制作记录/超清版版式.json').read_text())
FONTDIR = OUT / 'P26｜树叶做的午饭/字体'
NS = 'http://www.w3.org/2000/svg'


def manuscript():
    text = (ROOT / '40页精简排版稿.md').read_text()
    pages = {}
    for m in re.finditer(r'^## P(\d+)｜([^\n]+)\n(.*?)(?=^## P\d+｜|^## 制作前|\Z)', text, re.M | re.S):
        fields = {}
        for f in re.finditer(r'^\*\*([^*]+)：\*\*\s*(.*?)(?=^\*\*|\Z)', m[3], re.M | re.S):
            fields[f[1]] = f[2].strip()
        n = int(m[1])
        original = next((ROOT / '图页').rglob(f'P{n}｜*.png'))
        pages[n] = dict(page=n, fields=fields, original=original, folder=OUT / original.stem, stem=original.stem)
    assert sorted(pages) == list(range(1, 41))
    return pages


def clean(text):
    return re.sub(r'\s+', '', text)


def width(text, size):
    # 文楷汉字接近全角；拉丁与数字按保守宽度估算，最终用PDF实际字框复核。
    return sum(.58 if ord(c) < 128 else 1 for c in text) * size


def wrap(text, size, maxwidth):
    text = clean(text)
    if width(text, size) <= maxwidth:
        return [text]
    closing = '，。！？；：、）》】”’…,.!?;:'
    opening = '（《【“‘'
    words = ['雨林', '植物', '叶子', '板根', '树冠', '种子', '真菌', '养分', '微生物', '环境', '同伴', '动物', '幼虫', '昆虫', '呼吸', '食物', '危险', '生活', '身体', '游泳', '发酵', '发芽', '萤火虫', '前部', '消化']
    avoid = set()
    for word in words:
        for match in re.finditer(word, text):
            avoid.update(range(match.start()+1, match.end()))
    shortest = max(1, int(width(text, size) / maxwidth + .999999))
    for count in range(shortest, min(len(text), shortest+5)+1):
        target = width(text, size) / count
        @lru_cache(None)
        def solve(start, remaining):
            if remaining == 0:
                return (0, ()) if start == len(text) else None
            best = None
            for end in range(start+1, len(text)+1):
                line = text[start:end]
                current_width = width(line, size)
                if current_width > maxwidth:
                    break
                if line[-1] in opening or (end < len(text) and text[end] in closing):
                    continue
                tail = solve(end, remaining-1)
                if tail is None:
                    continue
                cost = (current_width-target)**2 / size**2
                cost += 6 if end in avoid else 0
                cost += 100 if len(line) <= 2 else 0
                cost -= 2 if line[-1] in '，。；！？' else 0
                value = (cost+tail[0], (line,)+tail[1])
                if best is None or value[0] < best[0]:
                    best = value
            return best
        result = solve(0, count)
        if result:
            return list(result[1])
    raise ValueError('无法安排合法断行：'+text)


def text_node(lines, x, baseline, size, leading, color='#54351f', weight=400, anchor='start'):
    spans = ''.join(f'<tspan x="{x:g}" y="{baseline+i*leading:g}">{escape(line)}</tspan>' for i, line in enumerate(lines))
    return f'<text font-size="{size:g}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{spans}</text>'


def flowing(text, box, line_ratio=1.3):
    x, top, maxwidth, height, largest = box
    height = min(height, 1100 - top)
    size = largest
    while size >= 16:
        lines = wrap(text, size, maxwidth)
        leading = size * line_ratio
        if (len(lines)-1)*leading+size <= height:
            return text_node(lines, x, top + size*.86, size, leading)
        size -= .5
    raise ValueError(('文字框过小', text, box))


def interactive():
    elements = []
    def label(text, x, y, size=25):
        elements.append(text_node([text], x, y, size, size*1.3))
    def rule(x1, x2, y):
        elements.append(f'<path d="M{x1} {y} H{x2}" fill="none" stroke="#8a7849" stroke-width="1.6"/>')
    label('观察日期：', 280, 400)
    rule(415, 655, 405)
    label('地点：', 695, 400)
    rule(780, 1035, 405)
    label('我的发现来自：', 280, 452)
    for x in (487, 758):
        elements.append(f'<rect x="{x}" y="431" width="22" height="22" rx="2" fill="none" stroke="#806036" stroke-width="1.6"/>')
    label('亲眼观察', 520, 452)
    label('书本或影像', 792, 452)
    label('我看见了什么：', 280, 504)
    rule(470, 738, 509)
    label('（不知道名字也可以）', 752, 504, 21)
    label('它在哪里、正在做什么：', 280, 556)
    rule(595, 1035, 561)
    label('我听到或读到的声音线索：', 280, 608)
    rule(625, 1035, 613)
    label('我最想画下来的发现：', 280, 655)
    label('我还想知道：', 280, 991)
    rule(455, 1035, 996)
    label('亲子提示：', 300, 1064, 23)
    elements.append(text_node(wrap('请大人帮忙记录问题；在户外观察时保持距离，不捉、不喂、不采走。', 22, 610), 435, 1062, 22, 28))
    return elements


def make_svg(item):
    n, f, folder = item['page'], item['fields'], item['folder']
    spec = SPEC[str(n)]
    title = f['图内标题'].replace('（分两行）', '').split('／')
    title = spec.get('title_lines', title)
    x, baseline, maxwidth, largest = spec['title']
    size = min(largest, min(maxwidth / width(line, 1) for line in title))
    leading = spec.get('title_leading', size*1.23)
    anchor = 'middle' if spec.get('center') else 'start'
    elements = [text_node(title, x, baseline, size, leading, spec.get('title_ink', '#895c17'), 500, anchor)]
    body = f.get('绘本文字', f.get('封面导语', ''))
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    x, baseline, maxwidth, largest, leading = spec['story']
    size = min(largest, min(maxwidth / width(line, 1) for line in lines))
    elements.append(text_node(lines, x, baseline, size, leading, spec.get('ink', '#54351f'), anchor=anchor))
    if 'header' in spec:
        header = '雨林小百科'
        fact = f.get('雨林小百科', '')
        if n == 39:
            header, fact = '亲子延伸', f['亲子延伸']
        elif n == 40:
            header = '还记得吗？'
            fact = f['寻找提示贴纸'].removeprefix(header)
        x, baseline, maxwidth, largest = spec['header']
        size = min(largest, maxwidth / width(header, 1))
        color = '#fff4cc' if n in (7, 14, 16, 20, 27) else '#80521b'
        elements.append(text_node([header], x, baseline, size, size*1.2, color, 500, 'middle'))
        elements.append(flowing(fact, spec['fact'], spec.get('fact_leading', 1.3)))
    if n == 37:
        elements.extend(interactive())
    content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="{NS}" xmlns:xlink="http://www.w3.org/1999/xlink" width="254mm" height="254mm" viewBox="0 0 1254 1254">
<title>{escape(f['图内标题'].replace('（分两行）', ''))}｜超清排版</title>
<desc>插画经2倍AI超分至2508像素，文字独立矢量排版。PNG导出3000×3000像素、300PPI。PDF保留嵌入字体，不含出血标记。</desc>
<image x="0" y="0" width="1254" height="1254" xlink:href="插画底图-AI超分2508px.png" preserveAspectRatio="xMidYMid meet"/>
<g font-family="LXGW WenKai" text-rendering="geometricPrecision" style="font-variant-ligatures:none;font-feature-settings:'liga' 0,'clig' 0,'calt' 0,'ccmp' 0,'rlig' 0">
{chr(10).join(elements)}
</g>
</svg>
'''
    path = folder / (item['stem'] + '-高清排版.svg')
    path.write_text(content)
    return path


def export(item):
    folder, stem = item['folder'], item['stem']
    svg = make_svg(item)
    cache = Path(os.environ.get('RF_HD_CACHE', '/tmp/rf-hd-batch'))
    cache.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, 'FONTCONFIG_FILE': str(FONTDIR / 'fontconfig.xml'), 'XDG_CACHE_HOME': str(cache / 'font-cache'), 'INKSCAPE_PROFILE_DIR': str(cache / 'inkscape-profile')}
    png, pdf = folder / (stem + '-3000px.png'), folder / (stem + '-矢量文字版.pdf')
    for output, options in [(png, ['--export-width=3000', '--export-height=3000', '--export-dpi=300']), (pdf, [])]:
        subprocess.run(['inkscape', str(svg), '--export-area-page', '--export-filename='+str(output), *options], check=True, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    (folder / 'README.md').write_text(f'''# {stem} · 超清版

- [3000px PNG]({png.name})：3000×3000像素，300 PPI。
- [矢量文字 PDF]({pdf.name})：254×254 mm，文字为矢量并已嵌入字体，插画为2508×2508像素位图。
- [可编辑 SVG]({svg.name})：同目录保存无字插画底图；字体使用[共享的霞鹜文楷](../P26｜树叶做的午饭/字体/)。PNG和PDF无需安装字体。

沿用已确认P26试样的处理方法：图像编辑工具分离旧文字，2倍AI超分，按MD文案重新排字。保留本页角色、动作、服饰、动物与光线。

完整方法、原图保留与印刷规格说明见[超清版总索引](../README.md)。
''')
    return dict(page=item['page'], png=str(png), pdf=str(pdf))


def worker(args):
    pages = manuscript()
    cache = Path(args.cache)
    cache.mkdir(parents=True, exist_ok=True)
    binary = Path(args.upscaler) if args.upscaler else None
    models = Path(args.models) if args.models else binary.parent / 'models-cunet'
    env = {**os.environ, 'LP_NUM_THREADS': '2', 'XDG_CACHE_HOME': str(cache)}
    if args.icd:
        env.update(VK_DRIVER_FILES=args.icd, VK_ICD_FILENAMES=args.icd)
    done = {26}
    order = list(range(2, 26)) + list(range(27, 41)) + [1]
    while len(done) < 40:
        progressed = False
        for n in order:
            if n in done:
                continue
            item = pages[n]
            original = item['folder'] / '插画底图-1254px.png'
            upscaled = item['folder'] / '插画底图-AI超分2508px.png'
            if not original.is_file():
                continue
            if not upscaled.is_file():
                tmp = item['folder'] / '插画底图-AI超分2508px.tmp.png'
                started = time.monotonic()
                with (cache / f'P{n}-upscale.log').open('w') as log:
                    if args.native_cpu:
                        input_ppm = cache / f'P{n}-input.ppm'
                        output_ppm = cache / f'P{n}-output.ppm'
                        subprocess.run(['magick', str(original), '-depth', '8', str(input_ppm)], check=True, stdout=log, stderr=log)
                        subprocess.run([args.native_cpu, str(input_ppm), str(output_ppm), str(models)], check=True, env=env, stdout=log, stderr=log)
                        subprocess.run(['magick', str(output_ppm), str(tmp)], check=True, stdout=log, stderr=log)
                        input_ppm.unlink()
                        output_ppm.unlink()
                    else:
                        jobs = '1:2:1' if args.device == '-1' else '1:1:1'
                        subprocess.run([str(binary), '-i', str(original), '-o', str(tmp), '-m', str(models), '-g', args.device, '-j', jobs, '-t', '256', '-n', '-1', '-s', '2', '-f', 'png'], check=True, env=env, stdout=log, stderr=log)
                tmp.replace(upscaled)
                print(f'P{n} AI超分完成，{time.monotonic()-started:.0f}秒', flush=True)
            result = export(item)
            (cache / f'P{n}-complete.json').write_text(json.dumps(result, ensure_ascii=False))
            done.add(n)
            progressed = True
            print(f'P{n} PNG/PDF/SVG已导出；共{len(done)}/40页', flush=True)
        if not progressed:
            time.sleep(5)
    print('40页导出完成。', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--page', type=int, help='重新排版导出单页；保留该页已有AI底图')
    parser.add_argument('--worker', action='store_true')
    parser.add_argument('--cache', default='/tmp/rf-hd-batch')
    parser.add_argument('--upscaler')
    parser.add_argument('--icd')
    parser.add_argument('--device', default='0', help='0为Vulkan设备，-1为原生CPU')
    parser.add_argument('--models', help='指定CUnet模型目录；默认使用二进制旁models-cunet')
    parser.add_argument('--native-cpu', help='已编译的CUnet/build/cpu_upscale路径；使用同一CUnet模型以FP32推理')
    args = parser.parse_args()
    if args.page:
        if args.page == 26:
            raise SystemExit('P26为已确认试样，批处理不覆盖。')
        print(json.dumps(export(manuscript()[args.page]), ensure_ascii=False))
    elif args.worker:
        if not args.native_cpu and not args.upscaler:
            parser.error('--worker需要--native-cpu或--upscaler。')
        if not args.models and not args.upscaler:
            parser.error('需要--models指定模型目录，或--upscaler使用其配套模型。')
        worker(args)
    else:
        parser.print_help()
