import functools
import traceback

import asyncio


class JsonException (Exception):
    pass

class CocObject (object):
    def __init__ (self, data: dict):
        self.data = data

        for key, value in self.data.items():
            if isinstance(value, (list, tuple)):
                setattr(self, key, [CocObject(v) if isinstance(v, dict) else v for v in value])
            else:
                setattr(self, key, CocObject(value) if isinstance(value, dict) else value)

def requestmethod (method):
    if asyncio.iscoroutinefunction(method):
        @functools.wraps(method)
        async def error_handler (*args, **kwargs):
            try:
                print(args, kwargs)
                return await method(*args, **kwargs)
            except Exception as exception:
                print(''.join(traceback.format_exception(type(exception), exception, exception.__traceback__)))
                return None
        return error_handler
    else:
        def error_handler (*args, **kwargs):
            try:
                print(args, kwargs)
                return method(*args, **kwargs)
            except Exception as exception:
                print(''.join(traceback.format_exception(type(exception), exception, exception.__traceback__)))
                return None
        return error_handler

def handle_coc_json_errors (json_content: dict):
    if 'status' not in json_content.keys():
        if 'error' in json_content.keys():
            raise JsonException(f'An error occurred!\n\n{json_content}')
        else:
            raise JsonException(f'An error occurred! An expected JSON key was not found in request response')
