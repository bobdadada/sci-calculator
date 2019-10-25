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
    CTRL + R    -       一键清除输入文本
    ENTER       -       显示输出结果
    ESC         -       关闭窗口
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
          [sg.Text('结果:'), sg.Text('', size=(40, 1), key='-OUTPUT-')],
          [sg.Multiline(tooltip='history', disabled=True, key='HISTORY')],
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
        inp = values['-IN-']
        try:
            if not validate(inp):
                raise SyntaxError('invalid input')
            res = str(eval(inp))
        except Exception as e:
            res = str(e)
        window['-OUTPUT-'].Update(res)
        window['HISTORY'].Update(inp + '  -->  ' + res + '\n', append=True, autoscroll=True)
    if event in ('Control_L:17', 'Control_R:17'):
        event, values = window.read(timeout=300)
        if event == 'r':
            window['-IN-'].Update('')
            window['-OUTPUT-'].Update('')

window.close()
