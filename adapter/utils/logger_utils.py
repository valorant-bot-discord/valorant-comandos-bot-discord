import os


def get_relative_path(absolute_path, lineno):
    relative_path = os.path.relpath(absolute_path, os.getcwd()).replace("\\", "/")
    return f"{relative_path}:{lineno}"


def extract_throw_info(throw, traceback_info):
    return {
        "Type": type(throw).__name__,
        "Message": str(throw),
        "Traceback": traceback_info
    }
