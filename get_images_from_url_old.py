#!/usr/bin/python3
# Based on code posted in forum reply by Liquid_Fire on 11/27/11 from
# http://stackoverflow.com/questions/8286352/how-to-save-an-image-locally-
# using-python-whose-url-address-i-already-know
import urllib.request
# Input Parameters
input_data = { \
    'url': { \
        'address': "http://spaceweather.com/images2016/", \
        'folder': { \
            'date': { \
                'values': ["25aug16"], \
#        ["12aug16", "13aug16", "14aug16", "15aug16", "16aug16", \
#        "17aug16", "18aug16", "19aug16", "20aug16", "21aug16", \
#        "22aug16", "23aug16", "24aug16"], 
                'format': "%d%b%y"
            }
        }, \
        'file': { \
            'name': ["coronalhole_sdo_blank", "hmi1898"], \
            'ext': [".jpg", ".gif"]
        }
    }
}
output_data = { \
    'image': { \
        'path': \
            "/Users/frederickpearce/Documents/PythonProjects/SunImagesToMovie/", \
        'file': { \
            'name': ["coronalhole", "sunspot"], \
            'ext' = ".jpg"
        }
    }
    'verbose': True
}

# Download image file from image file at input_data['url']['address'] +
# input_data['url']['folder']['date']['values'] +
# input_data['url']['file']['name'] + 
# input_data['url']['file']['ext']
# Then, write image file to directory/filename defined by
# output_data['image']['path'] + output_data['image']['file']['name'] +
# output_data['image']['file']['ext']
# The ['file']['name'] list value in input_data MUST be the same length as 
# the ['file']['name'] list value in  output_data!!!
print("\nGetting image files from input URLs\n")
for inp_date in input_data['url']['date']['values']:
    for inp_fnind, inp_fname in enumerate(input_data['url']['file']['name']):
        input_url = input_data['url']['address'] + inp_date + "/" + \
                input_data['url']['file']['name'] + \
                input_data['url']['file']['ext']
        if output_data['verbose']:
            print("Input image file URL: \n{}".format(input_url))
        output_imagefile = output_data['image']['path'] + \
                "_".join((inp_date, \
                        output_data['image']['file']['name'][inp_fnind])) + \
                output_data['image']['file']['ext']
        if output_data['verbose']:
            print("Output image file path: \n{}\n".format(output_imagefile))
        urllib.request.urlretrieve(input_url, output_imagefile)
if output_data['verbose']:
    print("")

