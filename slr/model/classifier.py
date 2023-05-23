import numpy as np
import tensorflow as tf


class KeyPointClassifier(object):
    def __init__(
        self,
        model_path='slr/model/slr_model.tflite',
        num_threads=1,
    ):
        #: Initializing tensor interpreter
        self.interpreter = tf.lite.Interpreter(
            model_path=model_path,
            num_threads=num_threads
        )
        self.interpreter.allocate_tensors()

        #: Input Output details
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def __call__(self, landmark_list):

        input_details_tensor_index = self.input_details[0]['index']

        #: Feeding landmarks to the tensor interpreter
        self.interpreter.set_tensor(
            input_details_tensor_index,
            np.array([landmark_list], dtype=np.float32)
        )

        #: Invoking interpreter for prediction
        self.interpreter.invoke()

        #: Getting tensor index from output details
        output_details_tensor_index = self.output_details[0]['index']
        # print(output_details_tensor_index)

        #: Getting all the prediction percentage
        result = self.interpreter.get_tensor(output_details_tensor_index)
        
        if max(np.squeeze(result)) > 0.5:
            #: Getting index of maximum accurate label
            result_index = np.argmax(np.squeeze(result))
            
            return result_index
        else:
            return 25
            
