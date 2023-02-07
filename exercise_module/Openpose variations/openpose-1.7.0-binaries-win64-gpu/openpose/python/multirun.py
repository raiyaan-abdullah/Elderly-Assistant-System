
import os


location= '../arm_abduction_and_adduction/Correct/'
for file in os.listdir(location):
    file_path= location+file
    output_folder= file[:-4]+'/'


    os.system('python openpose_python.py --video '+file_path+' --write_json output_json_folder/arm_abduction_and_adduction/correct/'+output_folder)