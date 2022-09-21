# unreal_qt
QT PySide2 support for unreal engine 5 (likely works in unreal 4)

automated styling using [unreal_stylesheet](https://github.com/leixingyu/UnrealStylesheet)

## Quickstart

1. Add the unreal_qt folder in your python path. See [unreal docs](https://docs.unrealengine.com/4.27/en-US/ProductionPipelines/ScriptingAndAutomation/Python/#pythonpathsintheunrealeditor)
2. create following sample script and add to unreal python path.
```python
import unreal_qt
unreal_qt.setup()  # if you put the setup in an init_unreal.py file, unreal will run setup on startup

# every widget you make after setup won't block the editor & have unreal styling
from PySide2.QtWidgets import QLabel, QWidget, QVBoxLayout

w = QWidget()
layout = QVBoxLayout()
w.setLayout(layout)
layout.addWidget(QLabel("Hello World!"))
w.show()
```
3. import script in unreal with the Python terminal to run it.

![image](https://user-images.githubusercontent.com/3758308/191580757-f3993797-da80-449e-b9d4-ad311b2f37c5.png)

## Dark title bar
The windows bar is by default white on Windows, and QT can't change the bar color.

With unreal_qt you can add a custom bar.

- default window bar & frame

![image](https://user-images.githubusercontent.com/3758308/191618705-45914a58-893b-4680-995e-976571b7c7eb.png)

- custom bar, no frame (no resize support!)

![image](https://user-images.githubusercontent.com/3758308/191618309-13e7329f-4310-407a-9eef-383a113e1ac1.png)

- custom bar, frame, no title bar (supports resize)

![image](https://user-images.githubusercontent.com/3758308/191618151-319b8530-addb-4b9a-a51f-5da0a90a4fd3.png)


## Engine resource browser
Included is a bare bones resource browser, letting you browse default unreal icons & shapes that can be used in your qt-tools
- filter by file type
- search bar to search resources

![image](https://user-images.githubusercontent.com/3758308/191581830-d0a527ec-cd5a-4724-9454-60f418bd93f0.png)
