# Bar Chart Race of Baseball League Japan
  This is the source code for creating a bar chart race animation of Baseball League Japan.  

## Example  
  [![Simple Charts / Baseball League Japan 1950-2022](https://img.youtube.com/vi/7UU6xZYmsRE/0.jpg)](https://www.youtube.com/watch?v=7UU6xZYmsRE "Simple Charts / Baseball League Japan 1950-2022")  

## Data Source
  日本プロ野球記録   
  https://2689web.com/games.html

## Setup  
  1. install Anaconda3-2020.02  
      https://repo.anaconda.com/archive/Anaconda3-2020.02-Windows-x86_64.exe
  2. install FFmpeg   
     https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip   
     download, unzip, and add "C:{folder path}\ffmpeg-master-latest-win64-gpl\bin" to the PATH environment variable.
  3. create virtual environment and install packages  
      conda create -n bca python==3.7.6 anaconda  
      conda activate bca  
      conda install -c conda-forge opencv==3.4.1  

## Usage  
  Send the following commands in virtual environment of python  
  &nbsp;&nbsp;&nbsp;&nbsp; cd {folder path}  
  &nbsp;&nbsp;&nbsp;&nbsp; python 1_get_data.py  
  &nbsp;&nbsp;&nbsp;&nbsp; python 2_preprocess.py   
  &nbsp;&nbsp;&nbsp;&nbsp; python 3_BarChartRaceBaseballJapan.py   
  &nbsp;&nbsp;&nbsp;&nbsp; python 4_create_video.py   
