# ImageClassification
Image Classification script in python using near exact matches.

## How it works
This script uses the imagehash lib and [this guide](https://realpython.com/blog/python/fingerprinting-images-for-near-duplicate-detection/) to fingerprint images, then compare the image library to itself, scanning for copies of the same picture.
Finally, it outputs a list of unique images.
