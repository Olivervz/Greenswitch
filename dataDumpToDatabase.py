DEBUG = True

import json

def removeYearlyAverage(windSpeedAveragesDict):
  monthlyWindSpeedAverage = dict(windSpeedAveragesDict)
  del monthlyWindSpeedAverage['13']
  return monthlyWindSpeedAverage

def readJsonDump(fileName):
  with open(fileName + '.json') as json_file:
    return json.load(json_file)

def convertDumpToDatabase(JsonDump, measurement):
  database = {}
  minimum = 1000000.00
  minimumLocation = ""
  maximum = 0.00
  maximumLocation = ""

  for entry in JsonDump['features']:

    if entry['properties']['parameter'][measurement]['13'] < minimum:
      minimum = entry['properties']['parameter'][measurement]['13']
      minimumLocation = str(entry['geometry']['coordinates'][0]) + "," + str(entry['geometry']['coordinates'][1])

    if entry['properties']['parameter'][measurement]['13'] > maximum:
      maximum = entry['properties']['parameter'][measurement]['13']
      maximumLocation = str(entry['geometry']['coordinates'][0]) + "," + str(entry['geometry']['coordinates'][1])

    database[str(entry['geometry']['coordinates'][0]) + "," + str(entry['geometry']['coordinates'][1])] = \
      {'completeAverage': entry['properties']['parameter'][measurement]['13'],
        'months': removeYearlyAverage(entry['properties']['parameter'][measurement])
      }

  database['minimum'] = {}
  database['minimum']['value'] = minimum
  database['minimum']['location'] = minimumLocation

  database['maximum'] = {}
  database['maximum']['value'] = maximum
  database['maximum']['location'] = maximumLocation
  return database

def writeDatabaseToJsonFile(database, fileName):
  with open(fileName + '.json', 'w', encoding='utf-8') as file:
    json.dump(database, file, ensure_ascii=False, indent=4)



if DEBUG:
  print ("Starting to read JSON...")
windSpeedDump = readJsonDump("windSpeed")
solarIrradianceDump = readJsonDump("solarIrradiance")
windDirectionDump = readJsonDump("windDirection")
if DEBUG:
  print ("Finished reading JSON...\n")



if DEBUG:
  print ("Converting JSON dump to database...")
windSpeedDatabase = convertDumpToDatabase(windSpeedDump, 'WS50M')
solarIrradianceDatabase = convertDumpToDatabase(solarIrradianceDump, 'ALLSKY_SFC_LW_DWN')
windDirectionDatabase = convertDumpToDatabase(windDirectionDump, 'WD50M')
if DEBUG:
  print ("Finished creating database...\n")



if DEBUG:
  print ("Writing databases to files...")
writeDatabaseToJsonFile(windSpeedDatabase, "windSpeedDatabase")
writeDatabaseToJsonFile(solarIrradianceDatabase, "solarIrradianceDatabase")
writeDatabaseToJsonFile(windDirectionDatabase, "windDirectionDatabase")
if DEBUG:
  print ("Finished writing database to files...\n")