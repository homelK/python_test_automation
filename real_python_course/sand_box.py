from datetime import datetime, timezone, timedelta


time = datetime.now(timezone(timedelta(hours=+3)))
print(time)


