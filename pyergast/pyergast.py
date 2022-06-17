import requests
import pandas as pd

def get_drivers(year=None, race=None):
  """
  Queries the API to obtain the list of drivers in a pandas dataframe format.
  By default, this function returns the list of all drivers who have ever driven in F1.
  If the year parameter is specified, this function returns the list of all drivers who drove in F1 in that year.
  If the year and race parameters are specified, this function returns the list of all drivers who drove in F1 for a particular race.

  Parameters
  ----------
  year: int
    An optional parameter that specifies the year to be queried.
  race: int
    An optional parameter that specifies the round of a year to be queried.

  Returns
  -------
  pandas.DataFrame

  Index:
    RangeIndex

  Columns:
    driverId: str
    permanentNumber: int
    code: str
    url: str
    givenName: str
    familyName: str
    dateOfBirth: str
    nationality: str
  """
  if year and race:
    url = 'http://ergast.com/api/f1/{}/{}/drivers.json?limit=1000'.format(year, race)
  elif year:
    url = 'http://ergast.com/api/f1/{}/drivers.json?limit=1000'.format(year)
  else:
    url = 'http://ergast.com/api/f1/drivers.json?limit=1000'

  r = requests.get(url)

  assert r.status_code == 200, 'Cannot connect to Ergast API'
  drivers = r.json()
  results = pd.DataFrame(drivers['MRData']['DriverTable']['Drivers'])

  return results


def get_constructors(year=None, race=None):
  """
  Queries the API to obtain the list of constructors in a pandas dataframe format.
  By default, this function returns the list of all constructors who have ever driven in F1.
  If the year parameter is specified, this function returns the list of all constructors who participated F1 in that year.
  If the year and race parameters are specified, this function returns the list of all constructors for a particular race.

  Parameters
  ----------
  year: int
    An optional parameter that specifies the year to be queried.
  race: int
    An optional parameter that specifies the round of a year to be queried.

  Returns
  -------
  pandas.DataFrame

  Index:
    RangeIndex

  Columns:
    constructorId: str
    url: str
    name: str
    nationality: str
  """
  if year and race:
    url = 'http://ergast.com/api/f1/{}/{}/constructors.json?limit=1000'.format(year, race)
  elif year:
    url = 'http://ergast.com/api/f1/{}/constructors.json?limit=1000'.format(year)
  else:
    url = 'http://ergast.com/api/f1/constructors.json?limit=1000'

  r = requests.get(url)
  
  assert r.status_code == 200, 'Cannot connect to Ergast API. Check your inputs.'
  constructors = r.json()
  result = pd.DataFrame(constructors['MRData']['ConstructorTable']['Constructors'])

  return result


def get_circuits(year=None, race=None):
  """
  Queries the API to obtain the list of circuits in a pandas dataframe format.
  By default, this function returns the list of all circuits ever used in F1.
  If the year parameter is specified, this function returns the list of all circuits used in F1 in that year.
  If the year and race parameters are specified, this function returns the information of the circuit that hosted the specified race in specified year.

  Parameters
  ----------
  year: int
    An optional parameter that specifies the year to be queried.
  race: int
    An optional parameter that specifies the round of a year to be queried.

  Returns
  -------
  pandas.DataFrame
  
  Index:
    RangeIndex

  Columns:
    circuitId: str
    url: str
    circuitName: str
    Latitude: int
    Longtitude: int
    Locality: str
    Country: str
  """
  if year and race:
    url = 'http://ergast.com/api/f1/{}/{}/circuits.json?limit=1000'.format(year, race)
  elif year:
    url = 'http://ergast.com/api/f1/{}/circuits.json?limit=1000'.format(year)
  else:
    url = 'http://ergast.com/api/f1/circuits.json?limit=1000'

  r = requests.get(url)
  
  assert r.status_code == 200, 'Cannot connect to Ergast API. Check your inputs.'
  circuits = r.json()
  result = pd.DataFrame(circuits['MRData']['CircuitTable']['Circuits'])

  # Grabbing latitude, longtitude, locality and country separately
  geo = result['Location']
  latitude, longtitude, locality, country = ([] for i in range(4))
  for track in geo:
    latitude.append(track['lat'])
    longtitude.append(track['long'])
    locality.append(track['locality'])
    country.append(track['country'])
  result['Latitude'] = latitude
  result['Longtitude'] = longtitude
  result['Locality'] = locality
  result['Country'] = country
  result = result.drop('Location', axis=1)

  return result


def find_driverId(firstname, lastname):
  """
  Searches the list of all drivers to find ones that are the same or similar to that input.

  Parameters
  ----------
  firstname: str
    The first name of the driver
  lastname: str
    The last name of the driver

  Returns
  -------
  pandas.DataFrame

  Index:
    RangeIndex

  Columns:
    driverId: str
    permanentNumber: int
    code: str
    url: str
    givenName: str
    familyName: str
    dateOfBirth: str
    nationality: str
  """
  dfDrivers = get_drivers()
  result = dfDrivers[
    dfDrivers['driverId'].str.contains(firstname.lower()) | dfDrivers['driverId'].str.contains(lastname.lower())
  ]

  return result


def find_constructorid(name):
  """
  Searches the list of all constructors to find ones that are the same or similar to the input.

  Parameters
  ----------
  name: str
    The name of the constructor

  Returns
  -------
  pandas.DataFrame

  Index:
    RangeIndex

  Columns:
    constructorId: str
    url: str
    name: str
    nationality: str
  """
  dfConstructors = get_constructors()
  result = dfConstructors[
    dfConstructors['constructorId'].str.contains(name.lower())
  ]

  return result


def find_circuitid(circuit):
  """
  Searches the list of all the circuits that are similar to the input

  Parameters
  ----------
  circuit: str
    The name of the circuit. Actual circuit name, locality, or country are all accepted.

  Returns
  -------
  pandas.DataFrame

  Index:
    RangeIndex

  Columns:
    circuitId: str
    url: str
    circuitName: str
    Latitude: int
    Longtitude: int
    Locality: str
    Country: str
  """
  dfCircuits = get_circuits()
  result = dfCircuits[
    dfCircuits['circuitId'].str.lower().str.contains(circuit.lower()) |
    dfCircuits['circuitName'].str.lower().str.contains(circuit.lower()) |
    dfCircuits['Locality'].str.lower().str.contains(circuit.lower()) |
    dfCircuits['Country'].str.lower().str.contains(circuit.lower())
  ]

  return result


def get_race_result(year=None, race=None):
  """
  Queries the API to return race results in a pandas dataframe format.
  By default this method returns the most recent result

  Parameters
  ----------
  year: int
    An optional parameter that specifies the year to be queried.
  race: int
    An optional parameter that specifies the round of a year to be queried.

  Returns
  -------
  pandas.DataFrame

  Index:
    RangeIndex
  
  Columns:
    number: int
    position: int
    positionText: str
    grid: int
    points: int
    driverID: str
    driver: str
    nationality: str
    constructorID: str
    constructor: str
    laps: int
    status: str
    Time: dict
  """
  if year or race:
    assert year and race, 'You must specify both a year and a race'
    url = 'http://ergast.com/api/f1/{}/{}/results.json?limit=1000'.format(year, race)
  else:
    url = 'http://ergast.com/api/f1/current/last/results.json?limit=1000'

  r = requests.get(url)
  
  assert r.status_code == 200, 'Cannot connect to Ergast API. Check your inputs.'
  race_result = r.json()
  result_dict = race_result['MRData']['RaceTable']['Races'][0]['Results']

  # Unpack the lists of dicts in result_dict and reformat the result
  for driver in result_dict:
    driver_info = driver['Driver']
    constructor_info = driver['Constructor']
    driver['driver'] = driver_info['givenName'] + ' ' + driver_info['familyName']
    driver['driverID'] = driver_info['driverId']
    driver['nationality'] = driver_info['nationality']
    driver['constructor'] = constructor_info['name']
    driver['constructorID'] = constructor_info['constructorId']

  # Select the columns that are relevant to the race result
  cols = ['number', 'position', 'positionText', 'grid', 'points', 'driverID', 'driver',
          'nationality', 'constructorID', 'constructor', 'laps', 'status', 'Time']
  return pd.DataFrame(result_dict)[cols]


def get_qualifying_result(year=None, race=None):
  """
  Queries the API to return qualifying results in a pandas dataframe format.
  By default this method returns the most recent result

  Parameters
  ----------
  year: int
    An optional parameter that specifies the year to be queried.
  race: int
    An optional parameter that specifies the round of a year to be queried.

  Returns
  -------
  pandas.DataFrame

  Index:
    RangeIndex

  Columns:
    number: int
    position: int
    driverID: str
    driver: str
    nationality: str
    constructorID: str
    constructor: str
    Q1: str
    Q2: str
    Q3: str
  """
  if year and race:
    assert year >= 1996, 'Qualifying data only available starting from 1996'
    url = 'http://ergast.com/api/f1/{}/{}/qualifying.json?limit=1000'.format(year, race)
  else:
    url = 'http://ergast.com/api/f1/current/last/qualifying.json?limit=1000'

  r = requests.get(url)

  assert r.status_code == 200, 'Cannot connect to Ergast API. Check your inputs.'
  race_result = r.json()
  result_dict = race_result['MRData']['RaceTable']['Races'][0]['QualifyingResults']

  # Unpack the lists of dicts in result_dict and reformat the result
  for driver in result_dict:
    driver_info = driver['Driver']
    constructor_info = driver['Constructor']
    driver['driver'] = driver_info['givenName'] + ' ' + driver_info['familyName']
    driver['driverID'] = driver_info['driverId']
    driver['nationality'] = driver_info['nationality']
    driver['constructor'] = driver_info['name']
    driver['constructorID'] = driver_info['constructorId']

  # Specify the columns to be returned, taking into account chaning qualifying formats
  cols = [
    'number', 'position', 'driverID', 'driver', 'nationality', 'constructorID', 'constructor', 'Q1'
  ]
  if 'Q2' in result_dict[0].keys():
    cols.append('Q2')
  if 'Q3' in result_dict[0].keys():
    cols.append('Q3')

  return pd.DataFrame(result_dict)[cols]


def get_schedule(year=None):
  """
  Queries the API to return the schedule of a specified season. Defaults to most recent season.

  Parameters
  ----------
  year: int
    An optional parameter that specifies the year to be queried.

  Returns
  -------
  pandas.DataFrame

  Index:
    RangeIndex

  Columns:
    season: int
    round: int
    url: str
    raceName: str
    date: str
    circuitId: str
    circuitName: str
    locality: str
    country: str
  """
  if year:
    url = 'http://ergast.com/api/f1/{}.json?limit=1000'.format(year)
  else:
    url = 'http://ergast.com/api/f1/current.json?limit=1000'

  r = requests.get(url)

  assert r.status_code == 200, 'Cannot connect to Ergast API. Check your inputs.'
  schedule = r.json()['MRData']['RaceTable']['Races']

  # Unpack the lists of dicts in result_dict and reformat the result
  for race in schedule:
    circuit = race['Circuit']
    race['circuitID'] = circuit['circuitId']
    race['circuitName'] = circuit['circuitName']
    race['locality'] = circuit['Location']['locality']
    race['country'] = circuit['Location']['country']
    del race['Circuit']

  return pd.DataFrame(schedule)


def driver_standings(year=None, race=None):
  """
  Fetch the driver standings after a specific race in a specific year. Defaults to latest standings

  Parameters
  ----------
  year: int
    An optional parameter that specifies the year to be queried.
  race: int
    An optional parameter that specifies the round of a year to be queried.

  Returns
  -------
  pandas.DataFrame

  Index:
    RangeIndex

  Columns:
    position: int
    positionText: str
    points: int
    wins: int
    driverID: str
    driver: str
    nationality: str
    constructorID: str
    constructor: str
  """
  if year and race:
    url = 'http://ergast.com/api/f1/{}/{}/driverStandings.json?limit=1000'.format(year, race)
  elif year:
    url = 'http://ergast.com/api/f1/{}/driverStandings.json?limit=1000'.format(year)
  else:
    url = 'http://ergast.com/api/f1/current/driverStandings.json?limit=1000'

  r = requests.get(url)

  assert r.status_code == 200, 'Cannot connect to Ergast API. Check your inputs.'
  driver_standings = r.json()['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

  for driver in driver_standings:
    driver['driverID'] = driver['Driver']['driverId']
    driver['driver'] = driver['Driver']['givenName'] + ' ' + driver['Driver']['familyName']
    driver['nationality'] = driver['Driver']['nationality']
    driver['constructorID'] = driver['Constructors'][0]['constructorId']
    driver['constructor'] = driver['Constructors'][0]['name']
    del driver['Driver']
    del driver['Constructors']

  return pd.DataFrame(driver_standings)


def constructor_standings(year=None, race=None):
  """
  Fetch the constructor standings after a specifis race in a specific year. Defaults to latest standings

  Parameters
  ----------
  year: int
    An optional parameter that specifies the year to be queried.
  race: int
    An optional parameter that specifies the round of a year to be queried.

  Returns
  -------
  pandas.DataFrame

  Index:
    RangeIndex

  Columns:
    position: int
    positionText: str
    points: int
    wins: int
    constructorID: str
    constructor: str
    nationality: str
  """
  if year and race:
    assert year >= 1958, 'Constructor standings only available starting 1958'
    url = 'http://ergast.com/api/f1/{}/{}/constructorStandings.json?limit=1000'.format(year, race)
  elif year:
    assert year >= 1958, 'Constructor standings only available starting 1958'
    url = 'http://ergast.com/api/f1/{}/constructorStandings.json?limit=1000'.format(year)
  else:
    url = 'http://ergast.com/api/f1/current/constructorStandings.json?limit=1000'

  r = requests.get(url)

  assert r.status_code == 200, 'Cannot connect to Ergast API. Check your inputs'
  constructor_standings = r.json()['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']

  for constructor in constructor_standings:
    constructor['constructorID'] = constructor['Constructor']['constructorId']
    constructor['name'] = constructor['Constructor']['name']
    constructor['nationality'] = constructor['Constructor']['nationality']
    del constructor['Constructor']

  return pd.DataFrame(constructor_standings)


def query_driver(driverid):
  """
  Fetches the driver's historical driver standings position

  Parameters
  ----------
  driverid: str
    A string representing the driver id of the driver. Use 'find_driverid' method to obtain constructorid

  Returns
  -------
  pandas.DataFrame

  Index:
    RangeIndex

  Columns:
    season: int
    round: int
    position: int
    positionText: str
    points: int
    wins: int
    driver: str
    nationality: str
    constructorID: str
    constructor: str
  """
  url = 'http://ergast.com/api/f1/drivers/{}/driverStandings.json?limit=1000'.format(driverid)
  r = requests.get(url)

  assert r.status_code == 200, 'Cannot connect to Ergast API. Check your inputs.'
  seasons = r.json()['MRData']['StandingsTable']['StandingsLists']

  # Extracting data from json
  for season in seasons:
    for key, value in season['DriverStandings'][0].items():
      season[key] = value
    season['driver'] = season['Driver']['givenName'] + ' ' + season['Driver']['familyName']
    season['nationality'] = season['Driver']['nationality']
    season['constructorID'] = season['Constructors'][0]['constructorId']
    season['constructor'] = season['Constructors'][0]['name']
    del season['DriverStandings']
    del season['Driver']
    del season['Constructors']

  return pd.DataFrame(seasons)


def query_constructor(constructorid):
  """
  Fetches the constructor's historical constructor standings position

  Parameters
  ----------
  constructorid: str
    A string representing the constructor id of the constructor. Use 'find_constructorid' function to obtain constructorid
  
  Returns
  -------
  pandas.DataFrame

  Index:
    RangeIndex

  Columns:
    season: int
    round: int
    position: int
    positionText: str
    points: int
    wins: int
    constructorID: str
    constructor: str
    nationality: str
  """
  url = 'http://ergast.com/api/f1/constructors/{}/constructorStandings.json?limit=1000'.format(constructorid)
  r = requests.get(url)

  assert r.status_code == 200, 'Cannot connect to Ergast API. Check your inputs.'
  seasons = r.json()['MRData']['StandingsTable']['StandingsLists']

  # Extracting data from json
  for season in seasons:
    for key, value in season['ConstructorStandings'][0].items():
      season[key] = value
    season['constructorID'] = season['Constructor']['constructorId']
    season['constructor'] = season['Constructor']['name']
    season['nationality'] = season['Constructor']['nationality']
    del season['Constructor']
    del season['ConstructorStandings']

  return pd.DataFrame(seasons)
