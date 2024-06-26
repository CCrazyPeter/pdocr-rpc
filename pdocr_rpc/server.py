#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: Apache Software License
from os import makedirs
from os.path import join, dirname, abspath, exists
from socketserver import ThreadingMixIn
from time import time
from typing import TYPE_CHECKING
from xmlrpc.server import SimpleXMLRPCServer

from pdocr_rpc.conf import setting

if not TYPE_CHECKING:
    from paddleocr import PaddleOCR


class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass


CURRENT_DIR = dirname(abspath(__file__))


def check_connected():
    return True


def image_put(data):
    pic_dir = join(CURRENT_DIR, "pic")
    if not exists(pic_dir):
        makedirs(pic_dir)

    pic_path = join(pic_dir, f"pic_{time()}.png")
    handle = open(pic_path, "wb")
    handle.write(data.data)
    handle.close()
    return pic_path


def paddle_ocr(pic_path, lang):
    """
     Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
     例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
    :param file_name:
    :param lang:
    :return:
    """
    ocr = PaddleOCR(use_angle_cls=True, lang=lang, ocr_version="PP-OCRv4")
    result = ocr.ocr(pic_path, cls=True)
    return result


def server():
    server = ThreadXMLRPCServer(("0.0.0.0", setting.PORT), allow_none=True)
    server.register_function(check_connected, "check_connected")
    server.register_function(image_put, "image_put")
    server.register_function(paddle_ocr, "paddle_ocr")
    print("Listen to client requests ...")
    print(f"Client request: IP:{setting.PORT}")
    server.serve_forever()


if __name__ == "__main__":
    server()
