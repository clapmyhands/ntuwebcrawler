import re

with open('scripts/output/tribun/2015/08/21.xml','r') as myFile:
    f = myFile.readlines();
f = "\n".join(f)

sub = re.sub(r'<(.*?)\>',"",f)
sub = re.sub(r'[^A-Za-z0-9 ]',"",sub)

print(sub)
