import ctypes
from ctypes import *
picam = ctypes.WinDLL("picam")
picam.Picam_InitializeLibrary()
cam = c_void_p(0)
picam.Picam_OpenFirstCamera(byref(cam))

# DEBUGGERS:
"""
var = pv.CAM_NAME_LEN
var2 = create_string_buffer(pv.CAM_NAME_LEN)
var3 = c_char_p(pv.CAM_NAME_LEN)
var4 = c_char(pv.CAM_NAME_LEN)
var5 = c_byte(pv.CAM_NAME_LEN)
var6 = c_ubyte(pv.CAM_NAME_LEN)
var7 = c_uint16(pv.CAM_NAME_LEN)
var8 = c_int16(pv.CAM_NAME_LEN)
placeholder = None
"""

piint = ctypes.c_int
major = piint()
minor = piint()
dist = piint()
release = piint()
picam.Picam_GetVersion(pointer(major), pointer(minor), pointer(dist), pointer(release))

'''
0
>>> major.value
3
>>> minor.value
3
>>> dist.value
1
>>> release.value
1510
'''