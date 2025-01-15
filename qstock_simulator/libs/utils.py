from PyQt6.QtCore import QThread, pyqtSignal

class FunctionThread(QThread):

    sigFunctionFinished = pyqtSignal()
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.func(*self.args, **self.kwargs)
        self.sigFunctionFinished.emit()

def run_in_thread(func, *args, **kwargs):
    thread = FunctionThread(func, *args, **kwargs)
    thread.start()
    return thread