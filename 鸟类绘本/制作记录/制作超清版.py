#!/usr/bin/env python3
"""鸟类绘本现有37页的超分、独立排字与导出；保持原版及v2文稿独立。"""
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
FONTDIR = OUT / '字体'
IDS = list(range(1, 37)) + [40]
NS = 'http://www.w3.org/2000/svg'

def manuscript():
    originals = {}
    for p in (ROOT / '扩图版').rglob('P*.png'):
        originals[int(re.match(r'P(\d+)', p.name)[1])] = p
    originals[40] = ROOT / '绘本图片/P40｜封底：听，窗外的第一声鸟鸣.png'
    source = (ROOT / '文本/40页精简排版稿.md').read_text()
    result = {}
    for m in re.finditer(r'^## P(\d+)｜([^\n]+)\n(.*?)(?=^## P\d+｜|^## 制作|\Z)', source, re.M | re.S):
        n = int(m[1])
        if n not in IDS:
            continue
        fields = {}
        for f in re.finditer(r'^\*\*([^*]+)：\*\*\s*(.*?)(?=^\*\*|\Z)', m[3], re.M | re.S):
            fields[f[1]] = f[2].strip()
        heading = m[2]
        title = fields.get('封面标题', heading)
        if n == 2:
            title = title.removeprefix('扉页：')
        elif n == 40:
            title = ''
        fields['图内标题'] = title
        fields['百科文字'] = fields.get('鸟类小百科', '')
        if n == 1:
            fields['百科文字'] = fields['寻找提示']
        elif n == 40:
            # 分辨率处理沿用现有封底图内长句，记录v1短稿与旧图的差别。
            fields['绘本文字'] = '\n'.join(SPEC['40']['body_lines'])
            fields['百科文字'] = '亲子观察：' + fields['亲子观察']
        original = originals[n]
        result[n] = dict(page=n, heading=heading, fields=fields, original=original, folder=OUT/original.stem, stem=original.stem)
    assert sorted(result) == IDS
    return result

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



def make_svg(item):
    n, f, spec = item['page'], item['fields'], SPEC[str(item['page'])]
    elements = []
    for x,y,w,h,opacity in spec.get('backings', []):
        elements.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="28" fill="#fff4d9" opacity="{opacity:g}" filter="url(#caption-soft)"/>')
    lines = spec.get('title_lines', [f['图内标题']])
    if lines:
        x, baseline, maxwidth, largest = spec['title']
        sizes = spec.get('title_sizes', [largest]*len(lines))
        leading = spec.get('title_leading', largest*1.3)
        anchor = 'middle' if spec.get('center') else 'start'
        for i, line in enumerate(lines):
            size = min(sizes[i], maxwidth/width(line, 1))
            elements.append(text_node([line], x, baseline+i*leading, size, leading, spec.get('title_ink','#895c17'), 500, anchor))
    body = spec.get('body_lines', [s.strip() for s in f['绘本文字'].splitlines() if s.strip()])
    x, baseline, maxwidth, largest, leading = spec['story']
    size = min(largest, min(maxwidth/width(line, 1) for line in body))
    anchor = 'middle' if spec.get('center') or spec.get('story_center') else 'start'
    elements.append(text_node(body, x, baseline, size, leading, spec.get('ink','#54351f'), anchor=anchor))
    if 'header' in spec:
        x, baseline, maxwidth, largest = spec['header']
        header = spec.get('header_text','鸟类小百科')
        size = min(largest, maxwidth/width(header,1))
        elements.append(text_node([header],x,baseline,size,size*1.2,spec.get('header_ink','#80521b'),500,'middle'))
    if f['百科文字']:
        box = spec['fact']
        node = flowing(f['百科文字'],box,spec.get('fact_leading',1.3))
        if spec.get('fact_center'):
            node = node.replace('text-anchor="start"','text-anchor="middle"')
        elements.append(node)
    for label in spec.get('extra_text', []):
        lines = list(label['text']) if label.get('vertical') else [label['text']]
        elements.append(text_node(lines, label['x'], label['baseline'], label['font'], label.get('leading', label['font']*1.25), label.get('color', '#54351f'), 500, 'middle'))
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="{NS}" xmlns:xlink="http://www.w3.org/1999/xlink" width="254mm" height="254mm" viewBox="0 0 1254 1254">
<title>{escape(item['heading'])}｜超清版</title>
<desc>插画由原图去字并经CUnet两倍AI超分，正文与贴纸独立矢量排版。PNG为3000×3000、300PPI，PDF保留嵌入字体；未制作印厂出血。</desc>
<defs><filter id="caption-soft" x="-20%" y="-50%" width="140%" height="200%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="8"/></filter></defs>
<image x="0" y="0" width="1254" height="1254" xlink:href="插画底图-AI超分2508px.png" preserveAspectRatio="xMidYMid meet"/>
<g font-family="LXGW WenKai" text-rendering="geometricPrecision" style="font-variant-ligatures:none;font-feature-settings:'liga' 0,'clig' 0,'calt' 0,'ccmp' 0,'rlig' 0">
{chr(10).join(elements)}
</g></svg>
'''
    path = item['folder']/(item['stem']+'-高清排版.svg')
    path.write_text(svg)
    return path

def export(item):
    folder, stem = item['folder'], item['stem']
    svg = make_svg(item)
    cache = Path('/tmp/bird-hd')
    env = {**os.environ,'FONTCONFIG_FILE':str(FONTDIR/'fontconfig.xml'),'XDG_CACHE_HOME':str(cache/'font-cache'),'INKSCAPE_PROFILE_DIR':str(cache/'inkscape-profile')}
    png,pdf = folder/(stem+'-3000px.png'),folder/(stem+'-矢量文字版.pdf')
    for target,options in [(png,['--export-width=3000','--export-height=3000','--export-dpi=300']),(pdf,[])]:
        subprocess.run(['inkscape',str(svg),'--export-area-page','--export-filename='+str(target),*options],check=True,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    notes = '保持原有构图、角色、鸟种、服饰、动作与道具；以对应v1稿核对主文字，不套用v2重排稿。'
    if item['page']==40:
        notes += '封底保留当前图内两句长文，并补足印刷安全边距；原短稿与原图保留。'
    (folder/'README.md').write_text(f'''# {stem} · 超清版

- [3000px PNG]({png.name})：3000×3000、300 PPI。
- [矢量文字 PDF]({pdf.name})：254×254 mm，字体已嵌入，插画为2508×2508位图。
- [可编辑 SVG]({svg.name})：同目录保留无字底图、超分底图；编辑文字需安装[共享字体](../字体/)，PNG、PDF无需安装。

{notes}

处理方式与印刷说明见[总索引](../README.md)。
''')
    return dict(page=item['page'],png=str(png),pdf=str(pdf))

def complete_png(path):
    if not path.is_file() or path.stat().st_size<12:
        return False
    with path.open('rb') as stream:
        stream.seek(-12,2)
        return stream.read()[4:8]==b'IEND'

def worker(args):
    items = manuscript()
    done = set()
    cache = Path('/tmp/bird-hd');cache.mkdir(exist_ok=True)
    while len(done)<len(items):
        progressed = False
        for n,item in items.items():
            if n in done:
                continue
            base = item['folder']/'插画底图-1254px.png'
            if not complete_png(base):
                continue
            enlarged = item['folder']/'插画底图-AI超分2508px.png'
            if not complete_png(enlarged):
                a,b = cache/f'P{n}-in.ppm',cache/f'P{n}-out.ppm'
                tmp = item['folder']/'插画底图-AI超分2508px.tmp.png'
                started=time.monotonic()
                with (cache/f'P{n}-upscale.log').open('w') as log:
                    subprocess.run(['magick',str(base),'-depth','8',str(a)],check=True,stdout=log,stderr=log)
                    subprocess.run([args.native_cpu,str(a),str(b),args.models],check=True,stdout=log,stderr=log)
                    subprocess.run(['magick',str(b),str(tmp)],check=True,stdout=log,stderr=log)
                tmp.replace(enlarged);a.unlink();b.unlink()
                print(f'P{n} AI超分完成，{time.monotonic()-started:.0f}秒',flush=True)
            result=export(item)
            (cache/f'P{n}-complete.json').write_text(json.dumps(result,ensure_ascii=False))
            done.add(n);progressed=True
            print(f'P{n} PNG/PDF/SVG已导出；{len(done)}/{len(items)}',flush=True)
        if not progressed:
            time.sleep(3)
    print('37张现有图页导出完成。',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker',action='store_true')
    parser.add_argument('--page',type=int)
    parser.add_argument('--native-cpu')
    parser.add_argument('--models')
    args=parser.parse_args()
    if args.page:
        print(json.dumps(export(manuscript()[args.page]),ensure_ascii=False))
    elif args.worker:
        if not args.native_cpu or not args.models:
            parser.error('--worker需要--native-cpu与--models。')
        worker(args)
    else:
        parser.print_help()
