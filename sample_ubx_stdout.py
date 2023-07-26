from time import sleep

latitude = 60.0
longitude = 28.0
monoTime = 10.0

while True:
    print \
    ('{{"latitude": {}, "longitude": {}, "altitude": 4.3679, "monotonicTime": {}, "accuracy": 0.14100000000000001, "verticalAccuracy": 0.179}}'. \
     format(str(latitude), str(longitude), str(monoTime)))
    sleep(1)
    latitude += 0.01
    longitude -= 0.01
    monoTime += 1
