import os
import shutil

dir1 = "D:\Github Projects\Elderly-Assistant-System\exercise_module\data\\arm_flexion_and_extension\correct\\"
correct=[]

for filename in os.listdir(dir1):
    correct.append(filename[:-4])
  
dir2 = "D:\Github Projects\Elderly-Assistant-System\exercise_module\data\\arm_flexion_and_extension\incorrect\\"
incorrect=[]
for filename in os.listdir(dir2):
    incorrect.append(filename[:-4])
    
dir3= "D:\Github Projects\Elderly-Assistant-System\exercise_module\data\\arm_flexion_and_extension\\flipped\\"

for filename in os.listdir(dir3):
    if filename[8:-4] in correct:
        shutil.move(os.path.join(dir3,filename),os.path.join(dir1,filename))
        
        
    if filename[8:-4] in incorrect:
        shutil.move(os.path.join(dir3,filename),os.path.join(dir2,filename))