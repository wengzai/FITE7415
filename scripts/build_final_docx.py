from __future__ import annotations

import html
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "Program" / "XAUUSD-ZEntry-Grid" / "final_report"
SOURCE = REPORT_DIR / "Final_Report.md"
OUTPUT = REPORT_DIR / "FITE7415_XAUUSD_Round35_Final_Report.docx"

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
}


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def clean_inline(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", text)
    return text


def text_run(text: str, bold: bool = False, italic: bool = False, code: bool = False) -> str:
    props = []
    if bold:
        props.append("<w:b/>")
    if italic:
        props.append("<w:i/>")
    if code:
        props.append('<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>')
    rpr = f"<w:rPr>{''.join(props)}</w:rPr>" if props else ""
    return f"<w:r>{rpr}<w:t xml:space=\"preserve\">{esc(text)}</w:t></w:r>"


def paragraph(
    text: str = "",
    style: str | None = None,
    bold: bool = False,
    italic: bool = False,
    code: bool = False,
    align: str | None = None,
) -> str:
    ppr_bits = []
    if style:
        ppr_bits.append(f'<w:pStyle w:val="{style}"/>')
    if align:
        ppr_bits.append(f'<w:jc w:val="{align}"/>')
    ppr = f"<w:pPr>{''.join(ppr_bits)}</w:pPr>" if ppr_bits else ""
    return f"<w:p>{ppr}{text_run(clean_inline(text), bold=bold, italic=italic, code=code)}</w:p>"


def code_block(lines: list[str]) -> str:
    body = []
    for line in lines:
        body.append(paragraph(line, style="Code", code=True))
    return "".join(body)


def parse_table(lines: list[str], start: int) -> tuple[str, int]:
    table_lines: list[str] = []
    i = start
    while i < len(lines) and lines[i].strip().startswith("|"):
        table_lines.append(lines[i].strip())
        i += 1

    rows: list[list[str]] = []
    for idx, line in enumerate(table_lines):
        cells = [clean_inline(cell.strip()) for cell in line.strip("|").split("|")]
        if idx == 1 and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells):
            continue
        rows.append(cells)

    if not rows:
        return "", i

    col_count = max(len(row) for row in rows)
    out = [
        "<w:tbl>",
        "<w:tblPr>",
        '<w:tblW w:w="0" w:type="auto"/>',
        '<w:tblLook w:firstRow="1" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>',
        "<w:tblBorders>"
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        "</w:tblBorders>",
        "</w:tblPr>",
    ]

    for row_index, row in enumerate(rows):
        out.append("<w:tr>")
        padded = row + [""] * (col_count - len(row))
        for cell in padded:
            shd = '<w:shd w:fill="E2E8F0"/>' if row_index == 0 else ""
            out.append(
                "<w:tc>"
                f"<w:tcPr>{shd}</w:tcPr>"
                f"<w:p>{text_run(cell, bold=(row_index == 0))}</w:p>"
                "</w:tc>"
            )
        out.append("</w:tr>")
    out.append("</w:tbl>")
    out.append(paragraph(""))
    return "".join(out), i


def svg_dimensions(path: Path) -> tuple[int, int]:
    root = ET.fromstring(path.read_text(encoding="utf-8"))
    width = root.get("width")
    height = root.get("height")

    def parse_px(value: str | None, default: int) -> int:
        if not value:
            return default
        match = re.search(r"[\d.]+", value)
        return int(float(match.group(0))) if match else default

    return parse_px(width, 960), parse_px(height, 420)


def image_paragraph(rel_id: str, image_id: int, title: str, width_px: int, height_px: int) -> str:
    # 6.5 inches wide, preserve aspect ratio. 1 inch = 914400 EMU.
    max_width_emu = int(6.5 * 914400)
    aspect = height_px / max(width_px, 1)
    cx = max_width_emu
    cy = int(max_width_emu * aspect)
    name = esc(title or f"Figure {image_id}")
    return f"""
<w:p>
  <w:pPr><w:jc w:val="center"/></w:pPr>
  <w:r>
    <w:drawing>
      <wp:inline distT="0" distB="0" distL="0" distR="0">
        <wp:extent cx="{cx}" cy="{cy}"/>
        <wp:docPr id="{image_id}" name="{name}" descr="{name}"/>
        <wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>
        <a:graphic>
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic>
              <pic:nvPicPr>
                <pic:cNvPr id="{image_id}" name="{name}"/>
                <pic:cNvPicPr/>
              </pic:nvPicPr>
              <pic:blipFill>
                <a:blip r:embed="{rel_id}"/>
                <a:stretch><a:fillRect/></a:stretch>
              </pic:blipFill>
              <pic:spPr>
                <a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
              </pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>
  </w:r>
</w:p>
"""


def parse_markdown(markdown: str) -> tuple[str, list[tuple[str, Path]]]:
    lines = markdown.splitlines()
    body: list[str] = []
    images: list[tuple[str, Path]] = []
    i = 0
    in_code = False
    code_lines: list[str] = []

    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            if in_code:
                body.append(code_block(code_lines))
                code_lines = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            code_lines.append(line)
            i += 1
            continue

        if not stripped:
            body.append(paragraph(""))
            i += 1
            continue

        if stripped.startswith("|"):
            tbl, i = parse_table(lines, i)
            body.append(tbl)
            continue

        image_match = re.fullmatch(r"!\[([^\]]*)\]\(([^)]+)\)", stripped)
        if image_match:
            title = image_match.group(1) or "Figure"
            rel_path = Path(image_match.group(2))
            full_path = (REPORT_DIR / rel_path).resolve()
            rel_id = f"rIdImage{len(images) + 1}"
            width_px, height_px = svg_dimensions(full_path)
            images.append((rel_id, full_path))
            body.append(image_paragraph(rel_id, len(images), title, width_px, height_px))
            body.append(paragraph(title, italic=True, align="center"))
            i += 1
            continue

        if stripped.startswith("# "):
            body.append(paragraph(stripped[2:], style="Title"))
        elif stripped.startswith("## "):
            body.append(paragraph(stripped[3:], style="Heading1"))
        elif stripped.startswith("### "):
            body.append(paragraph(stripped[4:], style="Heading2"))
        elif stripped.startswith("#### "):
            body.append(paragraph(stripped[5:], style="Heading3"))
        elif stripped.startswith("- "):
            body.append(paragraph("• " + stripped[2:], style="ListParagraph"))
        elif re.match(r"\d+\. ", stripped):
            body.append(paragraph(stripped, style="ListParagraph"))
        else:
            body.append(paragraph(stripped))
        i += 1

    if code_lines:
        body.append(code_block(code_lines))
    return "".join(body), images


def document_xml(body: str) -> str:
    ns_attrs = " ".join(f'xmlns:{key}="{value}"' for key, value in NS.items())
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document {ns_attrs}>
  <w:body>
    {body}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="720" w:right="720" w:bottom="720" w:left="720" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>
'''


def styles_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:qFormat/>
    <w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="22"/></w:rPr>
    <w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:qFormat/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:after="260"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="36"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:qFormat/>
    <w:pPr><w:spacing w:before="300" w:after="140"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="30"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:qFormat/>
    <w:pPr><w:spacing w:before="220" w:after="100"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="26"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:qFormat/>
    <w:pPr><w:spacing w:before="180" w:after="80"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="24"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="ListParagraph">
    <w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="360"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Code">
    <w:name w:val="Code"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="0" w:after="0"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="18"/></w:rPr>
  </w:style>
</w:styles>
'''


def content_types() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="svg" ContentType="image/svg+xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>
'''


def package_rels() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
'''


def document_rels(images: list[tuple[str, Path]]) -> str:
    rels = [
        '<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
        '<Relationship Id="rIdSettings" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>',
    ]
    for rel_id, image_path in images:
        rels.append(
            f'<Relationship Id="{rel_id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{esc(image_path.name)}"/>'
        )
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n  ' + "\n  ".join(rels) + "\n</Relationships>\n"


def settings_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:zoom w:percent="100"/>
  <w:defaultTabStop w:val="720"/>
</w:settings>
'''


def core_xml() -> str:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>FITE7415 XAUUSD Round 35 Final Report</dc:title>
  <dc:creator>FITE7415 Project Team</dc:creator>
  <cp:lastModifiedBy>FITE7415 Project Team</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>
'''


def app_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Codex</Application>
</Properties>
'''


def build_docx() -> None:
    body, images = parse_markdown(SOURCE.read_text(encoding="utf-8"))
    with zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED) as docx:
        docx.writestr("[Content_Types].xml", content_types())
        docx.writestr("_rels/.rels", package_rels())
        docx.writestr("word/document.xml", document_xml(body))
        docx.writestr("word/_rels/document.xml.rels", document_rels(images))
        docx.writestr("word/styles.xml", styles_xml())
        docx.writestr("word/settings.xml", settings_xml())
        docx.writestr("docProps/core.xml", core_xml())
        docx.writestr("docProps/app.xml", app_xml())
        for _rel_id, image_path in images:
            docx.write(image_path, f"word/media/{image_path.name}")
    print(f"saved {OUTPUT}")


if __name__ == "__main__":
    build_docx()
