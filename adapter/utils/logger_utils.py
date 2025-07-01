def extract_throw_info(throw, traceback_info):
    return {
        "Type": type(throw).__name__,
        "Message": str(throw),
        "Traceback": traceback_info
    }
