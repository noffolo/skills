#!/usr/bin/env python3
"""Integration test for project_scan using a mock Android project."""

import json
import shutil
import sys
import tempfile
from pathlib import Path


def create_mock_project(root: Path):
    """Create a minimal Android project structure for testing."""
    
    # === settings.gradle.kts (module declarations) ===
    (root / "settings.gradle.kts").write_text(
        'include(":app")\n'
        'include(":core:common")\n'
        'include(":feature:home")\n',
        encoding="utf-8",
    )
    
    # === app module ===
    app = root / "app"
    app_res = app / "src" / "main" / "res" / "values"
    app_res.mkdir(parents=True)
    
    (app / "build.gradle.kts").write_text(
        'plugins { id("com.android.application") }\n'
        "dependencies {\n"
        '    implementation(project(":core:common"))\n'
        '    implementation(project(":feature:home"))\n'
        '    implementation("com.google.android.material:material:1.11.0")\n'
        "}\n",
        encoding="utf-8",
    )
    
    (app_res / "colors.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        "<resources>\n"
        '    <color name="primary">#FF6200EE</color>\n'
        '    <color name="primary_dark">#FF3700B3</color>\n'
        '    <color name="accent">#FF03DAC5</color>\n'
        '    <color name="text_primary">#FF0F0F0F</color>\n'
        '    <color name="text_secondary">#FF666666</color>\n'
        '    <color name="bg_white">#FFFFFFFF</color>\n'
        "</resources>\n",
        encoding="utf-8",
    )
    
    (app_res / "strings.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        "<resources>\n"
        '    <string name="app_name">DotFortune</string>\n'
        '    <string name="notification_settings">Notification Settings</string>\n'
        '    <string name="cancel">Cancel</string>\n'
        '    <string name="confirm">Confirm</string>\n'
        "</resources>\n",
        encoding="utf-8",
    )
    
    (app_res / "dimens.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        "<resources>\n"
        '    <dimen name="margin_normal">16dp</dimen>\n'
        '    <dimen name="text_size_title">18sp</dimen>\n'
        "</resources>\n",
        encoding="utf-8",
    )
    
    # Drawable
    drawable_dir = app / "src" / "main" / "res" / "drawable"
    drawable_dir.mkdir(parents=True)
    (drawable_dir / "bg_card.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<shape xmlns:android="http://schemas.android.com/apk/res/android"\n'
        '    android:shape="rectangle">\n'
        '    <solid android:color="#FFFFFFFF" />\n'
        '    <corners android:radius="12dp" />\n'
        '    <stroke android:width="1dp" android:color="#FFE0E0E0" />\n'
        "</shape>\n",
        encoding="utf-8",
    )
    
    # Custom Views
    kt_dir = app / "src" / "main" / "java" / "com" / "dotfortune" / "widget"
    kt_dir.mkdir(parents=True)
    (kt_dir / "CompactSwitchCompat.kt").write_text(
        "package com.dotfortune.widget\n\n"
        "class CompactSwitchCompat(context: Context) : SwitchCompat(context) {\n"
        "}\n",
        encoding="utf-8",
    )
    (kt_dir / "RoundImageView.kt").write_text(
        "package com.dotfortune.widget\n\n"
        "class RoundImageView(context: Context) : ImageView(context) {\n"
        "}\n",
        encoding="utf-8",
    )
    
    # === core:common module (dependency) ===
    core = root / "core" / "common"
    core_res = core / "src" / "main" / "res" / "values"
    core_res.mkdir(parents=True)
    (core / "build.gradle.kts").write_text(
        'plugins { id("com.android.library") }\n', encoding="utf-8"
    )
    (core_res / "colors.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        "<resources>\n"
        '    <color name="core_divider">#FFE0E0E0</color>\n'
        '    <color name="core_background">#FFF5F5F5</color>\n'
        "</resources>\n",
        encoding="utf-8",
    )
    
    # === feature:home module (dependency, empty res) ===
    home = root / "feature" / "home"
    home.mkdir(parents=True)
    (home / "build.gradle.kts").write_text(
        'plugins { id("com.android.library") }\n', encoding="utf-8"
    )


def main():
    tmp = Path(tempfile.mkdtemp(prefix="mock_android_"))
    print(f"Mock project: {tmp}")
    
    try:
        create_mock_project(tmp)
        
        # Import scanner
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
        from project_scan import scan_project, format_text_report
        
        report = scan_project(str(tmp))
        
        # Print text report
        print(format_text_report(report))
        print()
        
        # Verify results
        errors = []
        
        s = report["summary"]
        # app + core:common = 2 scannable, feature:home has no src/main so skipped
        if s["modules_scanned"] != 2:
            errors.append(f"Expected 2 modules scanned, got {s['modules_scanned']}")
        if ":feature:home" not in report.get("modules_skipped", []):
            errors.append("Expected :feature:home in skipped modules")
        if s["colors"] != 8:  # 6 app + 2 core
            errors.append(f"Expected 8 colors, got {s['colors']}")
        if s["strings"] != 4:
            errors.append(f"Expected 4 strings, got {s['strings']}")
        if s["dimens"] != 2:
            errors.append(f"Expected 2 dimens, got {s['dimens']}")
        if s["drawables"] != 1:
            errors.append(f"Expected 1 drawable, got {s['drawables']}")
        if s["custom_views"] != 2:
            errors.append(f"Expected 2 custom views, got {s['custom_views']}")
        
        # Check color index
        ci = report["indices"]["colors"]
        if ci.get("#FF6200EE") != "@color/primary":
            errors.append(f"Color index missing #FF6200EE -> @color/primary")
        if ci.get("#FFE0E0E0") not in ("@color/core_divider",):
            # Could be core_divider (first module with this hex)
            # Actually app doesn't have this hex in colors.xml, only in drawable stroke
            pass
        
        # Check string index
        si = report["indices"]["strings"]
        if si.get("Cancel") != "@string/cancel":
            errors.append(f"String index missing 'Cancel'")
        
        # Check custom views
        view_names = {v["name"] for v in report["custom_views"]}
        if "CompactSwitchCompat" not in view_names:
            errors.append("Missing CompactSwitchCompat")
        if "RoundImageView" not in view_names:
            errors.append("Missing RoundImageView")
        
        # Check drawables
        if report["drawables"]:
            d = report["drawables"][0]
            if d["name"] != "bg_card":
                errors.append(f"Expected drawable bg_card, got {d['name']}")
            if d.get("cornerRadius") != "12dp":
                errors.append(f"Expected cornerRadius 12dp, got {d.get('cornerRadius')}")
        
        print("---")
        if errors:
            print("FAILURES:")
            for e in errors:
                print(f"  x {e}")
            sys.exit(1)
        else:
            print("All checks passed!")
        
        # Also test JSON output
        json_str = json.dumps(report, indent=2, ensure_ascii=False, default=str)
        parsed = json.loads(json_str)
        print(f"JSON serialization OK ({len(json_str)} bytes)")
        
    finally:
        shutil.rmtree(tmp)
        print("Mock project cleaned up.")


if __name__ == "__main__":
    main()
