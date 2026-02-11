#!/usr/bin/env python3
"""Deterministic K-UX v1 conformance verifier (reference implementation)."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

INVARIANTS = {
    "collapse_only",
    "field_perception",
    "compression_law",
    "unreachable_states",
}
MODES = {"svg", "dom", "css", "canvas", "terminal"}
SHA256_RE = re.compile(r"^sha256:[a-f0-9]{64}$")


def sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def compute_projection_hash(collapse_result_hash: str, projection: dict[str, Any]) -> str:
    canonical = json.dumps(
        {
            "collapse_result_hash": collapse_result_hash,
            "mode": projection["mode"],
            "layout": projection["layout"],
            "styling": projection["styling"],
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(canonical)


def _require_keys(obj: dict[str, Any], keys: list[str], path: str, errors: list[str]) -> None:
    for key in keys:
        if key not in obj:
            errors.append(f"{path}.{key}: missing")


def verify_kux(document: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []

    if document.get("@kux") != "v1":
        errors.append("@kux must equal 'v1'")
    if document.get("@status") != "canonical":
        errors.append("@status must equal 'canonical'")

    _require_keys(document, ["source", "projection", "replay", "proof_surface"], "root", errors)
    source = document.get("source", {})
    projection = document.get("projection", {})
    replay = document.get("replay", {})
    proof = document.get("proof_surface", {})

    if isinstance(source, dict):
        _require_keys(
            source,
            ["collapse_result_hash", "collapse_trace_hash", "entropy", "invariants", "compression_ratio"],
            "source",
            errors,
        )
        for h in ("collapse_result_hash", "collapse_trace_hash"):
            value = source.get(h)
            if not isinstance(value, str) or not SHA256_RE.match(value):
                errors.append(f"source.{h} must match sha256:[a-f0-9]{{64}}")
        if source.get("entropy") != 0.21:
            errors.append("source.entropy must equal 0.21")
        inv = source.get("invariants")
        if not isinstance(inv, list) or len(inv) < 1 or len(inv) != len(set(inv)):
            errors.append("source.invariants must be a non-empty unique list")
        elif not set(inv).issubset(INVARIANTS):
            errors.append("source.invariants contains non-canonical values")
        cr = source.get("compression_ratio")
        if not isinstance(cr, (int, float)) or cr < 0:
            errors.append("source.compression_ratio must be a number >= 0")

    if isinstance(projection, dict):
        _require_keys(projection, ["mode", "layout", "styling"], "projection", errors)
        if projection.get("mode") not in MODES:
            errors.append("projection.mode must be one of svg|dom|css|canvas|terminal")
        if projection.get("layout") != "deterministic":
            errors.append("projection.layout must equal 'deterministic'")
        styling = projection.get("styling")
        if not isinstance(styling, dict):
            errors.append("projection.styling must be an object")
        else:
            if styling.get("pure") is not True:
                errors.append("projection.styling.pure must be true")
            if styling.get("no_runtime_injection") is not True:
                errors.append("projection.styling.no_runtime_injection must be true")
        anim = projection.get("animation")
        if isinstance(anim, dict):
            if anim.get("allowed") not in (None, False):
                errors.append("projection.animation.allowed must be false when provided")
            if anim.get("async") not in (None, False):
                errors.append("projection.animation.async must be false when provided")

    if isinstance(replay, dict):
        _require_keys(
            replay,
            ["replay_identity_required", "hash_projection", "input_hash", "render_deterministic"],
            "replay",
            errors,
        )
        if replay.get("replay_identity_required") is not True:
            errors.append("replay.replay_identity_required must be true")
        if replay.get("render_deterministic") is not True:
            errors.append("replay.render_deterministic must be true")
        for h in ("hash_projection", "input_hash"):
            value = replay.get(h)
            if not isinstance(value, str) or not SHA256_RE.match(value):
                errors.append(f"replay.{h} must match sha256:[a-f0-9]{{64}}")

    if isinstance(proof, dict):
        _require_keys(proof, ["show_entropy", "show_invariants", "show_compression_ratio"], "proof_surface", errors)

    replay_identity_valid = False
    if isinstance(source, dict) and isinstance(projection, dict) and isinstance(replay, dict):
        if "collapse_result_hash" in source and "mode" in projection and "layout" in projection and "styling" in projection:
            expected = compute_projection_hash(source["collapse_result_hash"], projection)
            replay_identity_valid = replay.get("hash_projection") == expected
            if not replay_identity_valid:
                errors.append("replay.hash_projection does not match deterministic projection hash")

    result = {
        "schema_valid": len([e for e in errors if "hash_projection" not in e]) == 0,
        "entropy_valid": isinstance(source, dict) and source.get("entropy") == 0.21,
        "replay_identity_valid": replay_identity_valid,
        "deterministic_projection": isinstance(projection, dict)
        and projection.get("layout") == "deterministic"
        and isinstance(replay, dict)
        and replay.get("render_deterministic") is True,
        "errors": errors,
    }
    result["passed"] = result["entropy_valid"] and result["replay_identity_valid"] and result["deterministic_projection"] and not errors
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify K-UX v1 conformance")
    parser.add_argument("document", type=Path, help="Path to K-UX JSON document")
    args = parser.parse_args()

    try:
        doc = json.loads(args.document.read_text(encoding="utf-8"))
    except Exception as exc:
        print(json.dumps({"passed": False, "errors": [f"invalid_json: {exc}"]}, indent=2))
        return 2

    result = verify_kux(doc)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
