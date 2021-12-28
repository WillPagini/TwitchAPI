import schedule
import time
import export

def update():
    export.updateBigquery()

# sets o schedule
schedule.every(60).minutes.do(update)

# verify pending schedulings
while 1:
    schedule.run_pending()
    time.sleep(3)
