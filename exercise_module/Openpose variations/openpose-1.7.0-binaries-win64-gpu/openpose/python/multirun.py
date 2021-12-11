
import os


location= '../arm_movement_good/'
for file in os.listdir(location):
    file_path= location+file
    output_folder= file[:-4]+'/'


    os.system('python openpose_python.py --video '+file_path+' --write_json output_json_folder/arm_movement_good/'+output_folder)