#!/usr/bin/env python3
"""Build one host-neutral FLD1 asset pack from the existing per-asset release ZIPs."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
import zipfile
from pathlib import Path

ASSETS = {
    "AEHandoff_VortexRing_20K_v01.zip": {
        "folder": "VortexRing_20K",
        "title": "Vortex Ring 20K",
        "ja": "波打つトーラス内の循環と断面旋回を解析式で生成した粒子場です。流体ソルバーの結果ではありません。",
        "en": "An analytic particle field with toroidal circulation, coherent waves, and tube swirl. It is not a fluid-solver result.",
        "count": 20000, "samples": 49, "sps": 12, "rotation": [0, 0, 0],
    },
    "AEHandoff_SmokePointSource_20K_v01.zip": {
        "folder": "SmokePointSource_20K",
        "title": "Smoke Point Source 20K",
        "ja": "一点から順次発生し、上昇流れと粒子ごとの分散で広がる手続き粒子場です。密度・浮力・圧力は解いていません。",
        "en": "A procedural particle field emitted sequentially from one point into a rising, dispersing flow. Density, buoyancy, and pressure are not solved.",
        "count": 20000, "samples": 49, "sps": 12, "rotation": [-75, 0, 0],
    },
    "AEHandoff_RippleSheet_20K_v01.zip": {
        "folder": "RippleSheet_20K",
        "title": "Ripple Sheet 20K",
        "ja": "平面点群に進行波とたなびきを与えた解析的な粒子場です。",
        "en": "An analytic sheet-like particle field with travelling waves and undulation.",
        "count": 20000, "samples": 49, "sps": 12, "rotation": [15, 0, 0],
    },
    "AEHandoff_WindTunnel_20K_v01.zip": {
        "folder": "WindTunnel_20K",
        "title": "Wind Tunnel 20K",
        "ja": "円柱まわりのポテンシャル流れと手続き的な非定常後流を組み合わせた粒子場です。CFDや実験との定量比較用ではありません。",
        "en": "A particle field combining potential flow around a cylinder with a procedural unsteady wake. It is not intended for quantitative CFD or experimental comparison.",
        "count": 20000, "samples": 49, "sps": 12, "rotation": [0, 0, 0],
    },
    "AEHandoff_PlaneToTorus_20K_v01.zip": {
        "folder": "PlaneToTorus_20K",
        "title": "Plane to Torus 20K",
        "ja": "同一の粒子IDを保ったまま、XY平面からトーラスへ幾何学的に変形する粒子場です。",
        "en": "A geometric morph from an XY plane to a torus while preserving particle identity.",
        "count": 20000, "samples": 49, "sps": 12, "rotation": [0, 0, 0],
    },
    "AEHandoff_VortexRing_1M_v01.zip": {
        "folder": "VortexRing_1M",
        "title": "Vortex Ring 1M",
        "ja": "Vortex Ringの100万粒子版です。17保存サンプルで、20K版と同じ座標・進行範囲を使用します。",
        "en": "The one-million-particle Vortex Ring variant. It uses 17 stored samples with the same coordinate and progression range as the 20K version.",
        "count": 1000000, "samples": 17, "sps": 4, "rotation": [0, 0, 0],
    },
}

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def useful_root(extracted: Path) -> Path:
    items = [p for p in extracted.iterdir() if p.name != "__MACOSX"]
    if len(items) == 1 and items[0].is_dir():
        return items[0]
    return extracted

def neutralize_json(path: Path) -> None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return
    if not isinstance(data, dict):
        return
    ae = data.pop("suggested_ae", None)
    if isinstance(ae, dict):
        data["suggested_playback"] = {
            "samples_per_second": ae.get("samples_per_second"),
            "sample_offset": ae.get("sample_offset", 0),
            "note": "Host-side presentation suggestion; timing is not encoded as absolute presentation time in FLD1.",
        }
        data["suggested_view"] = {
            "initial_rotation_xyz_degrees": ae.get("object_rotation_xyz_degrees", [0, 0, 0]),
            "note": "Optional host-side starting orientation; not part of the FLD1 state contract.",
        }
    if "distribution_status" in data:
        data["distribution_status"] = "Public FLD1 asset pack; distributed cache/settings/previews are CC0-1.0."
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def per_asset_readme(meta: dict, lang: str) -> str:
    r = meta["rotation"]
    if lang == "ja":
        return f"""# {meta['title']}

{meta['ja']}

- FLD1 profile: point3-pv
- 粒子数: {meta['count']:,}
- 保存サンプル数: {meta['samples']}
- 推奨表示速度: {meta['sps']} samples / second
- Sample Offset: 0
- 初期回転XYZの目安: {r[0]}°, {r[1]}°, {r[2]}°
- 座標系: right-handed XYZ, Z-up

推奨表示速度と初期回転はDCC側の表示例であり、FLD1に絶対的な上映時間やカメラ姿勢を固定するものではありません。
AE Handoff、Fusion Handoff、その他のFLD1 readerで同じ粒子状態を利用できます。

このフォルダの配布アセットはCC0-1.0です。
"""
    return f"""# {meta['title']}

{meta['en']}

- FLD1 profile: point3-pv
- Particles: {meta['count']:,}
- Stored samples: {meta['samples']}
- Suggested playback: {meta['sps']} samples / second
- Sample Offset: 0
- Suggested initial XYZ rotation: {r[0]}°, {r[1]}°, {r[2]}°
- Coordinates: right-handed XYZ, Z-up

Playback rate and initial rotation are host-side presentation suggestions. FLD1 does not lock the asset to an absolute presentation duration or camera pose.
The same particle state can be used by AE Handoff, Fusion Handoff, or another FLD1 reader.

Distributed assets in this folder are CC0-1.0.
"""

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--cc0", required=True, type=Path)
    args = ap.parse_args()

    missing = [name for name in ASSETS if not (args.input / name).is_file()]
    if missing:
        raise SystemExit("Missing release assets: " + ", ".join(missing))

    with tempfile.TemporaryDirectory() as td:
        temp = Path(td)
        root = temp / "FLD1_Asset_Pack_v01"
        root.mkdir()

        manifest = {
            "package": "FLD1 Asset Pack",
            "version": "v01",
            "profile": "point3-pv",
            "host_independent": True,
            "license": "CC0-1.0",
            "assets": [],
        }

        for zip_name, meta in ASSETS.items():
            extracted = temp / ("extract_" + meta["folder"])
            extracted.mkdir()
            with zipfile.ZipFile(args.input / zip_name) as zf:
                zf.extractall(extracted)
            src = useful_root(extracted)
            dst = root / meta["folder"]
            dst.mkdir()

            for p in src.rglob("*"):
                if not p.is_file():
                    continue
                upper = p.name.upper()
                if upper.startswith("README") or upper.startswith("SHA256SUMS"):
                    continue
                rel = p.relative_to(src)
                out = dst / rel
                out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, out)

            for p in dst.rglob("*.json"):
                neutralize_json(p)

            (dst / "README_ja.md").write_text(per_asset_readme(meta, "ja"), encoding="utf-8")
            (dst / "README_en.md").write_text(per_asset_readme(meta, "en"), encoding="utf-8")

            fld = sorted(dst.rglob("*.fld1"))
            manifest["assets"].append({
                "name": meta["title"],
                "directory": meta["folder"],
                "particle_count": meta["count"],
                "sample_count": meta["samples"],
                "suggested_samples_per_second": meta["sps"],
                "suggested_initial_rotation_xyz_degrees": meta["rotation"],
                "fld1_files": [str(x.relative_to(root)).replace("\\", "/") for x in fld],
            })

        (root / "README_ja.md").write_text("""# FLD1 Asset Pack v01

FLD1の確認・制作に使える6種類の粒子場を1つにまとめた、ホスト非依存のアセットパックです。

収録内容:
- Vortex Ring 20K
- Smoke Point Source 20K
- Ripple Sheet 20K
- Wind Tunnel 20K
- Plane to Torus 20K
- Vortex Ring 1M

FLD1は粒子状態を渡すための形式です。このパックはAfter Effects専用ではありません。
AE Handoff、Fusion Handoff、またはFLD1仕様に従う別のreaderで利用できます。

新規キャッシュでは保存サンプル番号 q=0,1,2,... を進行座標とし、sample_rate=1、速度は dx/dq です。
各フォルダの推奨 samples / second は表示側の例で、絶対時間をFLD1へ固定するものではありません。

各アセットの説明・粒子数・保存サンプル数・初期姿勢の目安は各フォルダのREADMEを参照してください。
manifest.jsonは機械可読な一覧、SHA256SUMS.txtはパック内ファイルの検証用です。

配布アセットはCC0-1.0です。生成コードそのもののライセンスとは分離されています。
FLD1仕様: https://github.com/goldkiss2010-ai/fld1
DCC Handoff: https://github.com/goldkiss2010-ai/dcc-handoff
""", encoding="utf-8")

        (root / "README_en.md").write_text("""# FLD1 Asset Pack v01

A host-independent bundle of six particle fields for testing and production with FLD1.

Included:
- Vortex Ring 20K
- Smoke Point Source 20K
- Ripple Sheet 20K
- Wind Tunnel 20K
- Plane to Torus 20K
- Vortex Ring 1M

FLD1 is a particle-state handoff format. This pack is not specific to After Effects.
Use it with AE Handoff, Fusion Handoff, or another reader that implements the FLD1 contract.

For new caches, stored sample index q=0,1,2,... is the progression coordinate, sample_rate=1, and velocity is dx/dq.
The suggested samples / second values are host-side presentation examples; FLD1 does not encode an absolute presentation duration.

See each asset folder for description, particle/sample counts, and a suggested initial orientation.
manifest.json provides a machine-readable index and SHA256SUMS.txt verifies files inside the pack.

Distributed assets are CC0-1.0.
FLD1 specification: https://github.com/goldkiss2010-ai/fld1
DCC Handoff: https://github.com/goldkiss2010-ai/dcc-handoff
""", encoding="utf-8")

        shutil.copy2(args.cc0, root / "CC0-1.0.txt")
        (root / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        files = sorted(p for p in root.rglob("*") if p.is_file() and p.name != "SHA256SUMS.txt")
        sums = "\n".join(f"{sha256(p)}  {p.relative_to(root).as_posix()}" for p in files) + "\n"
        (root / "SHA256SUMS.txt").write_text(sums, encoding="utf-8")

        args.output.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(args.output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6, allowZip64=True) as zf:
            for p in sorted(root.rglob("*")):
                if p.is_file():
                    zf.write(p, p.relative_to(root.parent))

    print(f"{args.output.name} {args.output.stat().st_size} bytes sha256={sha256(args.output)}")

if __name__ == "__main__":
    main()
