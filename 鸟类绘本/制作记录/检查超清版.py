#!/usr/bin/env python3
"""检查鸟类现有37张图页的输出、文字、字体、实际边距和原图保留。"""
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import xml.etree.ElementTree as ET
from 制作超清版 import ROOT, SPEC, IDS, manuscript

def command(*args):
    return subprocess.check_output(args,text=True)

def normalize(text):
    return re.sub(r'\s+','',text)

def png_info(path):
    info={}
    with path.open('rb') as stream:
        assert stream.read(8)==b'\x89PNG\r\n\x1a\n'
        while True:
            b=stream.read(4)
            if len(b)<4:break
            length=struct.unpack('>I',b)[0];kind=stream.read(4)
            if kind==b'IHDR':
                data=stream.read(length);info['width'],info['height']=struct.unpack('>II',data[:8])
            elif kind==b'pHYs':
                x,y,unit=struct.unpack('>IIB',stream.read(length))
                if unit==1:info['ppi_x'],info['ppi_y']=round(x*.0254,3),round(y*.0254,3)
            else:stream.seek(length,1)
            stream.read(4)
            if kind in (b'IDAT',b'IEND'):break
    return info

reports=[]
for n,item in manuscript().items():
    folder,stem=item['folder'],item['stem']
    png,pdf,svg=folder/(stem+'-3000px.png'),folder/(stem+'-矢量文字版.pdf'),folder/(stem+'-高清排版.svg')
    if not all(p.is_file() for p in (png,pdf,svg)):
        reports.append(dict(page=n,status='待导出'));continue
    report=dict(page=n,status='通过',issues=[])
    try:
        info=png_info(png)
        assert (info['width'],info['height'])==(3000,3000),info
        assert abs(info['ppi_x']-300)<.01 and abs(info['ppi_y']-300)<.01,info
        report['png']=info
        tree=ET.parse(svg)
        text=''.join(''.join(t.itertext()) for t in tree.findall('.//{http://www.w3.org/2000/svg}text'))
        actual=command('pdftotext','-raw',str(pdf),'-')
        assert normalize(text)==normalize(actual),'PDF与SVG文字不同'
        f=item['fields']
        for required in (f['绘本文字'],f['百科文字']):
            assert normalize(required) in normalize(actual),'正文或贴纸文字与校对稿不同'
        title=f['图内标题']
        if n in [3,17,25,31]:
            drop=lambda s:re.sub(r'[：:/／]','',normalize(s))
            assert drop(title) in drop(actual),'章名缺失'
        elif title:
            assert normalize(title) in normalize(actual),'图内标题缺失'
        fonts=command('pdffonts',str(pdf))
        assert 'LXGWWenKai' in fonts and not re.search(r'\bno\b',fonts),'字体未全部嵌入或映射异常'
        report['embedded_fonts']=True
        meta=command('pdfinfo',str(pdf))
        assert re.search(r'Pages:\s+1\b',meta) and re.search(r'Page size:\s+720 x 720 pts',meta),'PDF页数或尺寸异常'
        images=command('pdfimages','-list',str(pdf)).splitlines()[2:]
        assert any(row.split()[3:5]==['2508','2508'] for row in images if len(row.split())>5),'PDF插画像素异常'
        box=ET.fromstring(command('pdftotext','-bbox',str(pdf),'-'))
        words=list(box.iter('{http://www.w3.org/1999/xhtml}word'))
        x1=min(float(w.get('xMin')) for w in words);y1=min(float(w.get('yMin')) for w in words)
        x2=max(float(w.get('xMax')) for w in words);y2=max(float(w.get('yMax')) for w in words)
        margins=[x1/720,(720-x2)/720,y1/720,(720-y2)/720]
        report['text_margin_percent_left_right_top_bottom']=[round(v*100,2) for v in margins]
        assert min(margins)>=.12,'文字安全余量不足12%'
        for e in tree.iter():
            ref=e.get('{http://www.w3.org/1999/xlink}href')
            if ref:assert (folder/ref).is_file(),'SVG缺少底图'
        relative=item['original'].relative_to(ROOT.parent).as_posix()
        original=subprocess.check_output(['git','show','HEAD:'+relative],cwd=ROOT.parent)
        assert hashlib.sha256(original).digest()==hashlib.sha256(item['original'].read_bytes()).digest(),'原图被修改'
        report['original_unchanged']=True
    except (AssertionError,KeyError,subprocess.CalledProcessError) as error:
        report['status']='需修订';report['issues'].append(str(error))
    reports.append(report)
(ROOT/'制作记录/超清版技术复核.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n')
for row in reports:
    if row['status']!='待导出':print('P'+str(row['page']),row['status'],row.get('issues',[]),row.get('text_margin_percent_left_right_top_bottom',[]))
print('导出',sum(r['status']!='待导出' for r in reports),'/37；通过',sum(r['status']=='通过' for r in reports))
sys.exit(0 if len(reports)==37 and all(r['status']=='通过' for r in reports) else 1)
