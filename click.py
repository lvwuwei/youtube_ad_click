import time
import selenium
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver

driver = webdriver.Chrome()

# enters email
adButton = ['ytp-ad-preview-container' , 'ytp-ad-preview-container.countdown-next-to-thumbnail']
adTimerDone = 'ytp-ad-skip-button-container'
vidPlaying = r'count-text.style-scope.ytd-comments-header-renderer' #looks for comments header to know whether a video has been selected or not
searchBox = 'ytd-searchbox-spt'
timeStamp = 'ytp-time-current'
totalTime = 'ytp-time-duration'
vidsWatched = 0
exceptionCounter = 0
pauseDetector = False #False for not paused, True for paused


'''
midrollCheckFrequency = int(input('Please enter how often youd like to check for midroll ads, between 7 and 15'))
midrollInputValidation = False
while not midrollInputValidation:
    if midrollCheckFrequency.isdigit() and (midrollCheckFrequency >= 7 and midrollCheckFrequency <=15):
        print(f'Thank you. While the video is playing, there will be a check for skippable midrolls every {midrollCheckFrequency} seconds')
        midrollInputValidation = True
    elif not midrollCheckFrequency or midrollCheckFrequency < 7 or midrollCheckFrequency > 15:
        midrollCheckFrequency = int(input('That is not an acceptable input. Please enter a number between 7 and 15'))
        '''
def launchDriver():
    driver.get('https://www.youtube.com/')
    vidCheck()

def vidCheck():
    video_playing = False
    global exceptionCounter

    while not video_playing:
        try: 
            video_playing = driver.find_element_by_class_name(vidPlaying)
            video_playing = True
        except NoSuchElementException:
            video_playing = False
            print('No video has been selected. Please select a video')
#       video_playing = driver.find_element_by_class_name(vidPlaying)
        time.sleep(3)
        if video_playing == True:
            exceptionCounter = 0
            print('Video selected! Locating ad box')
            adSearch()
        
# looks for skip-ad box
def pauseDetector(previousTimeStamp, previousTimeStamp2, chancesGiven):
    if previousTimeStamp / previousTimeStamp2 == 1:
        chancesGiven += 1
        if chancesGiven == 30:
            timePaused = [0,0]
            timePaused[0] = int((chancesGiven * 15) / 60)
            print('The video has been paused for {timePaused[0]} minutes and {timePaused[1]} seconds. The program will automatically terminate in 30 seconds')
            time.sleep(30)
            finalCheck = vidDurationHandler(1)
            if finalCheck == 'last try':
                print("video has been paused for too long. terminating program")
                closeBrowser()
    elif previousTimeStamp / previousTimeStamp2 != 1:
        return 'Video is not paused. Carry on!'
    
def adSearch():
    global exceptionCounter
    try:
        adButtonPresent = driver.find_element_by_class_name(adButton[1])
        finishedAdTimer = driver.find_element_by_class_name(adTimerDone)
    except NoSuchElementException:
        print('No ad button found')
        time.sleep(1)
        exceptionCounter += 1
        if exceptionCounter >= 25:
            closeBrowser()
        
        adSearch(exceptionCounter)
    if adButtonPresent:
        print('Ad has been found!')
        for second in range(6,-1,-1):
            print(f'Skipping ad in {second}')
            time.sleep(1)
        finishedAdTimer.click()
        print('Ad has been skipped!')
        vidDurationHandler()

    
def vidDurationHandler(afkHandler=0):
    pauseHelper = [0,0,0]
    pauseCounter = 0
    time.sleep(2)
    currentTimeStamp = driver.find_element_by_class_name(timeStamp)
    totalVidTime = driver.find_element_by_class_name(totalTime)
    print(currentTimeStamp.get_attribute('innerHTML') , 'is the current timestamp')
    print(totalVidTime.get_attribute('innerHTML') , 'is the total video time')
    processedTimeStamp = currentTimeStamp.get_attribute('innerHTML').split(':')
    processedTotalTime = totalVidTime.get_attribute('innerHTML').split(':')
    finalizedTimeStamp = (int(processedTimeStamp[0]) * 60) + int(processedTimeStamp[1])
    finalizedTotalTime = (int(processedTotalTime[0]) * 60) + int(processedTotalTime[1])
    print(f'{finalizedTimeStamp} is the the time stamp in seconds')
    print(f'{finalizedTotalTime} is the total time in seconds')
    while finalizedTimeStamp / finalizedTotalTime <= .97:
        
        time.sleep(15)
        print('Video is not close to over!')
        processedTimeStamp = driver.find_element_by_class_name(timeStamp).get_attribute('innerHTML').split(':')
        finalizedTimeStamp = (int(processedTimeStamp[0]) * 60) + int(processedTimeStamp[1])
        print(f'{finalizedTimeStamp} is the current time in seconds')
        print(f'{finalizedTotalTime} is still the total time in seconds')
        if pauseCounter <= 1:
            if afkHandler == 1:
                return 'last try'
            pauseHelper[pauseCounter] = finalizedTimeStamp
            pauseCounter += 1
        elif pauseCounter == 2:
            pauseResult = pauseDetector(pauseHelper[0], pauseHelper[1], pauseHelper[2])
            print(pauseResult)
        
    else:
        global vidsWatched
        vidsWatched += 1
        print('Video is basically over. Wait for autoplay or select a new video!\n')
        print(f'You\'ve watched {vidsWatched} videos in this session')
        time.sleep(15)
        vidCheck()
#unfinished, needs to look through channels in 1st if statement to find exact 
#channel & need a way to see subscriptions even when public 
#(Cuz youtube isnt showing them on the channel's homepage like it should)
def subsShortcut(): 
    baseChannel = input("Please enter the name or link of the channel that you want to search the subscriptions of")
    if baseChannel.isalnum():
        sBox1 = driver.find_element_by_class_name(searchBox) 
        #sBox2 alone might be sufficient, as its the only time 'search-input'
        # appears in an ID field in the html. if so change searchBox to 'search-input'
        sBox2 = driver.find_element_by_id('search-input')
        if sBox1 and sBox2:
            sBox2.click()
            sBox2.send_keys(baseChannel)
            sBox2.send_keys(Keys.ENTER)
    elif len(baseChannel) >= 32 and not baseChannel.isalnum():
        driver.get(baseChannel)
    pass
            
def closeBrowser():
    driver.close()
    print('Successfully closed browser! No memory leaks here!')

if __name__ == '__main__':
    launchDriver()
    closeBrowser()

    
