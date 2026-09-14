import os

def FileHander(filePath):
    print(filePath)
    sampleRate = SampleRate(filePath)
    fileName = FileName(filePath)



    return sampleRate, fileName

def SampleRate(filePath):
    with open(filePath, "r") as file:
            for line in file:
                if "Sample Rate" in line:
                    print(line)
                    items = line.split(",")
    
                    for position, item in enumerate(items):
                        item = item.replace("\"", "")
                        item = item.replace(" ", "")
                        item = item.lower()
    
                        items[position] = item
    
                    if "samplerate" in items:
                        sampleRatePosition = items.index("samplerate")
                        sampleRate = items[sampleRatePosition + 1]
                    else:
                        sampleRate = "N/A"
                        print ("Sample Rate not found")
                    
                    print(items)
                    print(sampleRate)

                    break

    return sampleRate

def FileName(filePath):
     fileName = os.path.basename(filePath)

     return fileName

def Channels(filePath):
    channels = {}
    with open(filePath, "r") as file:
                for line in file:
                    if "Corr Speed" in line:
                        print(line)
                        items = line.split(",")
                             
                        for position, item in enumerate(items):
                            item = item.replace("\"", "")
                            item = item.replace(" ", "")
                            item = item.lower()
                             
                            items[position] = item
                            channels[item] = position

                        break
    return channels


def Telemetry(filePath, channels):
    telemetry = {}
    for channel in channels:
        telemetry[channel] = []
    
    with open(filePath, "r") as file:
        for line in file:
            if "km/h" in line:
                next(file)
                next(file)
                            
                print(line)
                
                for line in file:
                    if line.strip() == "":
                          continue
                     
                    items = line.split(",")

        
                    for position, item in enumerate(items):
                        item = item.replace("\"", "")
                        item = item.replace(" ", "")
                        item = item.replace("\n", "")
                        item = item.lower()

                        items[position] = item

                    for channel in channels:
                        position = channels[channel]
                        value = float(items[position])
                        telemetry[channel].append(value)

    return telemetry