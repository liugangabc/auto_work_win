# coding=utf-8

from IPython.display import Image
import time
from PIL import ImageGrab
import aircv as ac
# pip install opencv-python
# pip install aircv

from pymouse import PyMouse
# pip install pymouse pyHook
from pykeyboard import PyKeyboard


# pip install PyUserInput


def matchImg(imgobj, imgsrc="", confidence=0.5):
    # imgobj 目标图像路径，imgsrc 基础图片路径, confidence 0.5 找到中间位置
    imsrc = ac.imread(imgsrc)
    imobj = ac.imread(imgobj)

    match_result = ac.find_template(imsrc, imobj, confidence)
    if match_result is not None:
        return match_result
    return None


def desktop_find(target):
    desktop = ImageGrab.grab()
    desktop.save('now.png')
    result = matchImg(target, imgsrc='now.png')
    if result:
        return True, result["result"]
    else:
        return False, [0, 0]


class Operation(object):
    pass


class LeftOperation(Operation):
    def __init__(self, target, count=1, interval=1):
        self.target = target
        self.count = count
        self.interval = interval

    def run(self, pymouse=None):
        if not isinstance(pymouse, PyMouse):
            pymouse = PyMouse()
        is_find, position = desktop_find(self.target)
        assert is_find
        x, y = position
        for i in xrange(self.count):
            # pymouse.move(x, y)
            pymouse.click(x, y, 1)
            time.sleep(self.interval)


class RightOperation(Operation):
    def __init__(self, target, count=1, interval=1):
        self.target = target
        self.count = count
        self.interval = interval

    def run(self, pymouse=None):
        if not isinstance(pymouse, PyMouse):
            pymouse = PyMouse()
        is_find, position = desktop_find(self.target)
        assert is_find
        x, y = position
        for i in xrange(self.count):
            # pymouse.move(x, y)
            pymouse.click(x, y, 2)
            time.sleep(self.interval)


class InputOperation(Operation):
    def __init__(self, target, input, count=1, interval=1):
        self.target = target
        self.count = count
        self.interval = interval
        self.input = input

    def run(self, pymouse=None):
        if not isinstance(pymouse, PyMouse):
            pymouse = PyMouse()
        is_find, position = desktop_find(self.target)
        assert is_find
        keyboard = PyKeyboard()
        x, y = position
        pymouse.click(x, y, 1)
        for i in xrange(self.count):
            time.sleep(self.interval)
            keyboard.type_string(self.input)


class Check(object):
    def __init__(self, flag, count=10, opera_wait=1):
        self.flag = flag
        self.count = count
        self.opera_wait = opera_wait

    def run(self):
        for i in xrange(self.count):
            time.sleep(self.opera_wait)
            is_find, position = desktop_find(self.flag)
            if is_find:
                return True
        return False


class Step(object):
    def __init__(self, opera, verify=None):
        self.opera = opera
        self.verify = verify

    def run(self):
        try:
            self.opera.run()
            print "opera success"
        except Exception as e:
            print "opera faild"
            raise e
        if self.verify:
            try:
                self.verify.run()
                print "verify success"
            except Exception as e:
                print "verify faild"
                raise e


class Workflow(object):
    def __init__(self):
        self.steps = []

    def add(self, step):
        if not isinstance(step, Step):
            raise ValueError
        self.steps.append(step)

    def run(self):
        for step in self.steps:
            step.run()


OPERA = {
    "LeftOperation": LeftOperation,
    "RightOperation": RightOperation,
    "InputOperation": InputOperation,
}


def workflow_list(data):
    out = []
    for w in data:
        workflow_obj = Workflow()

        for s in w["steps"]:
            opera = OPERA.get(s["operation"]["type"])
            o = opera(*s["operation"]["data"])
            step_data = {"opera": o}
            if s["verify"]["enable"]:
                step_data["verify"] = Check(*s["verify"]["data"])

            s = Step(**step_data)
            workflow_obj.add(s)

        out.append(workflow_obj)
    return out


# test 

data = [
    {
        "name": "test",
        "start": 1,
        "steps": [
            {
                "name": "setp_1",
                "operation": {
                    "type": "LeftOperation",
                    "data": {
                        "target": "./a.png",
                        "count": 2,
                        "interval": 0.5
                    }
                },
                "verify": {
                    "enable": True,
                    "data": {
                        "flag": "./a_verify.png",
                        "opera_wait": 1,
                        "count": 10
                    }
                }
            },
            {
                "name": "setp_2",
                "operation": {
                    "type": "InputOperation",
                    "data": {
                        "target": "./b.png",
                        "input": "liugang@chinac.com",
                        "count": 1,
                        "interval": 0.5
                    }
                },
                "verify": {
                    "enable": False,
                    "data": {
                        "flag": "./d_verify.png",
                        "opera_wait": 1,
                        "count": 10
                    }
                }
            },
            {
                "name": "setp_3",
                "operation": {
                    "type": "InputOperation",
                    "data": {
                        "target": "./c.png",
                        "input": "Passw0rd!2",
                        "count": 1,
                        "interval": 0.5
                    }
                },
                "verify": {
                    "enable": False,
                    "data": {
                        "flag": "./d_verify.png",
                        "opera_wait": 1,
                        "count": 10
                    }
                }
            },
            {
                "name": "setp_4",
                "operation": {
                    "type": "LeftOperation",
                    "data": {
                        "target": "./d.png",
                        "count": 2,
                        "interval": 0.5
                    }
                },
                "verify": {
                    "enable": True,
                    "data": {
                        "flag": "./d_verify.png",
                        "opera_wait": 1,
                        "count": 10
                    }
                }
            },
        ]
    }
]

# bbb = workflow_list(data)

step_data = {
    "name": "setp_1",
    "operation": {
        "type": "LeftOperation",
        "data": {
            "target": "./img/a.png",
            "count": 2,
            "interval": 0.1
        }
    },
    "verify": {
        "enable": True,
        "data": {
            "flag": "./img/ioa.png",
            "opera_wait": 1,
            "count": 10
        }
    }
}

# step_data = {
#     "name": "setp_2",
#     "operation": {
#         "type": "InputOperation",
#         "data": {
#             "target": "./img/ioa.png",
#             "input": "liugang@chinac.com",
#             "count": 1,
#             "interval": 0.5
#         }
#     },
#     "verify": {
#         "enable": True,
#         "data": {
#             "flag": "./img/ioa_verify.png",
#             "opera_wait": 1,
#             "count": 10
#         }
#     }
# }

# step_data = {
#     "name": "setp_3",
#     "operation": {
#         "type": "InputOperation",
#         "data": {
#             "target": "./img/c.png",
#             "input": "Passw0rd!2",
#             "count": 1,
#             "interval": 0.5
#         }
#     },
#     "verify": {
#         "enable": False,
#         "data": {
#             "flag": "./img/d_verify.png",
#             "opera_wait": 1,
#             "count": 10
#         }
#     }
# }

# step_data = {
#     "name": "setp_4",
#     "operation": {
#         "type": "LeftOperation",
#         "data": {
#             "target": "./img/d.png",
#             "count": 1,
#             "interval": 0.5
#         }
#     },
#     "verify": {
#         "enable": False,
#         "data": {
#             "flag": "./img/d_verify.png",
#             "opera_wait": 1,
#             "count": 10
#         }
#     }
# }


def step_fctory(data):
    opera = OPERA.get(data["operation"]["type"])
    o = opera(**data["operation"]["data"])
    step_data = {"opera": o}
    if data["verify"]["enable"]:
        step_data["verify"] = Check(**data["verify"]["data"])
    return Step(**step_data)


step_fctory(step_data).run()
