# unreal_qt
QT PySide2 support for unreal engine 5 (likely works in 4 too)

```python
import unreal_qt
unreal_qt.setup()  # put this in an init_unreal.py file to auto setup on unreal start

# every widget you make after setup won't block the editor & have unreal styling
from PySide2.QtWidgets import QLabel, QWidget, QVBoxLayout

w = QWidget()
layout = QVBoxLayout()
w.setLayout(layout)
layout.addWidget(QLabel("Hello World!"))
w.show()
```
![image](https://user-images.githubusercontent.com/3758308/191580757-f3993797-da80-449e-b9d4-ad311b2f37c5.png)

## Title bar
note that the windows bar is white.
since QT can't change bar color unreal_qt has some options to wrap your widget with a custom bar.
- default window bar & frame (see above image)

![image](https://user-images.githubusercontent.com/3758308/191580757-f3993797-da80-449e-b9d4-ad311b2f37c5.png)

- custom bar, no frame (note you can't resize this one yet!)

![image](https://user-images.githubusercontent.com/3758308/191583138-20abd8f9-386e-4631-bb49-fcc9bb0b1497.png)

- custom bar, frame, no title bar

![image](https://user-images.githubusercontent.com/3758308/191582742-a1c021b0-2aa9-4318-8474-231683d280de.png)


## Engine resource browser
Included is a bare bones resource browser, letting you browse default unreal icons & shapes that can be used in your qt-tools
- filter by file type
- search bar to search resources

![image](https://user-images.githubusercontent.com/3758308/191581830-d0a527ec-cd5a-4724-9454-60f418bd93f0.png)
