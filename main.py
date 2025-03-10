import pywintypes
import win32api
import win32con
import pystray
from PIL import Image

i = 0
res = set()
try:
    while True:
        ds = win32api.EnumDisplaySettings(None, i)
        res.add(f"{ds.PelsWidth}⨯{ds.PelsHeight}")
        i += 1
except:
    pass

sorted_res = sorted(res, key=lambda x: (int(x.split('⨯')[0]), int(x.split('⨯')[1])))

def get_current_resolution():
    ds = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)
    return f"{ds.PelsWidth}⨯{ds.PelsHeight}"

current_resolution = get_current_resolution()

def exit_action(icon, item):
    print('Exiting...')
    icon.stop()

def change_resolution(icon, item):
    global current_resolution
    selected_resolution = str(item)
    print(f"Selected resolution: {selected_resolution}")
    icon.menu = update_menu(current_resolution, checked=False, enabled=True)
    
    current_resolution = selected_resolution
    devmode = pywintypes.DEVMODEType()
    width, height = selected_resolution.split('⨯')
    width = int(width)
    height = int(height)
    devmode.PelsWidth = width
    devmode.PelsHeight = height
    devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT
    win32api.ChangeDisplaySettings(devmode, 0)

    icon.menu = update_menu(selected_resolution, checked=True, enabled=False)

def update_menu(selected_resolution, checked, enabled):
    menu_items = []
    for resolution in sorted_res:
        menu_items.append(pystray.MenuItem(resolution, change_resolution, checked=lambda item, res=resolution: res == selected_resolution, enabled=enabled if resolution == selected_resolution else True))
    menu_items.append(pystray.Menu.SEPARATOR)
    menu_items.append(pystray.MenuItem('Exit', exit_action))
    return pystray.Menu(*menu_items)

tray_image = Image.open(r"icon.jpg")
icon = pystray.Icon("resolution_changer", tray_image, menu=update_menu(current_resolution, checked=True, enabled=False))
icon.run()
