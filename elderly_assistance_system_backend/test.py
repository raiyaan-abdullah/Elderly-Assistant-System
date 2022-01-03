from datetime import datetime

t= datetime.strptime('14:10:50', '%H:%M:%S')
print(t.strftime("%I:%M %p"))