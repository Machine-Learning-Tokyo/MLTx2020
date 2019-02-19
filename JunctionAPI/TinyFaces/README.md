# Tiny Face Detector in TensorFlow

 A TensorFlow port(inference only) of Tiny Face Detector from [authors' MatConvNet codes](https://github.com/peiyunh/tiny)[1].

# Usage
## Converting a pretrained model

`matconvnet_hr101_to_pickle` reads weights of the MatConvNet pretrained model and
write back to a pickle file which is used in a TensorFlow model as initial weights.

1. Download a [ResNet101-based pretrained model(hr_res101.mat)](https://www.cs.cmu.edu/%7Epeiyunh/tiny/hr_res101.mat)
from the authors' repo.

2. Convert the model to a pickle file by:
```
python matconvnet_hr101_to_pickle.py
        --matlab_model_path /path/to/pretrained_model
        --weight_file_path  ./tinyface_tf/tf.pkl
```
3. Don't forget to change the model path in "tiny_face_det.py" file (L:34)

# Examples
### selfie with many people
This is the same image as one in [the authors' repo](https://github.com/peiyunh/tiny)[1].

![selfie](https://github.com/cydonia999/Tiny_Faces_in_Tensorflow/blob/master/images/selfie.jpg?raw=true)

[Original image](https://github.com/peiyunh/tiny/blob/master/data/demo/selfie.jpg)
