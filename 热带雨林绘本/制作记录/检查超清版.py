#!/usr/bin/env python3
"""检查导出文件、文稿一致性、字体和实际文字边距；不代替目视验收。"""
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import xml.etree.ElementTree as ET
from 制作超清版 import manuscript, ROOT


def command(*args):
    return subprocess.check_output(args, text=True)


def normalize(text):
    return re.sub(r'\s+', '', text)


def png_info(path):
    info = {}
    with path.open('rb') as stream:
        assert stream.read(8) == b'\x89PNG\r\n\x1a\n'
        while True:
            length_bytes = stream.read(4)
            if len(length_bytes) < 4:
                break
            length = struct.unpack('>I', length_bytes)[0]
            kind = stream.read(4)
            if kind == b'IHDR':
                data = stream.read(length)
                info['width'], info['height'] = struct.unpack('>II', data[:8])
            elif kind == b'pHYs':
                x, y, unit = struct.unpack('>IIB', stream.read(length))
                if unit == 1:
                    info['ppi_x'], info['ppi_y'] = round(x*.0254, 3), round(y*.0254, 3)
            else:
                stream.seek(length, 1)
            stream.read(4)
            if kind in (b'IDAT', b'IEND'):
                break
    return info


reports = []
for n, item in manuscript().items():
    stem, folder = item['stem'], item['folder']
    png = folder / (stem + '-3000px.png')
    pdf = folder / (stem + '-矢量文字版.pdf')
    svg = folder / (stem + '-高清排版.svg')
    if not all(p.is_file() for p in (png, pdf, svg)):
        reports.append(dict(page=n, status='待导出'))
        continue
    report = dict(page=n, status='通过', issues=[])
    try:
        info = png_info(png)
        assert (info['width'], info['height']) == (3000, 3000), info
        assert abs(info['ppi_x']-300) < .01 and abs(info['ppi_y']-300) < .01, info
        report['png'] = info
        svgdoc = ET.parse(svg)
        svgtext = ''.join(''.join(t.itertext()) for t in svgdoc.findall('.//{http://www.w3.org/2000/svg}text'))
        pdftext = command('pdftotext', '-raw', str(pdf), '-')
        assert normalize(svgtext) == normalize(pdftext), 'PDF与SVG文字不同'
        f = item['fields']
        title = f['图内标题'].replace('（分两行）', '').replace('／', '')
        required = [title, f.get('绘本文字', f.get('封面导语', ''))]
        required.extend(f[key] for key in ('雨林小百科', '亲子延伸', '寻找提示贴纸') if key in f)
        if n == 37:
            required.append(f['亲子提示'])
            required.extend(['观察日期：', '地点：', '我的发现来自：', '亲眼观察', '书本或影像', '我看见了什么：', '它在哪里、正在做什么：', '我听到或读到的声音线索：', '我最想画下来的发现：', '我还想知道：'])
        for text in required:
            assert normalize(text) in normalize(pdftext), 'MD文字缺失：'+text
        fonts = command('pdffonts', str(pdf))
        assert 'LXGWWenKai' in fonts and not re.search(r'\bno\b', fonts), '字体未全部嵌入或缺少Unicode映射'
        report['embedded_fonts'] = True
        pdfmeta = command('pdfinfo', str(pdf))
        assert re.search(r'Pages:\s+1\b', pdfmeta) and re.search(r'Page size:\s+720 x 720 pts', pdfmeta), 'PDF页数或尺寸异常'
        bitmap = command('pdfimages', '-list', str(pdf)).splitlines()[2:]
        assert any(line.split()[3:5] == ['2508', '2508'] for line in bitmap if len(line.split()) > 5), 'PDF插画分辨率异常'
        bbox = ET.fromstring(command('pdftotext', '-bbox', str(pdf), '-'))
        words = list(bbox.iter('{http://www.w3.org/1999/xhtml}word'))
        x1 = min(float(w.get('xMin')) for w in words)
        y1 = min(float(w.get('yMin')) for w in words)
        x2 = max(float(w.get('xMax')) for w in words)
        y2 = max(float(w.get('yMax')) for w in words)
        margins = [x1/720, (720-x2)/720, y1/720, (720-y2)/720]
        report['text_margin_percent_left_right_top_bottom'] = [round(x*100, 2) for x in margins]
        assert min(margins) >= .12, '文字安全边距不足12%'
        for element in svgdoc.iter():
            href = element.get('{http://www.w3.org/1999/xlink}href')
            if href:
                assert (svg.parent/href).is_file(), 'SVG缺少底图'
        original = item['original']
        relative = original.relative_to(ROOT.parent).as_posix()
        committed = subprocess.check_output(['git', 'show', 'HEAD:'+relative], cwd=ROOT.parent)
        assert hashlib.sha256(committed).digest() == hashlib.sha256(original.read_bytes()).digest(), '原图发生改变'
        report['original_unchanged'] = True
    except (AssertionError, KeyError, subprocess.CalledProcessError) as error:
        report['status'] = '需修订'
        report['issues'].append(str(error))
    reports.append(report)

path = ROOT / '制作记录/超清版技术复核.json'
path.write_text(json.dumps(reports, ensure_ascii=False, indent=2)+'\n')
for report in reports:
    if report['status'] != '待导出':
        print('P'+str(report['page']), report['status'], report.get('issues', []), report.get('text_margin_percent_left_right_top_bottom', []))
print('已导出', sum(r['status'] != '待导出' for r in reports), '/ 40；通过', sum(r['status'] == '通过' for r in reports))
