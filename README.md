# IngeTrazo Organize Toolbar Plugin

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![IngeTrazo Compatible](https://img.shields.io/badge/IngeTrazo-v0.4%2B-orange.svg)](https://github.com/ingelibre/ingetrazo)
[![Version](https://img.shields.io/badge/Version-1.0.0-green.svg)](https://github.com/seghier/ingetrazo-organize-toolbar/releases)

A dedicated, high-productivity **Organize** toolbar and **Extensions** submenu for [IngeTrazo](https://github.com/ingelibre/ingetrazo).

Provides quick one-click buttons for organizing geometry (hiding, unhiding, reversing faces, and grouping) — mirroring familiar SketchUp workflows with native IngeTrazo styling.

<div align="center">
  <img src="assets/organize_toolbar_preview.png" width="536" alt="Organize Toolbar Preview"/>
</div>

---

## ✨ Features & Actions

### Organize Toolbar

| Icon | Tool | Shortcut | Description |
| :---: | :--- | :---: | :--- |
| <img src="assets/icon_hide.png" width="32" alt="Hide"/> | **Hide** | `Ctrl+H` | Hides the currently selected objects, faces, or edges. |
| <img src="assets/icon_unhide_last.png" width="32" alt="Unhide Last"/> | **Unhide Last** | — | Restores the most recently hidden batch of entities (faces, edges, or groups) in reverse chronological order. |
| <img src="assets/icon_unhide_all.png" width="32" alt="Unhide All"/> | **Unhide All** | — | Restores all hidden elements across the entire scene and open groups. |
| <img src="assets/icon_reverse_face.png" width="32" alt="Reverse Faces"/> | **Reverse Faces** | — | Flips the front and back orientation of selected faces. |
| <img src="assets/icon_group.png" width="32" alt="Make Group"/> | **Make Group** | `Ctrl+G` | Wraps selected geometry into an isolated group. |
| <img src="assets/icon_ungroup.png" width="32" alt="Explode Group"/> | **Explode Group** | `Ctrl+Shift+G` | Dissolves selected groups back into loose geometry. |

---

## 🚀 Installation

### Option 1: Quick Install via Releases (Recommended)

1. Download [`organize_toolbar.py`](https://github.com/seghier/ingetrazo-organize-toolbar/releases/latest/download/organize_toolbar.py) (or the `.zip` archive) from the **[Releases](https://github.com/seghier/ingetrazo-organize-toolbar/releases)** page.
2. Open IngeTrazo and go to:
   **Extensions ▸ Open plugins folder**
3. Place `organize_toolbar.py` into that folder:
   - **Windows**: `%APPDATA%\ingetrazo\plugins\`
   - **Linux**: `~/.local/share/ingetrazo/plugins/`
   - **macOS**: `~/Library/Application Support/ingetrazo/plugins/`
4. Restart IngeTrazo. The **Organize** toolbar will appear at the top, and an **Organize** menu will be added under **Extensions**.

---

### Option 2: 1-Click Install via PowerShell (Windows)

Open PowerShell and paste:

```powershell
$pluginDir = "$env:APPDATA\ingetrazo\plugins"
if (!(Test-Path $pluginDir)) { New-Item -ItemType Directory -Force -Path $pluginDir }
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/seghier/ingetrazo-organize-toolbar/main/organize_toolbar.py" -OutFile "$pluginDir\organize_toolbar.py"
Write-Host "IngeTrazo Organize Toolbar installed successfully!" -ForegroundColor Green
```

---

### Option 3: Git Clone directly into Plugins

```bash
# Windows (PowerShell)
cd "$env:APPDATA\ingetrazo\plugins"
git clone https://github.com/seghier/ingetrazo-organize-toolbar.git organize_toolbar_plugin
copy organize_toolbar_plugin\organize_toolbar.py .

# Linux
cd ~/.local/share/ingetrazo/plugins
git clone https://github.com/seghier/ingetrazo-organize-toolbar.git
```

---

## 🎨 Design & Quality Details

- **Crisp Vector Icons**: Drawn programmatically via `QPainter` paths at 48×48 high-DPI resolution. No external SVG files or raster icons required.
- **Theme-Aware**: Ink dynamically adapts to the host window palette (`#ECEFF1` on dark theme, `#21252B` on light theme) with IngeTrazo's signature orange accent (`#F37329`).
- **Robust Unhide Engine**: Correctly detects and restores hidden faces (`attrs['hidden']`), edges, groups, and multi-selection compound commands without crashing or dropping elements.
- **Defensive Error Handling**: Safe invocation wrappers ensure the plugin loads seamlessly across all IngeTrazo builds (packaged executables or source builds) without breaking core application startup.

---

## 📄 License

Distributed under the [GNU General Public License v3.0 or later (GPL-3.0-or-later)](LICENSE).
