"""将当前选用的40张PNG按页码嵌入阅读PDF，不修改原图。"""

import re
from io import BytesIO
from pathlib import Path

from PIL import Image
from pypdf import PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


def main():
    root = Path(__file__).resolve().parents[1]
    numbered = []
    for path in (root / "图页").rglob("*.png"):
        match = re.match(r"P(\d+)｜", path.name)
        if match:
            numbered.append((int(match.group(1)), path))
    numbered.sort()
    assert [number for number, _ in numbered] == list(range(1, 41)), "需要P1—P40各一张"
    for _, path in numbered:
        with Image.open(path) as image:
            assert image.size == (1254, 1254), (path.name, image.size)

    output = root / "阅读版" / "热带雨林大冒险-40页阅读版.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    page_side = 600
    pdf = canvas.Canvas(str(output), pagesize=(page_side, page_side), pageCompression=1)
    pdf.setTitle("热带雨林大冒险｜40页阅读版")
    pdf.setSubject("按P1—P40顺序嵌入当前选用图页，供阅读审阅")
    for number, path in numbered:
        # 阅读PDF采用高质量JPEG压缩，保留原像素尺寸；PNG原文件不修改。
        jpeg = BytesIO()
        with Image.open(path) as image:
            image.convert("RGB").save(jpeg, format="JPEG", quality=95, subsampling=0, optimize=True)
        jpeg.seek(0)
        pdf.drawImage(ImageReader(jpeg), 0, 0, width=page_side, height=page_side)
        key = f"P{number}"
        pdf.bookmarkPage(key)
        pdf.addOutlineEntry(path.stem, key, level=0)
        pdf.showPage()
    pdf.save()
    reader = PdfReader(str(output))
    assert len(reader.pages) == 40
    for page in reader.pages:
        assert float(page.mediabox.width) == page_side
        assert float(page.mediabox.height) == page_side
    print(f"完成：{output}")
    print("验证：40张PNG，1254×1254；PDF共40页，顺序连续。")


if __name__ == "__main__":
    main()
