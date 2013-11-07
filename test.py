from framework import *

z = 3
@Test.describe("Derp")
def describe():
  @Test.it("herp")
  def it():
    x = 1
    y = 3
    Test.assertEquals(x, y)
    Test.assertEquals(y, z)

  @Test.it("blerp")
  def it():
    @Test.expectError()
    def fn():
      raise Exception('aasdf')
    @Test.expectNoError()
    def fn():
      return
      raise Exception('aasdf')