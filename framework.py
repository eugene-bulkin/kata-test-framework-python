import re

class Test(object):
  def __init__(self):
    self.__describing = False
    self.__html = []
    self.__correct = 0
    self.__incorrect = 0
    self.__failed = []

  @property
  def describing(self):
    return self.__describing
  @describing.setter
  def describing(self, value):
    self.__describing = value

  @property
  def html(self):
    return self.__html
  @html.setter
  def html(self, value):
    self.__html = value

  @property
  def correct(self):
    return self.__correct
  @correct.setter
  def correct(self, value):
    self.__correct = value

  @property
  def incorrect(self):
    return self.__incorrect
  @incorrect.setter
  def incorrect(self, value):
    self.__incorrect = value

  @property
  def failed(self):
    return self.__failed
  @failed.setter
  def failed(self, value):
    self.__failed = value

  class describe(object):
    def __init__(self, msg):
      if Test.describing:
        raise Exception("Cannot call describe within another describe")
      self.msg = msg

    def __call__(self, fn):
      Test.describing = True
      Test.html.append(Test.logFilter('<div class="console-describe"><h6>'))
      Test.html.append(self.msg) #_message(msg)
      Test.html.append(Test.logFilter(':</h6>'))
      fn()
      Test.html.append(Test.logFilter('</div>'))
      print ''.join(Test.html)
      Test.html = []
      Test.describing = False
      if len(Test.failed) > 0:
        raise Test.failed[0]

  class it(object):
    def __init__(self, msg):
      self.msg = msg

    def __call__(self, fn):
      Test.html.append(Test.logFilter('<div class="console-it"><h6>'))
      Test.html.append(self.msg) #_message(msg)
      Test.html.append(Test.logFilter(':</h6>'))
      fn()
      Test.html.append(Test.logFilter('</div>'))

  @staticmethod
  def logFilter(msg, lf=None):
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
    if passed:
      successMsg = "Test Passed"
      if "successMsg" in options.keys() and options["successMsg"]:
        successMsg += ": " + options["successMsg"]
      print Test.html.append(Test.logFilter('<div class="console-passed">') + successMsg + \
        Test.logFilter('</div>', True))
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
          Test.html.append('%s%s%s' % (Test.logFilter("<div class='console-failed'>Test Failed: "), msg, Test.logFilter("</div>", True)))
          error = Exception(msg)
          if Test.describing:
            Test.failed.append(error)
          else:
            raise error

  @staticmethod
  def assertEquals(actual, expected, msg=None, options={}):
    #logCall('assertEquals')
    if actual != expected:
      msg = 'Expected: %s, instead got: %s' % (Test.inspect(expected), Test.inspect(actual))
      Test.expect(False, msg, options)
    else:
      if "successMsg" not in options.keys():
        options["successMsg"] = "Value == %s" % Test.inspect(expected)
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

  class expectError(object):
    def __init__(self, msg=None, options={}):
      self.msg = msg
      self.options = options
    def __call__(self, fn):
      passed = True
      try:
        fn()
      except Exception as e:
        print Test.logFilter('<b>Expected error was thrown:</b> %s' % e)
        passed = True
      else:
        passed = False
      Test.expect(passed, self.msg, self.options)
      return True

  class expectNoError(object):
    def __init__(self, msg=None, options={}):
      self.msg = msg
      self.options = options
    def __call__(self, fn):
      passed = True
      try:
        fn()
      except Exception as e:
        print Test.logFilter('<b>Unexpected error was thrown:</b> %s' % e)
        passed = False
      else:
        passed = True
      Test.expect(passed, self.msg, self.options)
      return True
Test = Test()
describe = Test.describe
it = Test.it