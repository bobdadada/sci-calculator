import PySimpleGUI as _sg

from scipy.constants import *
from numpy import *

_help_text = """
version: 0.2

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

def _validate(text):
    for s in text.split():
        if s.strip().startswith('_'):
            return False
        if s in ('eval', 'exec'):
            return False
    for s in ['=', 'import', 'from', ';']:
        if s in text:
            return False
    return True


_menu_def = [['&Help', '&About']]
# All the stuff inside your window.
_main_layout = [[_sg.Menu(_menu_def)],
          [_sg.Text('公式:'), _sg.InputText(key='-IN-')],
          [_sg.Text('结果:'), _sg.Text('', size=(40, 1), key='-OUTPUT-')],
          [_sg.Multiline(tooltip='history', disabled=True, key='HISTORY'), _sg.Button('Save')],
          [_sg.Button('Calculate', bind_return_key=True), _sg.Button('Exit')]]

# Create the Window
_window = _sg.Window('小型科学计算器', _main_layout, return_keyboard_events=True)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    _event, _values = _window.read()
    if _event == 'Up:38':
        try:
            if _p-1<0:
                continue
            _window['-IN-'].Update(_history[_p-1])
        except IndexError:
            pass
        else:
            _p -= 1
    if _event == 'Down:40':
        try:
            _window['-IN-'].Update(_history[_p+1])
        except IndexError:
            pass
        else:
            _p += 1
    if _event in (None, 'Exit', 'Escape:27'):   # if user closes window or clicks cancel
        break
    if _event in ('About', 'F1:112'):
        _sg.Popup(_help_text, title='帮助文件')
    if _event == 'Save':
        _save_layout = [[_sg.Text('Filename')],
                       [_sg.Input(), _sg.FileBrowse(file_types=(("Text Files", "*.txt"),))],
                       [_sg.OK(), _sg.Cancel()]]
        _save_window = _sg.Window('Save History', _save_layout)
        _event, _values = _save_window.read()
        _save_window.close()
        if _event == 'OK':
            _filename = _values[0]
            try:
                with open(_filename, 'w', encoding='utf-8') as fp:
                    fp.write(_window['HISTORY'].Get())
                _sg.popup('save history to', _filename)
            except:
                continue
    if _event == 'Calculate':
        _inp = _values['-IN-']
        try:
            if not _validate(_inp):
                raise SyntaxError('invalid input')
            _res = str(eval(_inp))
        except Exception as e:
            _res = str(e)
        _window['-OUTPUT-'].Update(_res)
        _window['HISTORY'].Update(_inp + '  -->  ' + _res + '\n', append=True, autoscroll=True)
        _history.append(_inp)
        _p = len(_history)-1
    if _event in ('Control_L:17', 'Control_R:17'):
        _event, _ = _window.read(timeout=500)
        if _event in ('f', 'F'):
            _window['-IN-'].Update('')
            _window['-OUTPUT-'].Update('')

_window.close()
