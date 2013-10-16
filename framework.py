import re
import inspect
import sys

class Test(object):
    # properties
    def __init__(self):
        self.__describing = False
        self.__html = []
        self.__allowed = ["describe", "it", "expect"]
        self.__correct = 0
        self.__incorrect = 0
        self.__failed = []

    def __checkAllowed(self, stack):
        if "_Test__allowed" in stack[1][0].f_locals:
            return True
        caller = str(stack[1][0].f_locals["self"].__class__).split(".")[1]
        return caller in self.__allowed

    @property
    def describing(self):
        if self.__checkAllowed(inspect.stack()):
            return self.__describing
    @describing.setter
    def describing(self, value):
        if self.__checkAllowed(inspect.stack()):
            self.__describing = value

    @property
    def html(self):
        if self.__checkAllowed(inspect.stack()):
            return self.__html
    @html.setter
    def html(self, value):
        if self.__checkAllowed(inspect.stack()):
            self.__html = value

    @property
    def correct(self):
        if self.__checkAllowed(inspect.stack()):
            return self.__correct
    @correct.setter
    def correct(self, value):
        if self.__checkAllowed(inspect.stack()):
            self.__correct = value

    @property
    def incorrect(self):
        if self.__checkAllowed(inspect.stack()):
            return self.__incorrect
    @incorrect.setter
    def incorrect(self, value):
        if self.__checkAllowed(inspect.stack()):
            self.__incorrect = value

    @property
    def failed(self):
        if self.__checkAllowed(inspect.stack()):
            return self.__failed
    @failed.setter
    def failed(self, value):
        if self.__checkAllowed(inspect.stack()):
            self.__failed = value

    @staticmethod
    def logFilter(msg, lf=None):
        if not Test._Test__checkAllowed(inspect.stack()):
            return

        m = re.sub('/<[^>].*>/g', '', msg)
        if len(m) == 0 and not lf:
            return ""
        else:
            return m + "\n"

    @staticmethod
    def inspect(obj):
        #logCall('inspect')
        return obj

    @staticmethod
    def expect(passed, msg=None, options={}):
        __allowed = "expect"
        if passed:
            successMsg = "Test Passed"
            if "successMsg" in options.keys() and options["successMsg"]:
                successMsg += ": " + options["successMsg"]
            print Test.logFilter('<div class="console-passed">') + successMsg + \
                  Test.logFilter('</div>', True)
            Test.correct += 1
        else:
            # if _message(msg):
            #     msg = _message(msg)
            # else:
            #     msg = "Invalid"
            if "extraCredit" in options.keys() and options["extraCredit"]:
                if options["extraCredit"] != True:
                    msg = options["extraCredit"]
                else:
                    msg = ""
                msg = ": ".join(filter(lambda s: s is not '', ["Test Missed:", msg]))
            else:
                print Test.logFilter("<div class='console-failed'>Test Failed: ") + msg + \
                      Test.logFilter("</div>", True)
                error = Exception(msg)
                if Test.describing:
                    Test.failed.append(error)
                else:
                    raise error

    @staticmethod
    def assertEquals(actual, expected, msg=None, options={}):
        #logCall('assertEquals')
        if actual != expected:
            msg = 'Expected: ' + Test.inspect(expected) + ', instead got: ' + Test.inspect(actual)
            Test.expect(False, msg, options)
        else:
            if "successMsg" not in options.keys():
                options["successMsg"] = "Value == " + Test.inspect(expected)
            Test.expect(True, None, options)

    @staticmethod
    def assertNotEquals(actual, expected, msg=None, options={}):
        #logCall('assertEquals')
        if actual == expected:
            msg = 'Not Expected: ' + Test.inspect(expected)
            Test.expect(False, msg, options)
        else:
            if "successMsg" not in options.keys():
                options["successMsg"] = "Value != " + Test.inspect(expected)
            Test.expect(True, None, options)

    class describe:
        def __init__(self, msg):
            self.msg = msg
        def __enter__(self):
            if Test.describing:
                raise Exception("Cannot call describe within another describe")
            #logCall("describe")
            Test.describing = True
            Test.html.append(Test.logFilter('<div class="console-describe"><h6>'))
            Test.html.append(self.msg) #_message(msg)
            Test.html.append(Test.logFilter(':</h6>'))

        def __exit__(self, text, value, callback):
            Test.html.append(Test.logFilter('</div>'))
            print ''.join(Test.html)
            Test.html = []
            Test.describing = False
            if len(Test.failed) > 0:
                raise Test.failed[0]

    class it:
        def __init__(self, msg):
            self.msg = msg
        def __enter__(self):
            #logCall('it')
            Test.html.append(Test.logFilter('<div class="console-it"><h6>'))
            Test.html.append(self.msg) #_message(msg)
            Test.html.append(Test.logFilter(':</h6>'))
            # TODO: handle callbacks
        def __exit__(self, text, value, callback):
            Test.html.append(Test.logFilter('</div>'))

    class expectError:
        def __init__(self, msg=None, options={}):
            self.msg = msg
            self.options = options
        def __enter__(self):
            pass
        def __exit__(self, text, value, callback):
            if text is not None: # error thrown
                print Test.logFilter('<b>Expected error was thrown:</b> ' + value.message)
                passed = True
            else:
                passed = False
            Test.expect(passed, self.msg, self.options)
            return True

    class expectNoError:
        def __init__(self, msg=None, options={}):
            self.msg = msg
            self.options = options
        def __enter__(self):
            pass
        def __exit__(self, text, value, callback):
            if text is not None: # error thrown
                print Test.logFilter('<b>Expected error was thrown:</b> ' + value.message)
                passed = True
            else:
                passed = False
            Test.expect(passed, self.msg, self.options)
            return True
Test = Test()