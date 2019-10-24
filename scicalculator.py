import PySimpleGUI as sg

from scipy.constants import *
from numpy import *

help_text = """
version: 0.1

使用了
```
    from scipy.constants import *
    from numpy import *
```
的方式导入环境变量

键盘绑定：
    DEL     -       一键清除输入文本
    ENTER   -       显示输出结果
    ESC     -       关闭窗口
"""

def validate(text):
    for s in ['=', 'import', 'from', ';']:
        if s in text:
            return False
    return True

menu_def = [['Help', 'About']]
# All the stuff inside your window.
layout = [[sg.Menu(menu_def)],
          [sg.Text('公式:'), sg.InputText(key='-IN-')],
          [sg.Text('结果:'), sg.Text('', size=(15,1), key='-OUTPUT-')],
          [sg.Button('Calculate', bind_return_key=True), sg.Button('Exit')]]

# Create the Window
window = sg.Window('小型科学计算器', layout, return_keyboard_events=True)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Exit', 'Escape:27'):   # if user closes window or clicks cancel
        break
    if event == 'About':
        sg.Popup(help_text, title='帮助文件')
    if event == 'Calculate':
        try:
            inp = values['-IN-']
            if not validate(inp):
                raise SyntaxError()
            res = eval(inp)
        except (SyntaxError, NameError):
            res = 'invalid syntax'
        window['-OUTPUT-'].Update(res)
    if event == 'Delete:46':
        window['-IN-'].Update('')
        window['-OUTPUT-'].Update('')

window.close()
