# Cloth Cache Range Manager

<img width="353" height="326" alt="螢幕擷取畫面 2026-08-13 164059" src="https://github.com/user-attachments/assets/b7286d63-13b2-41b0-a7e9-b7ffc0b1c552" />

A small Blender add-on for managing Cloth simulation cache frame ranges.

Blender Cloth cache ranges are normally stored per Cloth object, which can become inconvenient when a scene contains many Cloth simulations. This add-on provides a simple way to synchronize Cloth cache ranges with the current Scene frame range.

## Features

* Display the current Scene Start and End frames
* Detect all Cloth objects in the current scene
* Detect Cloth cache ranges that do not match the Scene range
* List mismatched Cloth objects
* Select individual mismatched objects
* Select all mismatched Cloth objects
* Sync selected Cloth objects to the Scene range
* Sync all Cloth objects to the Scene range

## Installation

1. Download `cloth_cache_range_manager.py`
2. Open Blender
3. Go to **Edit → Preferences**
4. Open **Add-ons** 
5. Choose **Install from Disk**
6. Select `cloth_cache_range_manager.py`
7. Enable the add-on if necessary

## Usage

Open the 3D Viewport and press `N` to open the Sidebar.

Go to:

**Cloth → Cloth Cache Range Manager**

The panel displays the current Scene frame range and automatically checks Cloth objects for mismatched cache ranges.

Use:

* **Select All Mismatched** to select Cloth objects whose cache range differs from the Scene range
* **Sync Selected Cloth** to update only selected Cloth objects
* **Sync All Cloth** to update every Cloth object in the current scene

## What It Changes

The add-on modifies only the Cloth point-cache frame range:

```python
mod.point_cache.frame_start
mod.point_cache.frame_end
```

It does not automatically bake or delete Cloth caches, and it does not modify Cloth simulation parameters.

## Compatibility

Designed for modern Blender versions using the current Cloth point-cache API.

Tested successfully with the Blender version used during development.

## License

Released under the MIT License. See `LICENSE` for details.

## Credits

Developed with assistance from ChatGPT .
