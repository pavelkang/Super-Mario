#! /usr/bin/env python

# Super Mario.pyw
# All code and assets created by Chen Liuli

import sys
import os
if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
sys.path.append(os.path.join('src'))
try:
    libdir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
    sys.path.insert(0, libdir)
except:
    pass

import main
if __name__ == '__main__':
    main.main()   
