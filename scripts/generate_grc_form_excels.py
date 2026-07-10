#!/usr/bin/env python3
from __future__ import annotations

import html
import re
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "assets" / "downloads" / "grc"
FORM_FILES = sorted(ROOT.glob("grc-frm*.html"))


def clean(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return html.unescape(text)


def form_id(path: Path, soup: BeautifulSoup) -> str:
    h1 = clean(soup.find("h1").get_text(" ", strip=True)) if soup.find("h1") else path.stem.upper()
    match = re.search(r"(GRC-FRM-[A-Z0-9-]+)", h1, re.I)
    if match:
        return match.group(1).upper()
    title = clean(soup.title.get_text(" ", strip=True)) if soup.title else path.stem.upper()
    match = re.search(r"(GRC-FRM-[A-Z0-9-]+)", title, re.I)
    return match.group(1).upper() if match else path.stem.upper()


def replace_controls(cell) -> str:
    for control in cell.find_all(["input", "textarea", "select"]):
        placeholder = control.get("placeholder") or control.get("value") or ""
        if control.name == "select":
            options = [clean(o.get_text(" ", strip=True)) for o in control.find_all("option")]
            placeholder = " / ".join([o for o in options if o]) or placeholder
        control.replace_with(f"[{placeholder or 'Fill'}]")
    return clean(cell.get_text(" ", strip=True))


def nearest_section(node) -> str:
    current = node
    while current:
        header = None
        if getattr(current, "select_one", None):
            header = current.select_one(".frm-section-header h3, .section-title, h2, h3")
        if header:
            return clean(header.get_text(" ", strip=True))
        current = current.parent
    return "Form"


def extract_rows(path: Path) -> tuple[str, str, list[list[str]]]:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    fid = form_id(path, soup)
    title = clean(soup.find("h1").get_text(" ", strip=True)) if soup.find("h1") else fid
    rows: list[list[str]] = [["Section", "Field / Ref", "Question / Description", "Expected Response", "Evidence / Notes"]]

    seen = set()

    for block in soup.select(".field-block"):
        label = clean(block.select_one(".field-label").get_text(" ", strip=True)) if block.select_one(".field-label") else "Field"
        body_node = block.select_one(".field-body") or block
        body = replace_controls(body_node)
        note = clean(" ".join(n.get_text(" ", strip=True) for n in block.select(".note")))
        section = nearest_section(block)
        row = (section, label, body, "", note)
        if row not in seen:
            rows.append(list(row))
            seen.add(row)

    for table in soup.find_all("table"):
        section = nearest_section(table)
        table_rows = table.find_all("tr")
        if not table_rows:
            continue
        headers = [clean(th.get_text(" ", strip=True)) for th in table_rows[0].find_all(["th", "td"])]
        has_header = bool(table_rows[0].find_all("th"))
        data_rows = table_rows[1:] if has_header else table_rows
        for tr in data_rows:
            cells = [replace_controls(td) for td in tr.find_all(["th", "td"])]
            if not any(cells):
                continue
            if len(cells) == 2:
                row = (section, cells[0], cells[1], "", "")
            elif len(cells) == 3:
                row = (section, cells[0], cells[1], cells[2], "")
            else:
                ref = cells[0] if cells else ""
                question = cells[1] if len(cells) > 1 else ""
                response = cells[2] if len(cells) > 2 else ""
                notes = " | ".join(cells[3:]) if len(cells) > 3 else ""
                if has_header and headers and len(headers) == len(cells):
                    notes = " | ".join(f"{h}: {v}" for h, v in zip(headers[3:], cells[3:]) if v) or notes
                row = (section, ref, question, response, notes)
            if row not in seen:
                rows.append(list(row))
                seen.add(row)

    if len(rows) == 1:
        for item in soup.select("li"):
            text = clean(item.get_text(" ", strip=True))
            if text:
                rows.append(["Guidance", "", text, "", ""])

    return fid, title, rows


def col_name(index: int) -> str:
    name = ""
    index += 1
    while index:
        index, rem = divmod(index - 1, 26)
        name = chr(65 + rem) + name
    return name


def sheet_xml(title: str, rows: list[list[str]]) -> str:
    all_rows = [[title, "", "", "", ""], ["", "", "", "", ""]] + rows
    xml_rows = []
    for r_idx, row in enumerate(all_rows, start=1):
        cells = []
        for c_idx, value in enumerate(row):
            ref = f"{col_name(c_idx)}{r_idx}"
            style = "1" if r_idx == 1 else "2" if r_idx == 3 else "0"
            value = escape(str(value or ""))
            cells.append(f'<c r="{ref}" t="inlineStr" s="{style}"><is><t xml:space="preserve">{value}</t></is></c>')
        xml_rows.append(f'<row r="{r_idx}">{"".join(cells)}</row>')
    dimension = f"A1:E{len(all_rows)}"
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <dimension ref="{dimension}"/>
  <sheetViews><sheetView workbookViewId="0"><pane ySplit="3" topLeftCell="A4" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>
  <sheetFormatPr defaultRowHeight="18"/>
  <cols><col min="1" max="1" width="28" customWidth="1"/><col min="2" max="2" width="26" customWidth="1"/><col min="3" max="3" width="58" customWidth="1"/><col min="4" max="4" width="32" customWidth="1"/><col min="5" max="5" width="42" customWidth="1"/></cols>
  <sheetData>{"".join(xml_rows)}</sheetData>
  <autoFilter ref="A3:E{len(all_rows)}"/>
</worksheet>'''


def workbook_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets><sheet name="Form" sheetId="1" r:id="rId1"/></sheets>
</workbook>'''


def styles_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="3"><font><sz val="10"/><name val="Aptos"/></font><font><b/><sz val="16"/><color rgb="FFFFFFFF"/><name val="Aptos Display"/></font><font><b/><sz val="10"/><color rgb="FFFFFFFF"/><name val="Aptos"/></font></fonts>
  <fills count="4"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF0F2E4D"/></patternFill></fill><fill><patternFill patternType="solid"><fgColor rgb="FF1A4A7A"/></patternFill></fill></fills>
  <borders count="2"><border/><border><left style="thin"><color rgb="FFD9E2EF"/></left><right style="thin"><color rgb="FFD9E2EF"/></right><top style="thin"><color rgb="FFD9E2EF"/></top><bottom style="thin"><color rgb="FFD9E2EF"/></bottom></border></borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="3"><xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf><xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="center"/></xf><xf numFmtId="0" fontId="2" fillId="3" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf></cellXfs>
  <cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>'''


def write_xlsx(path: Path, title: str, rows: list[list[str]]) -> None:
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>''')
        z.writestr("_rels/.rels", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>''')
        z.writestr("xl/_rels/workbook.xml.rels", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>''')
        z.writestr("xl/workbook.xml", workbook_xml())
        z.writestr("xl/worksheets/sheet1.xml", sheet_xml(title, rows))
        z.writestr("xl/styles.xml", styles_xml())
        z.writestr("docProps/core.xml", f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>{escape(title)}</dc:title><dc:creator>O Lado B</dc:creator></cp:coreProperties>''')
        z.writestr("docProps/app.xml", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>O Lado B KB</Application></Properties>''')


def download_block(fid: str, xlsx_name: str) -> str:
    return f'''  <div class="download-box">
    <strong>Excel version available.</strong>
    <span>Use the spreadsheet version when collecting responses, evidence, scores, or approvals.</span>
    <a href="assets/downloads/grc/{xlsx_name}" download>Download Excel version</a>
  </div>
'''


def ensure_download_link(path: Path, fid: str, xlsx_name: str) -> None:
    text = path.read_text(encoding="utf-8")
    if "assets/downloads/grc/" in text:
        return
    style = """
  .download-box { display:flex; align-items:center; gap:12px; flex-wrap:wrap; background:#E8F0FA; border:0.5px solid #B9D1EA; border-left:4px solid #1A4A7A; border-radius:10px; padding:0.9rem 1.1rem; margin:0 0 1.25rem 0; font-size:13px; color:#0F2E4D; }
  .download-box strong { color:#0F2E4D; }
  .download-box span { color:#444; flex:1; }
  .download-box a { color:#1A4A7A; font-weight:700; text-decoration:none; background:#fff; border:0.5px solid #B9D1EA; border-radius:6px; padding:5px 10px; }
"""
    text = text.replace("</style>", style + "</style>", 1) if "</style>" in text else text
    block = download_block(fid, xlsx_name)
    hero_end = text.find("</div>", text.find("kb-page-hero"))
    if hero_end != -1:
        text = text[: hero_end + 6] + "\n" + block + text[hero_end + 6 :]
    else:
        wrapper = text.find('<div class="page-wrapper">')
        insert_at = text.find(">", wrapper) + 1 if wrapper != -1 else text.find("<body>")
        text = text[:insert_at] + "\n" + block + text[insert_at:]
    path.write_text(text, encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    generated = []
    for path in FORM_FILES:
        fid, title, rows = extract_rows(path)
        xlsx_name = f"{path.stem}.xlsx"
        write_xlsx(OUT_DIR / xlsx_name, title, rows)
        ensure_download_link(path, fid, xlsx_name)
        generated.append((fid, xlsx_name, len(rows) - 1))
    for fid, xlsx_name, count in generated:
        print(f"{fid}: {xlsx_name} ({count} rows)")


if __name__ == "__main__":
    main()
