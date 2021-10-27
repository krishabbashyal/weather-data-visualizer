import os
from matplotlib import pyplot as plt
import numpy as numpy

def main():

    print(os.listdir("CityData"))
    dataFile = input("Which city's data would you like to open: ")

    # Cleaning user input to ensure that capilization and file extention are in proper format.
    dataFile.title()
    if dataFile[-1].lower() != "v":
        dataFile += ".CSV"

    # If invalid file was entered main() will be re-called until valid input if given
    try:
        openedFile = open("CityData/" + dataFile,'r')
        readFile = openedFile.read()
    except:
        print("\nInvalid entry, please retry")
        main()

    dataCollum = input("\n1. Temperature\n2. Humidity\n3. GHI\nWhat data would you like to plot: ")
    chartType = input("\n1. Scatter\n2. Discrete\n3. Monthly\nWhat type of chart would you like to plot: ")

    listRowsWork = readFile.split('\n')
    listRows = listRowsWork[2:8762]

    workingList = []

    for x in range(0, 8760):
        workingList.append(listRows[x].split(','))

    dateData = []
    timeData = []
    ghiData = []
    tempData = []
    humidityData = []

    for x in range(0, 8760):
        dateData.append(str(workingList[x][0]))
        timeData.append(str(workingList[x][1]))
        ghiData.append(float(workingList[x][4]))
        tempData.append(float(workingList[x][31]))
        humidityData.append(float(workingList[x][37]))

    monthly = []
    hourly = []

    for x in range(0, 8760):
        monthly.append(int(str(dateData[x])[:2]))
        hourly.append(int(str(timeData[x])[:2]))

    if chartType == "1" or chartType.lower() == "scatter":
        plt.style.use("seaborn")
        plt.figure("Code by Krishab Bashyal")
        plt.title(f"Scatter Plot (Each Hour of Day) for {dataFile}")
        xAxis = hourly

        if dataCollum == "1" or dataCollum.lower() == "temprature":
            yAxis = tempData
            plt.ylabel("Temperature in °C")
        if dataCollum == "2" or dataCollum.lower() == "humidity":
            yAxis = humidityData
            plt.ylabel("Humidity in %")
        if dataCollum == "3" or dataCollum.lower() == "ghi":
            yAxis = ghiData
            plt.ylabel("Solar Irradiance")

        plt.xlabel("Hour of Day")
        plt.scatter(xAxis, yAxis, s = 5, color = "#38618c")

    if chartType == "2" or chartType.lower() == "discrete":
        plt.style.use("seaborn")
        plt.figure("Code by Krishab Bashyal")
        plt.title(f"Discrete Values (Each Hour of the Year) for {dataFile}")
        xAxis = range(0,8760)

        if dataCollum == "1" or dataCollum.lower() == "temprature":
            yAxis = tempData
            plt.ylabel("Temperature in °C")
        if dataCollum == "2" or dataCollum.lower() == "humidity":
            yAxis = humidityData
            plt.ylabel("Humidity in %")
        if dataCollum == "3" or dataCollum.lower() == "ghi":
            yAxis = ghiData
            plt.ylabel("Solar Irradiance")

        area = 6  #point radius
        plt.xlabel("Hour of the Year")
        plt.scatter(xAxis, yAxis, s = 5, color = "#38618c")

    if chartType == "3" or chartType.lower() == "monthly":
        min = []
        max = []
        avg = []
        monthCounter = 1
        accumlatorDivision = 0

        minimumVal = 10000
        maximumVal = -10000
        accumulatorVal = 0

        for x in range(0, 8760):
            if dataCollum == "1" or dataCollum.lower() == "temprature":
                if tempData[x] < minimumVal:
                    minimumVal = tempData[x]

                if tempData[x] > maximumVal:
                    maximumVal = tempData[x]

                accumulatorVal += tempData[x]

            if dataCollum == "2" or dataCollum.lower() == "humidity":
                if humidityData[x] < minimumVal:
                    minimumVal = humidityData[x]

                if humidityData[x] > maximumVal:
                    maximumVal = humidityData[x]

                accumulatorVal += humidityData[x]

            if dataCollum == "3" or dataCollum.lower() == "ghi":
                if ghiData[x] < minimumVal:
                    minimumVal = ghiData[x]

                if ghiData[x] > maximumVal:
                    maximumVal = ghiData[x]

                accumulatorVal += ghiData[x]

            accumlatorDivision += 1

            if x == 8759:

                min.append(minimumVal)
                max.append(maximumVal)
                avg.append(accumulatorVal / accumlatorDivision)
                monthCounter += 1
                accumlatorDivision = 0

                minimumVal = 10000
                maximumVal = -10000
                accumulatorVal = 0

            if x < 8759:

                if monthCounter != monthly[x + 1]:
                    min.append(minimumVal)
                    max.append(maximumVal)
                    avg.append(accumulatorVal / accumlatorDivision)
                    monthCounter += 1
                    accumlatorDivision = 0

                    minimumVal = 10000
                    maximumVal = -10000
                    accumulatorVal = 0

        plt.style.use("seaborn")
        plt.figure("Code by Krishab Bashyal")
        monthGroups = numpy.arange(12)
        barPadding = 0.25

        for month in range(0, 12):
            plt.bar(month, min[month], barPadding, color = "#38618c")
            plt.bar(month + barPadding, avg[month], barPadding, color = "#ffe74c")
            plt.bar(month + barPadding + barPadding, max[month], barPadding, color = "#ff5964" )

        if dataCollum == "1" or dataCollum.lower() == "temprature":
            yAxis = tempData
            plt.ylabel("Temperature in °C")
        if dataCollum == "2" or dataCollum.lower() == "humidity":
            yAxis = humidityData
            plt.ylabel("Humidity in %")
        if dataCollum == "3" or dataCollum.lower() == "ghi":
            yAxis = ghiData
            plt.ylabel("Solar Irradiance")
        
        plt.title(f'Monthly Minimum, Maximum and Averages for {dataFile}')
        plt.xticks(monthGroups + barPadding, ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
        plt.legend(["Minimum", "Average", "Maximum"])

    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()