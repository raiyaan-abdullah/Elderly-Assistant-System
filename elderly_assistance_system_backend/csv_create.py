import csv
import shutil
from medicine.models import Medicine

medicine_objects=Medicine.objects.all()
med_list=[]
for med in medicine_objects:
    if [med.name] in med_list:
        pass
    else:  
        med_list.append([med.name])
print(med_list)
# opening the csv file in 'w+' mode
file = open('medicine_strip_text_recognition/medicine_list.csv', 'w+', newline ='')

# writing the data into the file
with file:	
	write = csv.writer(file)
	write.writerows(med_list)
print("CSV file created..")
path="C:/Users/Riad/Documents/GitHub/Elderly-Assistance-System/elderly_assistance_system/elderly_assistance_system_backend/"


