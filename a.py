class Bd:
  __db_id = 7

  def __init__(self, arg):
    self.arg = arg
    self.__db_id = 7
    print("Bd __init__")
    print(self.__db_id)
    print(self.arg)
    print("Bd __init__ END")
  @property
  def db_id(self):
    return self.__db_id

  @db_id.setter
  def db_id(self, arg):
    self.__db_id = arg

class Ab:
  varx = 1
  vary = 2
  __db_id = 7

  @property
  def db_id(cls):
    return __db_id

  @db_id.setter
  def db_id(cls, arg):
    __db_id = arg

'''
s = 'abc''s'
print(s)

s2 = 'abc\'s'
print(s2)
s3 = "abc's"
print(s3)

l = [1,2,3]
l2 = [4,5,6]
l3 = l + l2
print(l3)
l3.append(10)
print(l3)
l3.extend([7,8,9])
print(l3)
'''
if __name__ == '__main__':
    print("0--")
#    print( "%d" % (Ab.db_id) )
    bd = Bd(2)
    print( bd.db_id )
    print( "%d" % (bd.db_id) )
    print("1--")
else:
    print("00--")
    print(__name__)


