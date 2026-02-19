import os
from datetime import datetime
import pytz

name = os.getenv("USER_NAME", "Tanya")
almaty_tz = pytz.timezone('Asia/Almaty')
almaty_time = datetime.now(almaty_tz).strftime('%Y-%m-%d %H:%M:%S')

print(f"Hello, {name}! Welcome to Docker World.")
print(f"Current time in Almaty: {almaty_time}")
