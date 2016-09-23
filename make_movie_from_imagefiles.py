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
def get_spaceweather_imagefile_name(if_path, if_date, if_filename, \
        if_extension, verbose):
    """Returns a complete image filename string tailored to the spaceweather 
    site by concatenating the input image filename (if) strings that define the
    path, date, filename root, and the filename extension
    If verbose is truthy, then print the returned image filename string
    """
    sw_imagefile = if_path + if_date + "_" + if_filename + if_extension
    if verbose:
        print("Input image file full path: \n{}\n".format(sw_imagefile))
    return sw_imagefile

def open_spaceweather_imagefile(sw_imagefile):
    """Open spaceweather image given input string specifying full path to file.
    Return image object if successfull, or None if there is an OS error.
    """
    try: 
        img = Image.open(sw_imagefile)
    except OSError:
        img = None
        print("ERROR: Can't load image at {}\n".format(sw_imagefile))
    return img

def set_axis_if_no_image(ax, bgcolor='white'):
    """This function is used to set the axis properties in the event that an
    image file was not loaded correctly.  It currently clears the previous 
    image, blanks all image spines, turns off all tick marks, and removes all
    tick labels.  Finally, the optional background color parameter is used to 
    set the background facecolor.  
    This should allow one to print a message on the axis.
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
    ax.set_axis_bgcolor(bgcolor)

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
        'figure': { \
            'title': { \
                'string': "Sun images from spaceweather.com", \
                'space_from_axes_top': 0.1
            }, \
            'axes': { \
                'subplot2grid': [((1, 2), (0, 0)), ((1, 2), (0, 1))], \
                'title': ["Coronal Holes", "Sunspots"]
            }, \
            'savefig_kwargs': { \
                'facecolor': 'black', \
                'edgecolor': 'black'
            }, \
            'text': { \
                'color': 'white'
            }
        }, \
        'verbose': True
    }
 
    # Make figure and axes objects.  Add title to each axis, then turn off
    # axis tick marks, etc.
    fig = plt.figure()
    ax = []
    ax_title_pos = []
    ax_title_pos_ymax = (0, 0)
    ax_title_pos_aid = 0
    for aid, spg in enumerate(output_data['figure']['axes']['subplot2grid']):
        ax.append(plt.subplot2grid(spg[0], spg[1]))
        ax[aid].set_title( \
                output_data['figure']['axes']['title'][aid], \
                color=output_data['figure']['text']['color']
        )
        ax_title_pos.append(ax[aid].title.get_position())
        if ax_title_pos[aid][1] > ax_title_pos_ymax[1]:
            ax_title_pos_ymax = ax_title_pos[aid]
            ax_title_pos_aid = aid
        ax[aid].set_axis_off()
    # Find the axis title position closest to the top of the figure, in 
    # the figure coordinate system, which is used to set the figure title 
    disp_title_pos = ax[ax_title_pos_aid].transAxes.transform( \
            ax_title_pos_ymax
    )
    fig_title_y = fig.transFigure.inverted().transform(disp_title_pos)[1]
    print(ax_title_pos_aid)
    print(ax_title_pos_ymax)
    print(fig_title_y)

    # Create movie writer
    FFMpegWriter = manimation.writers['ffmpeg']
    #metadata = dict(title='Movie Test', artist='Matplotlib',
    #                       comment='Movie support!')
    writer = FFMpegWriter(fps=output_data['movie']['fps'], \
            bitrate=output_data['movie']['bitrate']
    )
    # Set up movie writer, loop through each image file opening each one, 
    # plot it in a figure window, and then save the figure as a movie frame
    with writer.saving(fig, output_data['movie']['filename'], \
            output_data['movie']['dpi']):
        for if_date in input_data['image']['file']['dates']:
            if 'title' in output_data['figure']:
                fig.suptitle( \
                        output_data['figure']['title']['string']+": "+if_date, \
                        x=0.5, y=fig_title_y+\
                        output_data['figure']['title']['space_from_axes_top'], \
                        fontsize=14, fontweight='bold', \
                        color=output_data['figure']['text']['color']
                )
            for if_id, if_name in enumerate(input_data['image']['file']['name']):
                sw_imagefile = get_spaceweather_imagefile_name( \
                        input_data['image']['path'], if_date, if_name, \
                        input_data['image']['file']['ext'], \
                        output_data['verbose']
                )
                # Open image file, then plot in specified axis
                img = open_spaceweather_imagefile(sw_imagefile)
                if img:
                    ax[if_id].imshow(img)
                else:
                    set_axis_if_no_image(ax[if_id], bgcolor= \
                        output_data['figure']['savefig_kwargs']['facecolor']
                    )
            # Store image as movie frame
            writer.grab_frame(**output_data['figure']['savefig_kwargs'])        
    #print(img)
