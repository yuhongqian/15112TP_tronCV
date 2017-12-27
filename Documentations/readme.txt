Project Description:
This project is a tron game controlled using openCV.

Main features:
    1. AI player (under Single Player mode)
    2. Multiple players controlling using openCV simultaneously.

How To Run the Project:
    Method 1: Run main.py using any Python IDE.
    Method 2: Using terminal, cd to the project folder. Enter:
              python3 main.py

Install needed libraries:

    The project requries python3, tkinter, openCV3, pygame.

    Mac Users:

        For Mac users, all the installations can be done in the terminal.

    1. Install openCV3:

    * Install Xcode:
    sudo xcode-select --install

    * Accept Xcode license:
    sudo xcodebuild -license

    * Install hoomebrew:
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

    * Install openCV:
    brew tap homebrew/science
    brew install opencv

    * Test:
    python3
    import cv2

    (A more detailed installation guide can be found here: https://www.pyimagesearch.com/2017/05/15/resolving-macos-opencv-homebrew-install-errors/)

    2. pygame (from pygame official website):

    * Create and add the following to ~/.bash_profile:
        # Homebrew binaries now take precedence over Apple defaults
        export PATH=/usr/local/bin:$PATH

    * Install Apple Xcode command line tools:
        xcode-select --install

    * Install XQuartz:
        http://xquartz.macosforge.org/landing/

    * Install homebrew (skip this if already installed):
        ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"

    * Install Python3 "proper" and packages we’ll need for installing PyGame from bitbucket:
        brew install python3 hg sdl sdl_image sdl_mixer sdl_ttf portmidi

    * Install PyGame:
        pip3 install hg+http://bitbucket.org/pygame/pygame

    * Restart the Mac for XQuartz changes


    Windows Users:

    1. OpenCV3:
    https://docs.opencv.org/3.2.0/d3/d52/tutorial_windows_install.html

    2. PyGame:
    https://www.pygame.org/wiki/GettingStarted#Pygame Installation

    Linux Users:

    1. OpenCV3:
    https://docs.opencv.org/3.2.0/d7/d9f/tutorial_linux_install.html

    2. PyGame:
    https://www.pygame.org/wiki/GettingStarted#Pygame Installation







