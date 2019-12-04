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
    CTRL + F    -       一键清除输入文本
    ENTER       -       显示输出结果
    ESC         -       关闭窗口
    F1          -       查看帮助
"""

_history = []
_p = -1

def validate(text):
    for s in ['=', 'import', 'from', ';']:
        if s in text:
            return False
    return True

menu_def = [['&Help', '&About']]
# All the stuff inside your window.
main_layout = [[sg.Menu(menu_def)],
          [sg.Text('公式:'), sg.InputText(key='-IN-')],
          [sg.Text('结果:'), sg.Text('', size=(40, 1), key='-OUTPUT-')],
          [sg.Multiline(tooltip='history', disabled=True, key='HISTORY'), sg.Button('Save')],
          [sg.Button('Calculate', bind_return_key=True), sg.Button('Exit')]]

# Create the Window
window = sg.Window('小型科学计算器', main_layout, return_keyboard_events=True)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == 'Up:38':
        try:
            if _p-1<0:
                continue
            window['-IN-'].Update(_history[_p-1])
        except IndexError:
            pass
        else:
            _p -= 1
    if event == 'Down:40':
        try:
            window['-IN-'].Update(_history[_p+1])
        except IndexError:
            pass
        else:
            _p += 1
    if event in (None, 'Exit', 'Escape:27'):   # if user closes window or clicks cancel
        break
    if event in ('About', 'F1:112'):
        sg.Popup(help_text, title='帮助文件')
    if event == 'Save':
        save_layout = [[sg.Text('Filename')],
                       [sg.Input(), sg.FileBrowse(file_types=(("Text Files", "*.txt"),))],
                       [sg.OK(), sg.Cancel()]]
        save_window = sg.Window('Save History', save_layout)
        event, values = save_window.read()
        save_window.close()
        if event == 'OK':
            filename = values[0]
            try:
                with open(filename, 'w', encoding='utf-8') as fp:
                    fp.write(window['HISTORY'].Get())
                sg.popup('save history to', filename)
            except:
                continue
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
        _history.append(inp)
        _p = len(_history)-1
    if event in ('Control_L:17', 'Control_R:17'):
        event, _ = window.read(timeout=500)
        if event in ('f', 'F'):
            window['-IN-'].Update('')
            window['-OUTPUT-'].Update('')

window.close()
