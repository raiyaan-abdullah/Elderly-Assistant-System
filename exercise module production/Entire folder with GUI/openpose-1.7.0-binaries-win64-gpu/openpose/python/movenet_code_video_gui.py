# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 01:13:42 2021

@author: Riad
"""
import os
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow_docs.vis import embed
import numpy as np
import cv2
import wget
import time
import pyttsx3
import speech_recognition as sr
import glob
import shutil

# Import matplotlib libraries
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.patches as patches

# Some modules to display an animation using imageio.
import imageio
from IPython.display import HTML, display
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject

#@title Helper functions for visualization

# Dictionary that maps from joint names to keypoint indices.
KEYPOINT_DICT = {
    'nose': 0,
    'left_eye': 1,
    'right_eye': 2,
    'left_ear': 3,
    'right_ear': 4,
    'left_shoulder': 5,
    'right_shoulder': 6,
    'left_elbow': 7,
    'right_elbow': 8,
    'left_wrist': 9,
    'right_wrist': 10,
    'left_hip': 11,
    'right_hip': 12,
    'left_knee': 13,
    'right_knee': 14,
    'left_ankle': 15,
    'right_ankle': 16
}

# Maps bones to a matplotlib color name.
KEYPOINT_EDGE_INDS_TO_COLOR = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'
}


class movenet_Thread(QThread):
    movenet_status = pyqtSignal(QObject)


    def _keypoints_and_edges_for_display(self, keypoints_with_scores,
                                         height,
                                         width,
                                         keypoint_threshold=0.3):
      """Returns high confidence keypoints and edges for visualization.

      Args:
        keypoints_with_scores: A numpy array with shape [1, 1, 17, 3] representing
          the keypoint coordinates and scores returned from the MoveNet model.
        height: height of the image in pixels.
        width: width of the image in pixels.
        keypoint_threshold: minimum confidence score for a keypoint to be
          visualized.

      Returns:
        A (keypoints_xy, edges_xy, edge_colors) containing:
          * the coordinates of all keypoints of all detected entities;
          * the coordinates of all skeleton edges of all detected entities;
          * the colors in which the edges should be plotted.
      """
      keypoints_all = []
      keypoint_edges_all = []
      edge_colors = []
      num_instances, _, _, _ = keypoints_with_scores.shape
      for idx in range(num_instances):
        kpts_x = keypoints_with_scores[0, idx, :, 1]
        kpts_y = keypoints_with_scores[0, idx, :, 0]
        kpts_scores = keypoints_with_scores[0, idx, :, 2]
        kpts_absolute_xy = np.stack(
            [width * np.array(kpts_x), height * np.array(kpts_y)], axis=-1)
        kpts_above_thresh_absolute = kpts_absolute_xy[
            kpts_scores > keypoint_threshold, :]
        keypoints_all.append(kpts_above_thresh_absolute)

        for edge_pair, color in KEYPOINT_EDGE_INDS_TO_COLOR.items():
          if (kpts_scores[edge_pair[0]] > keypoint_threshold and
              kpts_scores[edge_pair[1]] > keypoint_threshold):
            x_start = kpts_absolute_xy[edge_pair[0], 0]
            y_start = kpts_absolute_xy[edge_pair[0], 1]
            x_end = kpts_absolute_xy[edge_pair[1], 0]
            y_end = kpts_absolute_xy[edge_pair[1], 1]
            line_seg = np.array([[x_start, y_start], [x_end, y_end]])
            keypoint_edges_all.append(line_seg)
            edge_colors.append(color)
      if keypoints_all:
        keypoints_xy = np.concatenate(keypoints_all, axis=0)
      else:
        keypoints_xy = np.zeros((0, 17, 2))

      if keypoint_edges_all:
        edges_xy = np.stack(keypoint_edges_all, axis=0)
      else:
        edges_xy = np.zeros((0, 2, 2))
      return keypoints_xy, edges_xy, edge_colors


    def draw_prediction_on_image(self,
        image, keypoints_with_scores, crop_region=None, close_figure=False,
        output_image_height=None):
      """Draws the keypoint predictions on image.

      Args:
        image: A numpy array with shape [height, width, channel] representing the
          pixel values of the input image.
        keypoints_with_scores: A numpy array with shape [1, 1, 17, 3] representing
          the keypoint coordinates and scores returned from the MoveNet model.
        crop_region: A dictionary that defines the coordinates of the bounding box
          of the crop region in normalized coordinates (see the init_crop_region
          function below for more detail). If provided, this function will also
          draw the bounding box on the image.
        output_image_height: An integer indicating the height of the output image.
          Note that the image aspect ratio will be the same as the input image.

      Returns:
        A numpy array with shape [out_height, out_width, channel] representing the
        image overlaid with keypoint predictions.
      """
      height, width, channel = image.shape
      aspect_ratio = float(width) / height
      fig, ax = plt.subplots(figsize=(12 * aspect_ratio, 12))
      # To remove the huge white borders
      fig.tight_layout(pad=0)
      ax.margins(0)
      ax.set_yticklabels([])
      ax.set_xticklabels([])
      plt.axis('off')

      im = ax.imshow(image)
      line_segments = LineCollection([], linewidths=(4), linestyle='solid')
      ax.add_collection(line_segments)
      # Turn off tick labels
      scat = ax.scatter([], [], s=60, color='#FF1493', zorder=3)

      (keypoint_locs, keypoint_edges,
       edge_colors) = self._keypoints_and_edges_for_display(
           keypoints_with_scores, height, width)

      line_segments.set_segments(keypoint_edges)
      line_segments.set_color(edge_colors)
      if keypoint_edges.shape[0]:
        line_segments.set_segments(keypoint_edges)
        line_segments.set_color(edge_colors)
      if keypoint_locs.shape[0]:
        scat.set_offsets(keypoint_locs)

      if crop_region is not None:
        xmin = max(crop_region['x_min'] * width, 0.0)
        ymin = max(crop_region['y_min'] * height, 0.0)
        rec_width = min(crop_region['x_max'], 0.99) * width - xmin
        rec_height = min(crop_region['y_max'], 0.99) * height - ymin
        rect = patches.Rectangle(
            (xmin,ymin),rec_width,rec_height,
            linewidth=1,edgecolor='b',facecolor='none')
        ax.add_patch(rect)

      fig.canvas.draw()
      image_from_plot = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
      image_from_plot = image_from_plot.reshape(
          fig.canvas.get_width_height()[::-1] + (3,))
      plt.close(fig)
      if output_image_height is not None:
        output_image_width = int(output_image_height / height * width)
        image_from_plot = cv2.resize(
            image_from_plot, dsize=(output_image_width, output_image_height),
             interpolation=cv2.INTER_CUBIC)
      return image_from_plot

    def to_gif(self, images, fps):
      """Converts image sequence (4D numpy array) to gif."""
      imageio.mimsave('./animation.gif', images, fps=fps)
      return embed.embed_file('./animation.gif')

    def speak(self, text):
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', 80)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.say(text)
        engine.runAndWait()

    # simple function to recognise speech from user
    def takecommand(self):
        #it takes microphone input and returns string output
        r = sr.Recognizer()
        with sr.Microphone(1) as source:
            print('Listening.....')
            r.pause_threshold = 1
            r.energy_threshold = 4000
            audio = r.listen(source)

        try:
            print('Recognising...')
            query = r.recognize_google(audio, language='en-in')
            print('User Said : ' , query)


        except Exception as e:
            pass
            '''print('exception : ',e)

            #self.speak("Please say yes when you are ready")
            return "None"'''
        return "none"


    def record_video(self):

        # Create a VideoCapture object
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 1280)
        self.cap.set(4, 720)

        # Default resolutions of the frame are obtained.The default resolutions are system dependent.
        # We convert the resolutions from float to integer.
        frame_width = int(self.cap.get(3))
        frame_height = int(self.cap.get(4))

        # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
        out = cv2.VideoWriter('movenet/record.mp4',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))

        initial_time= time.time()
        current_time=0
        while(True):
          current_time= time.time()
          self.ret, frame = self.cap.read()

          if (current_time - initial_time) > 6:
              self.movenet_status.emit(self)
              break
          else:

            # Write the frame into the file 'output.avi'
            out.write(frame)
            self.movenet_status.emit(self)

            # Display the resulting frame
            cv2.imshow('frame',frame)

            # Press Q on keyboard to stop recording
            if cv2.waitKey(1) & 0xFF == ord('q'):
              break


        # When everything done, release the video capture and video write objects
        self.cap.release()
        out.release()

        # Closes all the frames
        cv2.destroyAllWindows()



    def progress(self, value, max=100):
      return HTML("""
          <progress
              value='{value}'
              max='{max}',
              style='width: 100%'
          >
              {value}
          </progress>
      """.format(value=value, max=max))

    model_name = "movenet_thunder" #@param ["movenet_lightning", "movenet_thunder", "movenet_lightning_f16.tflite", "movenet_thunder_f16.tflite", "movenet_lightning_int8.tflite", "movenet_thunder_int8.tflite"]

    if "tflite" in model_name:
      if "movenet_lightning_f16" in model_name:
          model= "movenet/models/lite-model_movenet_singlepose_lightning_tflite_float16_4.tflite"
          input_size = 192
      elif "movenet_thunder_f16" in model_name:
          model= "movenet/models/lite-model_movenet_singlepose_thunder_tflite_float16_4.tflite"
          input_size = 256
      elif "movenet_lightning_int8" in model_name:
          model= "movenet/models/lite-model_movenet_singlepose_lightning_tflite_int8_4.tflite"
          input_size = 192
      elif "movenet_thunder_int8" in model_name:
          model= "movenet/models/lite-model_movenet_singlepose_thunder_tflite_int8_4.tflite"
          input_size = 256
      else:
          raise ValueError("Unsupported model name: %s" % model_name)

      # Initialize the TFLite interpreter
      interpreter = tf.lite.Interpreter(model_path=model)
      interpreter.allocate_tensors()

      def movenet(self, input_image):
        """Runs detection on an input image.

        Args:
          input_image: A [1, height, width, 3] tensor represents the input image
            pixels. Note that the height/width should already be resized and match the
            expected input resolution of the model before passing into this function.

        Returns:
          A [1, 1, 17, 3] float numpy array representing the predicted keypoint
          coordinates and scores.
        """
        # TF Lite format expects tensor type of uint8.
        input_image = tf.cast(input_image, dtype=tf.uint8)
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()
        self.interpreter.set_tensor(input_details[0]['index'], input_image.numpy())
        # Invoke inference.
        self.interpreter.invoke()
        # Get the model prediction.
        keypoints_with_scores = self.interpreter.get_tensor(output_details[0]['index'])
        return keypoints_with_scores

    else:
      if "movenet_lightning" in model_name:
        module = hub.load("movenet/models/movenet_singlepose_lightning_4")
        input_size = 192
      elif "movenet_thunder" in model_name:
        module = hub.load("movenet/models/movenet_singlepose_thunder_4")
        input_size = 256
      else:
        raise ValueError("Unsupported model name: %s" % model_name)

      def movenet(self, input_image):
        """Runs detection on an input image.

        Args:
          input_image: A [1, height, width, 3] tensor represents the input image
            pixels. Note that the height/width should already be resized and match the
            expected input resolution of the model before passing into this function.

        Returns:
          A [1, 1, 17, 3] float numpy array representing the predicted keypoint
          coordinates and scores.
        """
        model = self.module.signatures['serving_default']

        # SavedModel format expects tensor type of int32.
        input_image = tf.cast(input_image, dtype=tf.int32)
        # Run model inference.
        outputs = model(input_image)
        # Output is a [1, 1, 17, 3] tensor.
        keypoints_with_scores = outputs['output_0'].numpy()
        return keypoints_with_scores


    KEYPOINT_NAMES=[
        'nose',
        'left_eye',
        'right_eye',
        'left_ear',
        'right_ear',
        'left_shoulder',
        'right_shoulder',
        'left_elbow',
        'right_elbow',
        'left_wrist',
        'right_wrist',
        'left_hip',
        'right_hip',
        'left_knee',
        'right_knee',
        'left_ankle',
        'right_ankle'
    ]


    DATASET = "exercise 1a upto day 3"

    def run(self):

        file1 = open("myfile.txt", "r")

        # \n is placed to indicate EOL (End of Line)
        self.count = int(file1.read())
        #print(value)
        # file1.writelines(L)
        file1.close()


        if self.count==0:

            cap=cv2.VideoCapture(0)
            time.sleep(0.5)
            current_time=0
            prev_time=time.time()
            frame_counter=0
            ready_counter = 0

            while cap.isOpened():
                okay,frame= cap.read()
                frame_counter += 1
                #If the last frame is reached, reset the capture and the frame_counter
                if frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                    frame_counter = 0 #Or whatever as long as it is the same as next line
                    #cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    break
                # Our operations on the frame come here
                '''image_path = 'input_image.jpeg'
                image = tf.io.read_file(image_path)'''

                #image= np.asarray(image).astype(np.float32)
                image=tf.convert_to_tensor(frame, dtype=tf.float32)
                #image = tf.image.decode_jpeg(image)
                # Resize and pad the image to keep the aspect ratio and fit the expected size.
                input_image = tf.expand_dims(image, axis=0)
                input_image = tf.image.resize_with_pad(input_image, self.input_size, self.input_size)

                # Run model inference.
                keypoints_with_scores = self.movenet(input_image)
                keypoints_reduced = np.squeeze(keypoints_with_scores)

                #keypoints_flat = np.ndarray.flatten(keypoints_reduced)
                left_wrist= keypoints_reduced[9]
                right_wrist = keypoints_reduced[10]
                left_shoulder = keypoints_reduced[5]
                right_shoulder = keypoints_reduced[6]
                wrist_level_diff = left_wrist[0]-right_wrist[0]
                left_side_diff = left_wrist[1]-left_shoulder[1]
                right_side_diff = right_wrist[1]-right_shoulder[1]


                if abs(wrist_level_diff) <0.03 and abs(left_side_diff)<0.1 and  abs(right_side_diff)<0.1:
                    ready_counter = ready_counter + 1
                    print("Exercise ready")
                    print("left_wrist: ", keypoints_reduced[9])
                    print("right_wrist: ", keypoints_reduced[10])
                    print("left_shoulder: ", keypoints_reduced[5])
                    print("right_shoulder: ", keypoints_reduced[6])
                else:
                    ready_counter = 0
                    print("------------------------")
                    print("Left wrist: ",left_wrist)
                    print("Right wrist: ",right_wrist)
                    print("Left shoulder: ",left_shoulder)
                    print("Right shoulder: ",right_shoulder)
                    print("Wrist difference is: ",abs(wrist_level_diff))
                    print("Left difference is: ",abs(left_side_diff))
                    print("Right difference is: ",abs(right_side_diff))

                if ready_counter>5:
                    self.speak("Are you ready?")
                    user_reply = self.takecommand()
                    print(user_reply)
                    '''while "yes" not in user_reply:
                        self.speak("Please say yes when you are ready")
                        user_reply = self.takecommand()'''

                    cap.release()
                    cv2.destroyAllWindows()
                    self.record_video()
        if self.count==1:
            self.record_video()


        # Visualize the predictions with image.
        '''display_image = tf.expand_dims(image, axis=0)
        display_image = tf.cast(tf.image.resize_with_pad(
            display_image, 1280, 1280), dtype=tf.int32)
        output_overlay = self.draw_prediction_on_image(
            np.squeeze(display_image.numpy(), axis=0), keypoints_with_scores)

        font = cv2.FONT_HERSHEY_SIMPLEX
        # org
        org = (50, 50)

        # fontScale
        fontScale = 1

        # Blue color in BGR
        color = (255, 0, 0)

        # Line thickness of 2 px
        thickness = 2
        current_time=time.time()
        time_diff=current_time-prev_time
        fps=1/time_diff
        prev_time=current_time
        # Using cv2.putText() method
        image = cv2.putText(output_overlay, "FPS: "+str(int(fps)), org, font,
                           fontScale, color, thickness, cv2.LINE_AA)'''
        '''
        cv2.imshow('frame',image)
        if cv2.waitKey(1) == ord('q'):
            break
        
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
     '''
        if self.count == 0:

            files = glob.glob('movenet/live_json/*')
            path = os.path.join("movenet/live_json", str(self.count))
            for f in files:
                shutil.rmtree(f)
            os.mkdir(path)
        os.system('python openpose_python.py --video movenet/record.mp4 --net_resolution 528x272 --write_json movenet/live_json/'+str(self.count)+'/')