from pyergast import __version__
from pyergast import pyergast

def test_version():
  assert __version__ == '0.1.0'


def test_get_drivers():
  expected_drivers = 21
  actual_drivers = pyergast.get_drivers(2021)['driverId'].count()
  assert actual_drivers == expected_drivers, 'Should be true (21 drivers)'


def test_get_constructors():
  expected_constructors = 10
  actual_constructors = pyergast.get_constructors(2021)['constructorId'].count()
  assert actual_constructors == expected_constructors, 'Should be true (10 constructors)'

