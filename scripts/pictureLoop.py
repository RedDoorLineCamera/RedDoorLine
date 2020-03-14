import os
import time
import datetime

PICTURES_STORED = 0
TIME_BETWEEN = 50  # Seconds
dateObj = datetime.datetime
openTime_dict = {0 : 7, 1 : 7, 2: 7, 3 : 7, 4 : 7, 5 : 15, 6 : 15}
indexPath = 'RedDoorLine/index.html'
pushCodePath = 'push.sh'
nightClose = False

while True:
    currDatetime = datetime.datetime.now()
    now = currDatetime.timetuple()
    dateString = f'{now[0]}-{now[1]}-{now[2]}-{now[3]}:{now[4]:02}:{now[5]:02}'
    print(f'Current Time: {dateString}')
    # openTime = openTime_dict[now[6]]
    if now[3] < 2 or now[3] >= 17:
        TIME_BETWEEN = 50
        nightClose = False
        try:
            imgName = f"rdLine@{dateString}.jpg"
            os.system('rm ~/RedDoorLine/images/line/*')
            os.system(f'raspistill -o ~/RedDoorLine/images/line/{imgName} '
                      f'-rot 90 -ex snow -h 808 -roi .5,.2,.333,1 -br 55')
            # os.system(f'cp ~/RedDoorLine/images/{imgName} ~/RedDoorPics')
            lines = []
            with open(indexPath, 'r') as file:
                for line in file:
                    lines.append(line)
            with open(indexPath, 'w') as file:
                for string in lines:
                    if string.strip()[0:4] == "<img":
                        file.write(f'      <img src="images/line/{imgName}">\n')
                    elif string.strip()[0:4] == "<p>P":
                        fTime = currDatetime.strftime('%d %B %Y, %H:%M:%S')
                        file.write(
                            f'  <p>Picture from <b>{fTime}.</b>\n')
                    else:
                        file.write(string)
            newlines = []
            with open(pushCodePath, 'r') as file:
                for line in file:
                    newlines.append(line)
            with open(pushCodePath, 'w') as file:
                for string in newlines:
                    if string[0:6] == 'git co':
                        file.write(
                            f'git commit -m "autoCommit@{dateString}"\n')
                    else:
                        file.write(string)
            os.system('cd ~/')
            os.system('~/push.sh')
            PICTURES_STORED += 1
            if PICTURES_STORED >= 50:
                os.system('cd ~/')
                os.system('~/deleteImageHistory.sh')
                PICTURES_STORED = 0
        except Exception as e:
            print(f'Error: {e}')
            exit(1)
    else:
        if not nightClose:
            lines = []
            with open(indexPath, 'r') as file:
                for line in file:
                    lines.append(line)
            with open(indexPath, 'w') as file:
                for string in lines:
                    if string.strip()[0:4] == "<img":
                        file.write(f'      <img src="images/closed.png">\n')
                    elif string.strip()[0:4] == "<p>P":
                        file.write(
                            f'  <p>Picture from <b>----------.</b>\n')
                    else:
                        file.write(string)
            os.system('cd ~/')
            os.system('~/push.sh')
            nightClose = True
        TIME_BETWEEN = 3600
    print(f'Pausing for {TIME_BETWEEN} seconds')
    time.sleep(TIME_BETWEEN)
