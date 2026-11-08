#!/usr/bin/env python3
"""Static validation of P2 RTL curriculum diagrams.

This validates JSON/graph structure only. It does not run RTL simulation,
Vivado synthesis/implementation, GitHub Pages rendering, or Basys3 hardware.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "chapters"
DOCS = ROOT / "docs" / "rtl"
MODULES = {
    1: ["P2_01_basys3_top.v"],
    2: ["basys3_soc11_top_p2_02.v", "fnd_scan_controller.v",
        "p2_02_axi_fnd_v1_0.v", "p2_02_axi_fnd_v1_0_S00_AXI.v"],
    3: ["basys3_soc11_top_p2_03.v", "button_event_core.v",
        "p2_03_axi_buttons_v1_0.v", "p2_03_axi_buttons_v1_0_S00_AXI.v"],
    4: ["basys3_soc11_top_p2_04.v", "p2_04_axi_pwm_v1_0.v",
        "p2_04_axi_pwm_v1_0_S00_AXI.v", "pwm_core.v"],
    5: ["auto_light_controller.v", "basys3_soc11_top_p2_05.v",
        "cds_digital_core.v", "p2_04_axi_pwm_v1_0.v",
        "p2_04_axi_pwm_v1_0_S00_AXI.v", "p2_05_axi_cds_v1_0.v",
        "p2_05_axi_cds_v1_0_S00_AXI.v", "pwm_core.v"],
    6: ["basys3_soc11_top_p2_06.v", "hc_sr04_core.v",
        "p2_06_axi_sonic_v1_0.v", "p2_06_axi_sonic_v1_0_S00_AXI.v"],
    7: ["basys3_soc11_top_p2_07.v", "motor_controller.v",
        "p2_07_axi_motor_v1_0.v", "p2_07_axi_motor_v1_0_S00_AXI.v"],
    8: ["basys3_soc11_top_p2_08.v"],
    9: ["basys3_soc11_top_p2_08.v"],
    10: ["basys3_soc11_top_p2_08.v"],
}

def verify_page(path, idx, page, problems):
    label = f"{path.name}:page{idx}"
    nodes = page.get("nodes", [])
    edges = page.get("edges", [])
    ids = [node.get("id") for node in nodes]
    if len(ids) != len(set(ids)):
        problems.append(f"{label}: duplicate node ID")
    known = set(ids)
    width, height = page.get("width", 0), page.get("height", 0)
    if page.get("verification") != "DESIGN_DRAFT_NOT_CODE_VERIFIED":
        problems.append(f"{label}: unsupported verification claim")
    for node in nodes:
        key = node.get("id")
        x, y, w, h = (node.get(k, 0) for k in ("x", "y", "w", "h"))
        if w <= 0 or h <= 0 or x-w/2 < 0 or x+w/2 > width or y-h/2 < 0 or y+h/2 > height:
            problems.append(f"{label}: node {key} outside canvas")
        if node.get("pad") != 6 or node.get("padY") != 4:
            problems.append(f"{label}: node {key} padding differs from baseline")
    for i, first in enumerate(nodes):
        for second in nodes[i+1:]:
            if (2*abs(first["x"]-second["x"]) < first["w"]+second["w"] and
                2*abs(first["y"]-second["y"]) < first["h"]+second["h"]):
                problems.append(f'{label}: overlap {first["id"]}/{second["id"]}')
    for edge in edges:
        if edge.get("from") not in known or edge.get("to") not in known:
            problems.append(f'{label}: dangling edge {edge.get("id")}')
    return len(nodes), len(edges)


def main():
    issues, counts = [], {"chapters": 0, "pages": 0, "modules": 0, "nodes": 0, "edges": 0}
    for chapter, expected in MODULES.items():
        id_ = f"{chapter:02d}"
        path = CHAPTERS / f"P2_{id_}_rtl_pages.json"
        guide = DOCS / f"P2_{id_}_RTL.md"
        if not path.is_file() or not guide.is_file():
            issues.append(f"{id_}: missing RTL diagram or guide")
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        pages = doc.get("pages", [])
        if doc.get("format") != "soc-flow-pages" or doc.get("diagramType") != "RTL":
            issues.append(f"{id_}: incompatible document format")
        actual = [page.get("sourceFile") for page in pages[1:]]
        if actual != expected:
            issues.append(f"{id_}: module source inventory does not match provided ZIP")
        counts["chapters"] += 1
        counts["pages"] += len(pages)
        counts["modules"] += len(pages) - 1
        for idx, page in enumerate(pages, 1):
            n, e = verify_page(path, idx, page, issues)
            counts["nodes"] += n
            counts["edges"] += e
    if issues:
        print("STATIC_RTL_DIAGRAM_FAIL")
        for issue in issues:
            print(" -", issue)
        raise SystemExit(1)
    print("STATIC_RTL_DIAGRAM_PASS", counts)
    print("NOT VERIFIED: RTL_SIM / SYNTH_TIMING / BOARD / WEB")


if __name__ == "__main__":
    main()
