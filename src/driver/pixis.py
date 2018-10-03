"""

Author: Fernando Ferrari

Created on: 7 jun 2018

This file consists of a Python object oriented script created to control PIXIS 1024 CCD cameras
within a Windows 7 32 bit operational system.

This file should also work with further Windows versions, as long as they are the 32 bit versions.

*IMPORTANT*:
    After installing Princeton Instruments' PVCAM SDK on Windows 7, the required 'pvcam.ini'
    file should be stored in:
        C:\\Users\\user\\AppData\\Local\\VirtualStore\\Windows
    Otherwise, copy this file into your %SYSTEMROOT% location folder (C:\\Windows by default).
    The twin backslashes must be replaced with a single one.

READING HIGHLY RECOMMENDED (PVCAM SDK User Manual):
    ftp://ftp.piacton.com/Public/Manuals/Princeton%20Instruments/PVCAM%202.7%20Software%20User%20Manual.pdf

REMINDER:
    The camera should be turned on for running the methods.

ADDITIONAL USE REQUIREMENTS:
    * PIXIS, must allocate an even number of frame buffers.
    * One must not turn off or disconnect the camera with the camera open.
    * One must not call other PVCAM parameters such as PARAM_TEMP to get the
     current temperature during data collection. Only functions or parameters
     designated as 'online' may be called.

NOTE:
    The library does not name the 2 traditional dimensions as horizontal and vertical, it does so as
    serial and parallel, because the camera could be rotated.

"""

# ### Required Python Modules:
import datetime
import os

import numpy
from ctypes import *
from driver.pvcam_h import *
from driver import pvcam_h as pv

# This one is called 'Pillow'.
from PIL import Image

# ### Required Python Modules.


class CCDPixis:
    """
    Main class with methods built to interact with the PVCAM library.

    These methods are structured in a class because most of the
    PVCAM library methods require the library itself to be loaded and
    a handle identifier to point respectively, to the library instance
    and camera, currently being used.

    All errors are returned through the self._error() call, to the
    protected _error(self) method, from this class.
    """
    def __init__(self):
        """
        The pvcam32 DLL must be loaded before doing anything else.

        In case the instructions in the *IMPORTANT* section are not,
        or poorly followed, loading the pvcam32 dll might fail,
        in which case all the methods will return errors.
        """
        self.pv = pv
        self._hcam = None
        if os.name == "nt":
            self.pvcam = WinDLL("pvcam32")
        else:
            self.raw1394 = CDLL("libraw1394.so.11", RTLD_GLOBAL)
            # self.pthread = CDLL("libpthread.so.0", RTLD_GLOBAL) # python already loads libpthread
            # TODO: shall we use  ctypes.util.find_library("pvcam")?
            CDLL("libpvcam.so", RTLD_GLOBAL)

        self.pvcam.pl_pvcam_init()

        self._error()

    """
    NOTE:
    The methods: scan up to open; get data from the pvcam.ini file.
    That's why they don't depend on an open camera to work properly.
    Although open does require the camera to be connected to the system,
    for obvious reasons.
    """

    def scan(self):

        cams_total = c_int16()
        self.pvcam.pl_cam_get_total(byref(cams_total))

        if not self._error():
            print(cams_total.value)
            return cams_total.value

    # This method gets the device name pointed on pvcam.ini
    def name(self):

        cam_name = create_string_buffer(CAM_NAME_LEN)
        cam_id = self.pvcam.pl_cam_get_name(0, cam_name)

        if not self._error():
            print(cam_id)
            print(cam_name.value.decode())
            return cam_id, cam_name.value.decode()

    def version(self):

        raw = c_uint16()
        self.pvcam.pl_pvcam_get_ver(byref(raw))
        ver = []
        ver.insert(0, raw.value & 0x0f)  # lowest 4 bits = trivial version
        raw.value >>= 4
        ver.insert(0, raw.value & 0x0f)  # next 4 bits = minor version
        raw.value >>= 4
        ver.insert(0, raw.value & 0xff)  # highest 8 bits = major version

        if not self._error():
            return '.'.join(str(x) for x in ver)

    def ddi_version(self):

        raw = c_uint16()
        self.pvcam.pl_ddi_get_ver(byref(raw))
        ver = []
        ver.insert(0, raw.value & 0x0f)  # lowest 4 bits = trivial version
        raw.value >>= 4
        ver.insert(0, raw.value & 0x0f)  # next 4 bits = minor version
        raw.value >>= 4
        ver.insert(0, raw.value & 0xff)  # highest 8 bits = major version

        if not self._error():
            return '.'.join(str(x) for x in ver)

    def open(self):

        cam_name = create_string_buffer(CAM_NAME_LEN)
        self.pvcam.pl_cam_get_name(0, cam_name)
        if self._error():
            return

        cam_name = c_char_p(cam_name.value)
        self._hcam = c_int16()
        self.pvcam.pl_cam_open(cam_name, byref(self._hcam), OPEN_EXCLUSIVE)

        if not self._error():
            print(self._hcam.value)

    """
    The type_to_ctype dictionary stores the PVCAM library's own C language attribute
    types, used by the get_param method to search for the type of the requested parameter.
    """
    type_to_ctype = {
        # Line structure: "pv.TYPE...: c_...,  # Python integer (int) equal."
        TYPE_INT8: c_int8,  # 12
        TYPE_INT16: c_int16,  # 1
        TYPE_INT32: c_int32,  # 2
        TYPE_UNS8: c_uint8,  # 5
        TYPE_UNS16: c_uint16,  # 6
        TYPE_UNS32: c_uint32,  # 7
        TYPE_UNS64: c_uint64,  # 8
        TYPE_FLT64: c_double,  # 4
        TYPE_BOOLEAN: c_byte,  # 11
        TYPE_ENUM: c_uint32,  # 9
    }

    def get_param(self, req_param):
        """
        This method obtains five properties from the given parameter, these are:

            Access: This is the capability of changing the given parameter's value.
            An error is returned upon an attempt to assign a different value
            to a parameter without writing permissions.

            Value: This is the current value assigned to the given parameter.
            It might be changeable with the set_param method.

            Default: This is the default value of the given parameter.

            Minimum: This is the minimum value for the given parameter that the
            camera can work with.
            An attempt to assign an inferior value returns an error.

            Maximum: This is the maximum value for the given parameter that the
            camera can work with.

        This method should be called into a variable, so that its details can be
        revealed with the param_info method, unless CCDPixis.param_info(get_param(PARAMETER))
        is called in any manner.

        NOTE:
        All of the PVCAM library parameters return to default after library is closed.
        The library is closed alongside the program.

        :param req_param: Parameter to be obtained
        :return: Stops the method if an error code different from 0 is obtained within
        the PVCAM library
        :returns the requested parameter's properties, as cited above.
        """

        ret = []

        type_catcher = c_int32()
        self.pvcam.pl_get_param(self._hcam, req_param, ATTR_ACCESS, byref(type_catcher))
        if self._error():
            return
        if type_catcher.value == ACC_READ_WRITE:
            ret.append(1)
        elif type_catcher.value == ACC_READ_ONLY:
            ret.append(2)
        elif type_catcher.value == ACC_WRITE_ONLY:
            ret.append(3)
        else:
            ret.append(0)

        # This method must search for parameter type in order to return its proper value.
        type_catcher = c_uint32()
        self.pvcam.pl_get_param(self._hcam, req_param, ATTR_TYPE, byref(type_catcher))
        if self._error():
            return
        if type_catcher.value == TYPE_CHAR_PTR:
            # A string, must obtain its length.
            count = c_uint32()
            self.pvcam.pl_get_param(self._hcam, req_param, ATTR_COUNT, byref(count))
            content = create_string_buffer(count.value)
        elif type_catcher.value in self.type_to_ctype:
            content = self.type_to_ctype[type_catcher.value]()
        elif type_catcher.value in (TYPE_VOID_PTR, TYPE_VOID_PTR_PTR):
            print("Cannot handle arguments of type pointer")
            return
        else:
            print("Argument of unknown type %d" % type_catcher.value)
            return

        self.pvcam.pl_get_param(self._hcam, req_param, ATTR_CURRENT, byref(content))
        if self._error():
            return
        ret.append(content.value)

        self.pvcam.pl_get_param(self._hcam, req_param, ATTR_DEFAULT, byref(content))
        if self._error():
            return
        ret.append(content.value)

        self.pvcam.pl_get_param(self._hcam, req_param, ATTR_MIN, byref(content))
        if self._error():
            return
        ret.append(content.value)

        self.pvcam.pl_get_param(self._hcam, req_param, ATTR_MAX, byref(content))
        if self._error():
            return
        ret.append(content.value)

        return ret

    @staticmethod
    def param_info(param_list):
        """
        This method reveals the parameter values obtained with the get_param method.
        :param param_list: A list with the requested parameter's values to be revealed.
        :return:
        """
        if param_list is None:
            print("No Parameter!")
            return
        if param_list[0] == ACC_READ_WRITE:
            print("Access: Able to Read and Write.")
        elif param_list[0] == ACC_READ_ONLY:
            print("Access: Able to Read Only.")
        elif param_list[0] == ACC_WRITE_ONLY:
            print("Access: Able to Write Only.")
        else:
            print("Unknown Access")
        print("Value: " + str(param_list[1]))
        print("Default: " + str(param_list[2]))
        print("Minimum: " + str(param_list[3]))
        print("Maximum: " + str(param_list[4]))

    def set_param(self, req_param, value):
        """
        This method sets the given parameter's value to the given value.

        NOTE:
        All of the PVCAM library parameters return to default after library is closed.
        The library is closed alongside the program.

        Usage example:
            To set the exposure resolution in nanoseconds, milliseconds or seconds,
            (the best choice is usually in milliseconds) for life imaging (NOTE: using
            nanoseconds allows setting up to a limit of 71min):
                self.set_param(pv.PARAM_EXP_RES_INDEX, pv.EXP_RES_ONE_MILLISEC)

        :param req_param: Parameter to be set.
        :param value: Value to set parameter to.
        :return: Stops the method if an error code different from 0 is obtained within
        the PVCAM library.
        """

        content = c_int32(value)
        self.pvcam.pl_set_param(self._hcam, req_param, byref(content))
        if not self._error():
            print(str(req_param) + "'s Value Set To: " + str(value))

    def enum_available(self, enum_param):
        """
        This method gets all the available values for a given enumerated parameter.
        @:param enum_param (int): The given parameter ID (PARAM_*), it must be an
        enumerated parameter, that is, it must contain the enum C type.
        @:return (dict (int -> string)): value to description
        """
        count = c_uint32()
        self.pvcam.pl_get_param(self._hcam, enum_param, ATTR_COUNT, byref(count))
        if self._error():
            return

        ret = {}  # int -> str
        for i in range(count.value):
            length = c_uint32()
            content = c_uint32()
            self.pvcam.pl_enum_str_length(self._hcam, enum_param, i, byref(length))
            if self._error():
                return
            desc = create_string_buffer(length.value)
            self.pvcam.pl_get_enum_param(self._hcam, enum_param, i, byref(content),
                                         desc, length)
            if self._error():
                return
            ret[content.value] = desc.value

        if not self._error():
            return ret

    def take_picture(self, b, exp, path):
        """
        This method takes a picture* and saves it in a .tif format with a given name to a given
        directory.

        *: There are procedure instructions the Defining Exposures section on page 70 of the
        PVCAM SDK User Manual.

        :return: Stops the method if an error code different from 0 is obtained within
        the PVCAM library.
        """

        # ############################################## STEP 1 ###################################################

        # prepare image (region)
        region = rgn_type()
        # region is 0 indexed
        width = c_uint16()
        height = c_uint16()
        self.pvcam.pl_get_param(self._hcam, PARAM_SER_SIZE, ATTR_DEFAULT, byref(width))
        self.pvcam.pl_get_param(self._hcam, PARAM_PAR_SIZE, ATTR_DEFAULT, byref(height))
        # SER == Serial
        # PAR == Parallel
        region.s1, region.s2, region.p1, region.p2 = (0, width.value - 1, 0, height.value - 1)
        binning = b
        region.sbin, region.pbin = (binning, binning)

        if self._error():
            return

        # ############################################## STEP 2.1 ###################################################

        buffer_length = c_uint32()
        exp_ms = exp * 1e3  # ms (1.0 == s)
        self.pvcam.pl_exp_init_seq()
        self.pvcam.pl_exp_setup_seq(self._hcam, 1, 1, byref(region), TIMED_MODE, exp_ms, byref(buffer_length))
        # empty c_ushort_Array_1048576
        frame_buffer = (c_uint16 * buffer_length.value)()
        if self._error():
            return

        # ############################################## STEP 2.2 ###################################################

        self.pvcam.pl_exp_start_seq(self._hcam, frame_buffer)
        status = c_int16()
        byte_cnt = c_uint32()  # number of bytes already acquired: unused
        self.pvcam.pl_exp_check_status(self._hcam, byref(status), byref(byte_cnt))

        # ############################################## STEP 2.3 #################################################

        while status.value != READOUT_COMPLETE and status.value != READOUT_FAILED:
            self.pvcam.pl_exp_check_status(self._hcam, byref(status), byref(byte_cnt))

        if status.value == READOUT_FAILED:
            self.pvcam.pl_exp_abort(self._hcam, CCS_CLEAR)
            self._error()
            return

        # ############################################## STEP 3 ####################################################

        # frame_buffer holds the images obtained (apparently)
        self.pvcam.pl_exp_finish_seq(self._hcam, frame_buffer, None)
        self.pvcam.pl_exp_uninit_seq()

        p = cast(frame_buffer, POINTER(c_uint16))
        ndbuffer = numpy.ctypeslib.as_array(p, (height.value // binning, width.value // binning))  # numpy shape is H, W
        print(ndbuffer)
        now = datetime.datetime.now()
        name = now.strftime("%Y-%m-%d_%H:%M:%S")
        im3 = Image.fromarray(ndbuffer)
        im3.save(path + name + ".tif")

        """
        tiff_to_save = TIFFimage(obj)

        tiff_to_save.write_file(r"C:\\Users\\user\Pictures\testes_pixis\a")
        """

        self._error()

    def close(self):
        print("Closing Camera...")

        self.pvcam.pl_cam_close(self._hcam)

        self._error()

    def _error(self):
        """
        This method gets the latest error code, message and meaning, from the last attempted method.
        It also works even before the library is initialized, which is when:
        self.pvcam.pl_pvcam_init() is called.

        The library must obviously be open for this to work, which is why it's so reliable and
        called in every other method. For instructions on such, the *IMPORTANT* section
        should be read.

        :returns: True in case an error occurred and False otherwise.
        These values are used to discontinue the execution of methods that no longer
        need to be running in an error event.
        """
        if self.pvcam.pl_error_code():
            print("Error Code: " + str(self.pvcam.pl_error_code()))
            err_mes = create_string_buffer(ERROR_MSG_LEN)
            self.pvcam.pl_error_message(self.pvcam.pl_error_code(), err_mes)
            print("Error: " + err_mes.value.decode())
            return True
        else:
            return False
