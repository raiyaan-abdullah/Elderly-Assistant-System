import os
import shutil

dir1 = "D:\Github Projects\Elderly-Assistant-System\exercise_module\data\\arm_flexion_and_extension_5x\\test\correct\\"
correct=[]

for filename in os.listdir(dir1):
    correct.append(filename[:-4])
  
dir2 = "D:\Github Projects\Elderly-Assistant-System\exercise_module\data\\arm_flexion_and_extension_5x\\test\incorrect\\"
incorrect=[]
for filename in os.listdir(dir2):
    incorrect.append(filename[:-4])
    
dir3 = "D:\Github Projects\Elderly-Assistant-System\exercise_module\data\\arm_flexion_and_extension_5x\\train\\correct\\"
dir4 = "D:\Github Projects\Elderly-Assistant-System\exercise_module\data\\arm_flexion_and_extension_5x\\train\\incorrect\\"
dir5 = "D:\Github Projects\Elderly-Assistant-System\exercise_module\data\\arm_flexion_and_extension_5x\\unused\\correct\\"
dir6 = "D:\Github Projects\Elderly-Assistant-System\exercise_module\data\\arm_flexion_and_extension_5x\\unused\\incorrect\\"

for filename in os.listdir(dir3):
    if filename[8:-4] in correct:
        shutil.move(os.path.join(dir3,filename),os.path.join(dir5,filename))
        
for filename in os.listdir(dir4):       
    if filename[8:-4] in incorrect:
        shutil.move(os.path.join(dir4,filename),os.path.join(dir6,filename))