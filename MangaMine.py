#Ver. 0.2.2
#Authors: Dylan Wise & Zach Almon

import urllib.request
import re
import os

def main():
    success = False
    currentDirectory = os.getcwd()

    print('Currently MangaMine only supports MangaPanda.')
    print()
    print('The URL you are to input below should be the top level page of the')
    print('manga you wish to download')
    print('Ex: http://www.mangapanda.com/372/seto-no-hanayome.html ')

    while success == False:
        downloadManga = True

        print()
        print('Please enter the url of the manga you wish to download (or q to quit): ')
        urlRequest = input('')

        if urlRequest == 'q':
            return 

        #take the URL the user gave and cut off last five characters (.html)
        try:
            urllibHTML = urllib.request.urlopen(urlRequest).read()
            urlRequest = urlRequest[:-5]

        except:
            print()
            print('Invalid URL!')
            downloadManga = False

            #links to chapters on mangapanda are identified by the class 'chico_manga'
        if downloadManga == True:
            allChaps = re.findall(r'<div class="chico_manga"></div>\\n<a href="+(.*?)\">+', str(urllibHTML))

            numOfLoops = len(allChaps)
            
            #However the 6 most recent chapters are also under the 'chico_manga' class
            #so it is necessary to pop those chapters off and if there are not a total
            #of 6 chapters in the manga we have special cases
            if numOfLoops < 12:

                if numOfLoops == 10:
                    numOfLoops = 5
                    for i in range(5):
                        allChaps.pop(0)
                    
                elif numOfLoops == 8:
                    numOfLoops = 4
                    for i in range(4):
                        allChaps.pop(0)

                elif numOfLoops == 6:
                    for i in range(3):
                        allChaps.pop(0)

                elif numOfLoops == 4:
                    numOfLoops = 2
                    for i in range(2):
                        allChaps.pop(0)

                elif numOfLoops == 2:
                    numOfLoops = 1
                    allChaps.pop(0)

                else:
                    print('There was an error parsing the HTML!')

            else:
                numOfLoops = numOfLoops - 6
                for i in range(6):
                    allChaps.pop(0)

            #Rather conveniently, there is a class called 'aname' which contains the name of the manga
            grabName = re.findall(r'<h2 class="aname">+(.*?)\</h2>+', str(urllibHTML))
            directoryName = currentDirectory + "\\" + str(grabName[0])

            try: 
                os.makedirs(directoryName)    

            except OSError:                    
                if not os.path.isdir(directoryName):
                    raise

            os.chdir(directoryName)

            #loops chapter URLs to determine chapter number for both types of URLs
            chapterNames = []
            for i in range(len(allChaps)):
                chapterNum = re.findall('((?:\d)+)', allChaps[i])
                chapterNames.append(chapterNum[-1])
            
            fullDownload = False
            while 1:
                print('Do you wish to download the entire manga?[y/n]')
                continueChoiceFullDownload = input('')

                if continueChoiceFullDownload == 'y':
                    fullDownload = True
                    break

                elif continueChoiceFullDownload == 'n':
                    break

                else:
                    print('Invalid Option!')

            #Inquires the user if they wish to start from a specific chapter instead of downloading them all
            customStart = False
            chapterFound = False
            startLocation = 0

            if fullDownload == False:
                while 1:
                    print('Do you wish to start download from a certain chapter?[y/n]')
                    continueChoiceCustomChap = input('')

                    if continueChoiceCustomChap == 'y':
                        print('Please enter the chapter you wish to start from.')
                        chapNum = input('')

                        for i in range(len(chapterNames)):
                            if chapNum == chapterNames[i]:
                                chapterFound = True
                                customStart = True
                                startLocation = i

                        if chapterFound == False:
                            print('Invalid chapter number! Maybe the chapter is missing?')
                            print()

                        else:
                            break

                    elif continueChoiceCustomChap == 'n':
                        break

                    else:
                        print('Invalid Option!')
                        print()

            singleChapter = False
            validRange = False
            firstChap = 0
            lastChap = 0
            onlyChap = 0
            if customStart == False and fullDownload == False:
                while 1:
                    print('Do you wish to download a specific range of chapters? (or a single chapter?)')
                    print('[y/n]')
                    continueChoiceRangeChap = input('')

                    if continueChoiceRangeChap == 'y':
                        print('Please enter the range (in format 34-65) with no spaces or a single number for') 
                        print('one chapter.')
                        chapterRange = input('')

                        #looks for the patter 23-32, the numbers can be of any size
                        rangeString = re.findall('((?:\d+)[-/.](?:\d+))', chapterRange)
                        if len(rangeString) == 0:
                            #if that pattern is not detected it looks for a single number of any size
                            singleString = re.findall('((?:\d)+)', chapterRange)

                            if len(singleString) == 0:
                                print('That is an invalid range!')
                                print()

                            elif len(singleString) == 1:
                                for i in range(len(chapterNames)):
                                    if singleString[0] == chapterNames[i]:
                                        singleChapter = True
                                        onlyChap = i

                            else:
                                print('That is an invalid range!')
                                print()

                        elif len(rangeString) == 1:
                            #if pattern is valid look for the individual numbers
                            startAndEnd = re.findall('((?:\d)+)', rangeString[0])

                            if int(startAndEnd[1]) - int(startAndEnd[0]) > 0:
                                firstChapFound = False
                                lastChapFound = False

                                #we can always assume that the length of startAndEnd is 2
                                for i in range(len(startAndEnd)):
                                    for k in range(len(chapterNames)):

                                        if startAndEnd[i] == chapterNames[k]:

                                            if i == 0:
                                                firstChap = k
                                                firstChapFound = True

                                            if i == 1:
                                                lastChap = k
                                                lastChapFound = True

                                if firstChapFound == True and lastChapFound == True:
                                    validRange = True

                            #if the range is just one number (ex. 61-61) we only download that chapter
                            elif int(startAndEnd[1]) - int(startAndEnd[0]) == 0:

                                for i in range(len(chapterNames)):
                                    if startAndEnd[0] == chapterNames[i]:
                                        singleChapter = True
                                        onlyChap = i

                            else:
                                print('That is an invalid range!')
                                print()

                        else:
                            print('That is an invalid range!')
                            print()

                        if singleChapter == True or validRange == True:
                            break

                        else:
                            print('That is an invalid range!')
                            print('')

                    elif continueChoiceRangeChap == 'n':
                        break

                    else:
                        print('Invalid Option!')
                        print()

            #If the user chose a custom start location pop all chapters before off
            if customStart == True:
                for i in range(startLocation):
                    allChaps.pop(0)
                    chapterNames.pop(0)

            if singleChapter == True:
                for i in range(onlyChap):
                    allChaps.pop(0)
                    chapterNames.pop(0)

                for i in range(len(allChaps)-1):
                    allChaps.pop(-1)
                    chapterNames.pop(-1)

            if validRange == True:
                for i in range(firstChap):
                    allChaps.pop(0)
                    chapterNames.pop(0)

                for i in range(len(allChaps)-(lastChap-firstChap)-1):
                    allChaps.pop(-1)
                    chapterNames.pop(-1)


            if fullDownload == True or customStart == True or singleChapter == True or validRange == True:

                for i in range(len(allChaps)):

                    chapDirectoryName = directoryName + "\\Chapter " + str(chapterNames[i])

                    try: 
                        os.makedirs(chapDirectoryName)    

                    except OSError:                    
                        if not os.path.isdir(chapDirectoryName):
                            raise

                    os.chdir(chapDirectoryName)

                    #There are some special cases associated with the first loop through the chapter
                    isFirstLoopPage = True

                    chapURL = "http://www.mangapanda.com" + allChaps[i]
                    print("Downloading Chapter", str(chapterNames[i]))

                    imageLocation = 0

                    while 1:
                        try:
                            imageLocation += 1

                            #Looks at page URLs for any and all sequences of numbers
                            nextChapDetermine = re.findall('((?:\d)+)', chapURL)

                            urllibHTML = urllib.request.urlopen(chapURL).read()

                            if isFirstLoopPage == True:
                                determineAmountOfPages = re.findall('<option value="+(.*?)\</option>', str(urllibHTML))

                            if len(determineAmountOfPages) == imageLocation - 1:
                                break

                            #Checks the number of files in directory in comparison to the number of images in the chapter
                            #If the number is the same the assumption is made that all images have been downloaded
                            if isFirstLoopPage == True:
                                isFirstLoopPage = False
                                numOfFileInCWD = len([name for name in os.listdir('.') if os.path.isfile(name)])
                                if numOfFileInCWD == len(determineAmountOfPages):
                                    break
                        
                            #grabs both the next page URL and the URL for the image on the current page
                            URLandIMG = re.findall(r'<div id="imgholder">+(.*?)\" alt=+', str(urllibHTML))
                            nextPageURL = re.findall(r'<a href="+(.*?)\">', URLandIMG[0])
                            imageURL = re.findall(r'src="+(.*?)\.jpg', URLandIMG[0])
                        
                            imageName = "Page " + str(imageLocation) + ".jpg"
                            fileExists = os.path.isfile(imageName)
                            print("Downloading Page", imageLocation) 


                            #If file does not already exist, opens a file, writes image binary data to it and closes
                            if fileExists == False:
                                rawImage = urllib.request.urlopen(imageURL[0] + ".jpg").read()
                                fout = open(imageName, 'wb')       
                                fout.write(rawImage)                          
                                fout.close()
                        
                            chapURL = "http://www.mangapanda.com" + nextPageURL[0]

                        #Probably need to do more with this error
                        except:
                            print("Invalid URL Error!")
                            return
            
                while 1:
                    print('Do you wish to download another manga?[y/n]')
                    continueChoice = input('')

                    if continueChoice == 'y':
                        break

                    elif continueChoice == 'n':
                        success = True
                        break

                    else:
                        print('Invalid Option!')

main()
