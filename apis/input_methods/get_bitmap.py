
def export_bitmap_current_window():
    import win32gui
    import win32ui
    import win32con
    from PIL import Image
    import numpy
    import cv2
    import pickle
    hwnd = win32gui.GetForegroundWindow()
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()

    _left, _top, _right, _bottom = win32gui.GetWindowRect(hwnd)
    w = _right - _left
    h = _bottom - _top

    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)
    #dataBitMap.SaveBitmapFile(cDC, cur_time+".bmp") #Saves the image to a bitmap
    bmpinfo = dataBitMap.GetInfo()
    bmparray = numpy.asarray(dataBitMap.GetBitmapBits(), dtype=numpy.uint8)
    pil_im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmparray, 'raw', 'RGBX', 0, 1)
    pil_array = numpy.array(pil_im)
    cv_im = cv2.cvtColor(pil_array, cv2.COLOR_RGB2BGR)
    bitmapPickle = pickle.dumps(cv_im)
    # Free Resources, this step is required
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
    print(type(bitmapPickle))
    return bitmapPickle #Returns a pickle which we can store

def read_bitmap_image(bitmapPickle): #Takes in pickle
    from PIL import Image
    from datetime import datetime
    import pickle
    ndarray = pickle.loads(bitmapPickle)
    im = Image.fromarray(ndarray).convert('RGB')
    #cur_time = datetime.utcnow().isoformat()
    #cur_time = cur_time.replace(":", "'-'")
    #im.save("bob.bmp")
    print(type(im))
    return im #Returns image object

if __name__ == '__main__':
    #export_bitmap_current_window()
    from apscheduler.scheduler import Scheduler

    sched = Scheduler()
    sched.start()

    def some_job():
        databitmap = export_bitmap_current_window()
        read_bitmap_image(databitmap)

    sched.add_interval_job(some_job, seconds=5)
    while(True):
        pass