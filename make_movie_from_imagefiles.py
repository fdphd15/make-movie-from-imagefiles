#!/usr/bin/python3
# Code name: make_movie_from_imagefiles.py 
# Brief Description: Simple code to make a movie from an input set of image
# files and save it to file
# NOTE: this script requires the following external package(s):
# ffmpeg (see https://ffmpeg.org/download.html)
# For example, install using homebrew: brew install ffmpeg
# Code References:
# Use of matplotlib.animation to write movie follows example at
# http://matplotlib.org/examples/animation/moviewriter.html
# Created on: September 6, 2016
# Written by: Frederick D. Pearce
# Code version: 0.1 on 09/06/2016 - Original version used to setup github repo

# Copyright 2016 Frederick D. Pearce

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0

## I) Import modules, all available via pip install
# NOTE: Agg backend used for mac os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
from PIL import Image

## II) Define functions
def get_spaceweather_imagefile(if_path, if_date, if_filename, if_extension, \
        verbose):
    """Returns a complete image filename string tailored to the spaceweather 
    site by concatenating the input image filename (if) strings that define the
    path, date, filename root, and the filename extension
    If verbose is truthy, then print the returned image filename string
    """
    sw_imagefile = if_path + if_date + "_" + if_filename + if_extension
    if verbose:
        print("Input image file full path: \n{}\n".format(sw_imagefile))
    return sw_imagefile

def load_spaceweather_imagefile(sw_imagefile):
    """Load spaceweather image given input string specifying full path to file.
    Return image object if successfull, or None if there is an OS error.
    """
    try: 
        img = Image.open(sw_imagefile)
    except OSError:
        img = None
        print("ERROR: Can't load image at {}\n".format(sw_imagefile))
    return img

def set_axis_if_no_image(ax):
    """This function is used to set the axis properties in the event that an
    image file was not loaded correctly.  It currently clears the previous 
    image, blanks all image spines, turns off all tick marks, and removes all
    tick labels.  One should still be able to print a message on the axis.
    """
    ax.clear()
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.set_xticklabels([])
    ax.set_yticklabels([])

## III) If this file is run from command line, execute script below
if __name__ == "__main__":
    ## Run script
    # Input Parameters
    input_data = { \
        'image': { \
            'source': "http://spaceweather.com/images2016/", \
            'path': \
                "/Users/frederickpearce/Documents/PythonProjects/make_movie_from_imagefiles/sun_images/", \
            'file': { \
                'dates': [ \
                        "12aug16", "13aug16", "14aug16", "15aug16", \
                        "16aug16", "17aug16", "18aug16", "19aug16", \
                        "20aug16", "21aug16", "22aug16", "23aug16", \
                        "24aug16", "25aug16", "26aug16", "27aug16", \
                        "28aug16", "29aug16", "30aug16", "31aug16"
                ], \
                'name': ["coronalhole", "sunspot"], \
                'ext': ".jpg"
            }
        }
    }
    output_data = { \
        'movie': { \
            'filename': "make_movie_test_br5000.mp4", \
            'fps': 1, \
            'bitrate': 5000, \
            'dpi': 300
        }, \
        'figure': {
            'title': "Sun images from spaceweather.com", \
            'axes': { \
                'subplot2grid': [((1, 2), (0, 0)), ((1, 2), (0, 1))], \
                'title': ["Coronal Holes", "Sunspots"]
            }
        }, \
        'verbose': True
    }

    # Create movie writer
    FFMpegWriter = manimation.writers['ffmpeg']
    #metadata = dict(title='Movie Test', artist='Matplotlib',
    #                       comment='Movie support!')
    writer = FFMpegWriter(fps=output_data['movie']['fps'], \
            bitrate=output_data['movie']['bitrate']
    )
    
    # Make figure and axes objects
    fig = plt.figure()
    ax = []
    for aid, spg in enumerate(output_data['figure']['axes']['subplot2grid']):
        ax.append(plt.subplot2grid(spg[0], spg[1]))
    
    # Set up movie writer, then loop through each image file, load it into 
    # memory, plot it in a figure window, and then save the figure as a movie 
    # frame
    with writer.saving(fig, output_data['movie']['filename'], \
            output_data['movie']['dpi']):
        for if_date in input_data['image']['file']['dates']:
            if 'title' in output_data['figure']:
                fig.suptitle( \
                        output_data['figure']['title']+": "+if_date, \
                        x=0.5, y=0.85, fontsize=14, fontweight='bold'
                )
            for if_id, if_name in enumerate(input_data['image']['file']['name']):
                sw_imagefile = get_spaceweather_imagefile( \
                        input_data['image']['path'], if_date, if_name, \
                        input_data['image']['file']['ext'], \
                        output_data['verbose']
                )
                # Load image file
                img = load_spaceweather_imagefile(sw_imagefile)
                #Image.open(sw_imagefile)
                # Plot image in appropriate subplot2grid axis with axis ticks,
                # etc. turned off
                ax[if_id].set_axis_off()
                if img:
                    ax[if_id].imshow(img)
                else:
                    set_axis_if_no_image(ax[if_id])
                    #ax[if_id].clear()
                    #ax[if_id].spines['right'].set_color('none')
                    #ax[if_id].spines['left'].set_color('none')
                    #ax[if_id].yaxis.set_ticks_position('none')
                    #ax[if_id].set_yticklabels([])
                ax[if_id].set_title( \
                        output_data['figure']['axes']['title'][if_id]
                )
                #plt.show()
                # Store image as movie frame
            writer.grab_frame()
