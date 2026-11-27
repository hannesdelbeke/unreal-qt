⚠️ This repo is intended for developers. Artists and other non-developers can use the [Unreal Qt plugin](https://github.com/hannesdelbeke/unreal-qt-plugin) instead.

# Unreal Qt

Qt (PySide6) support for Unreal Engine 5. It likely also works with Unreal Engine 4.

- Prevents widgets from disappearing instantly due to garbage collection.
- Automatically styles all Qt widgets using Xingyu Lei's [unreal_stylesheet](https://github.com/leixingyu/UnrealStylesheet).
- Adds an optional dark title bar that better matches Unreal's UI.
- Parents widgets to Unreal's main window so they stay on top.

## Install

1. Copy the `unreal_qt` folder into a directory on Unreal's Python path, for example:
   - project: `D:\Unreal Projects\MyProject\Content\Python\Lib`
   - editor: `D:\Program Files\Epic Games\UE_5.4\Engine\Binaries\ThirdParty\Python3\Win64\Lib\site-packages`
2. Run the setup code when Unreal starts, for example from a plugin or an `init_unreal.py` file. See the [docs](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python).

## Quickstart

This guide assumes that PySide6 is already installed.

1. Add the `unreal_qt` folder to your Python path. See the [Unreal docs](https://docs.unrealengine.com/4.27/en-US/ProductionPipelines/ScriptingAndAutomation/Python/#pythonpathsintheunrealeditor).
2. Create `sample.py` with the snippet below, and add it to Unreal's Python path.
```python
# 1. IMPORT MODULE
import unreal_qt
from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout
from PySide6.QtCore import Qt

# INIT MODULE - this step can run automatically on editor startup if added to init_unreal.py
unreal_qt.setup()

# 2. CREATE WIDGET
w = QWidget()
layout = QVBoxLayout()
w.setLayout(layout)
layout.addWidget(QLabel("Hello World!"))

# DELETE THE WIDGET WHEN IT IS CLOSED
w.setAttribute(Qt.WA_DeleteOnClose, True)

# 3. WRAP WIDGET
unreal_qt.wrap(w)

# 4. SHOW WIDGET
w.show()
```
3. Import the script in Unreal's Python console to run it.
```python
import sample
```

![unreal_qt widget in Unreal Engine](https://user-images.githubusercontent.com/3758308/191580757-f3993797-da80-449e-b9d4-ad311b2f37c5.png)


<details>
 <summary>Dark title bar</summary>

## Dark title bar

On Windows, the window title bar is white by default, and Qt can't change its color.

With unreal_qt, you can add a custom title bar.

- Default window bar and frame

![Default window bar and frame](https://user-images.githubusercontent.com/3758308/191618705-45914a58-893b-4680-995e-976571b7c7eb.png)

- Custom bar, no frame (no resize support)

![Custom bar without a frame](https://user-images.githubusercontent.com/3758308/191618309-13e7329f-4310-407a-9eef-383a113e1ac1.png)

- Custom bar and frame, no title bar (supports resizing)

![Custom bar and frame without a title bar](https://user-images.githubusercontent.com/3758308/191618151-319b8530-addb-4b9a-a51f-5da0a90a4fd3.png)

</details>

## Community

- tech-artists.org thread: [PySide and Unreal5](https://discourse.techart.online/t/pyside-and-unreal5/15475/6)
- [ ] TODO: Unreal forums thread

## Similar projects

- [Unreal-PyToolkit](https://github.com/FXTD-ODYSSEY/Unreal-PyToolkit)
