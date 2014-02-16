"""유틸리티 함수와 클래스 모음"""
from importlib import import_module

__all__ = ['import_string']

UNDEFINED = type('Undefined', (object,),
                 {'__repr__': lambda self: 'UNDEFINED'})()


def import_string(import_name, package=None, default=UNDEFINED):
    """지정한 경로에 있는 파이썬 모듈이나 객체를 가져온다

    .. code-block:: pycon

       >>> from urllib.request import urlopen
       >>> import_string('urllib.request:urlopen') is urlopen
       True

    :param str import_name: 불러올 모듈이나 객체. 콜론(:)이 없을 경우 모듈 경로,
                           있을 경우에는 콜론 이후를 모듈 안의 객체 이름으로 해석한다.
    :param package: 모듈이 속한 패키지 경로
    :type package: str or None
    :param default: 모듈을 찾지 못했을 경우 예외를 발생하는 대신에 돌려줄 값
    :return: 가져온 모듈 또는 객체
    :rtype: module or object
    :raises ImportError: 모듈을 찾지 못함
    :raises AttributeError: 모듈은 찾았으나 객체를 찾지 못함

    """
    try:
        module_name, object_name = import_name.split(':', 1)
    except ValueError:
        module_name = import_name
        object_name = None
    try:
        obj = import_module(module_name, package)
        if object_name is not None:
            obj = getattr(obj, object_name)
        return obj
    except (ImportError, AttributeError):
        if default is not UNDEFINED:
            return default
        raise
