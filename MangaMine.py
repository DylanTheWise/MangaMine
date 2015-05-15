#Ver. 0.2
#Authors: Dylan Wise & Zach Almon
import urllib.request
import re
import os

#def findURLType(URLList):
    #URLType = []
    
    #Looks through the list of URLs for each chapter and determines its URL type
    #MangaPanda has two types of URLs, one that leads with 3 numbers sperated by
    #a dash and another that only has the chapter number.

    #for i in range(len(URLList)):
                                 #locates 3 numbers seperated by dashes ex. 42-87-24
    #    URLString = re.findall('((?:\d)+)([-/.])((?:\d)+)([-/.])((?:\d)+)', URLList[i])

    #    if len(URLString) == 0:
    #        URLType.append(0)

    #    else:
    #        URLType.append(1)

    #return URLType

def determineChapterNames(allChaps):
    chapterNames = []

    #loops chapter URLs to determine chapter number for both types of URLs
    for i in range(len(allChaps)):
        chapterNum = re.findall('((?:\d)+)', allChaps[i])
        chapterNames.append(chapterNum[-1])

        #if listOfURLTypes[i] == 0:
        #    chapterNames.append(chapterNum[-1])

        #if listOfURLTypes[i] == 1:
        #    chapterNames.append(chapterNum[-1])

    return chapterNames

def main():
    success = False
    currentDirectory = os.getcwd()

    print('Currently MangaMine only supports MangaPanda.')
    print()
    print('The URL you are to input below should be the top level page of the')
    print('manga you wish to download')
    print('Ex: http://www.mangapanda.com/372/seto-no-hanayome.html ')

    while(success == False):
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

            #listOfURLTypes = findURLType(allChaps)
            chapterNames = determineChapterNames(allChaps)

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

                imageLocation = 1
                allImagesFound = False

                while allImagesFound == False:
                    try:
                        #Looks at page URLs for any and all sequences of numbers
                        nextChapDetermine = re.findall('((?:\d)+)', chapURL)

                        urllibHTML = urllib.request.urlopen(chapURL).read()

                        if isFirstLoopPage == True:
                            determineAmountOfPages = re.findall('<option value="+(.*?)\</option>', str(urllibHTML))

                        #If on the first loop we look at the very last number in the list
                        #On every loop but the fist look at the second to last position in the list

                        if len(determineAmountOfPages) == imageLocation - 1:
                            break

                        #if listOfURLTypes[i] == 0:
                        #    if isFirstLoopPage == True:
                        #        if nextChapDetermine[-1] != chapterNames[i]:
                        #            break

                        #    else:
                        #        if len(determineAmountOfPages) == imageLocation:
                        #            if nextChapDetermine[-1] != chapterNames[i]:
                        #                break

                        #        if nextChapDetermine[-2] != chapterNames[i]:
                        #            break


                        #if listOfURLTypes[i] == 1:
                        #    if nextChapDetermine[-1] != chapterNames[i]:
                        #        break

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
                        imageLocation += 1

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
