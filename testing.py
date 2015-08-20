import re

a = "abcde./ab/ab aduhboi"
tes = re.sub('[^A-Za-z0-9]+','',a)
