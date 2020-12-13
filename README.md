# FocusDetection
Focus area detection in photographs


Focus Detection blah blah
Blur Detection works

## To install

This package only depends on numpy and opencv, to install them run, 

```
pip install -U -r requirements.txt

## To run


### run on a single image
python process.py -i input_image.png

### run on a directory of images
python process.py -i input_directory/ 

# or both! 
python process.py -i input_directory/ other_directory/ input_image.png
```

. In addition to logging whether an image is blurry or not, we can also,

```bash

This was inspired by:

This is based upon the blogpost [Blur Detection With Opencv](https://www.pyimagesearch.com/2015/09/07/blur-detection-with-opencv/) by Adrian Rosebrock.

![Focus Detection](https://raw.githubusercontent.com/WillBrennan/BlurDetection2/master/docs/demo.png)
