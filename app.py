from CO2Server import CO2Server


if __name__ == '__main__':
    plantServer = CO2Server()
    analizerList = plantServer.getGroupOfCO2Data()

    print(len(analizerList))

    # for i in range(0, 10):
    #     analizersList[i].startCalculate()
    #
    #     if analizersList[i].isBroken == False:
    #         print("good")
    #         print(analizersList[i].startPos)
    #         print(analizersList[i].endPos)
    #         analizersList[i].drawPlot()


    for analizer in analizerList:
        analizer.startCalculate()
        if analizer.isBroken == False:
            analizer.drawPlot()




    #
    # if len(analizersList) > 0:
    #     analizersList[0].startCalculate()
    #
    #     if analizersList[0].isBroken == False:
    #         print("good")
    #         print(analizersList[0].startPos)
    #         print(analizersList[0].endPos)
    #         analizersList[0].drawPlot()
