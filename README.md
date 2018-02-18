# webNovel2eBook
This Python script will download chapters from novels available on Qidan International aka webnovel.com and saves them into the .epub format.

## Getting Started

To run this script you'll need to have Python 3.6.1 install, which you can find [here](https://www.python.org/downloads/ "Python Download Link").

Additionally, you'll need PhantomJS, which you can find [here](http://phantomjs.org/download.html "PhantomJS Download Link").
After downloading PhantomJS extract the zip file and copy the executable from the bin folder into the folder the script is located in.

### Features

- Download and save you favorite Novels from webnovel.com into an ePub file.
- Automatically adds some metadata like author, title, series names and cover if available.
- Grabs the list of Novel as well as available chapters and metadata in real-time.

### Prerequisites

As mentioned before this script was written for Python version 3.6.1. It may work with other versions too but none are tested.
Also, you'll need selenium, beautifulsoup, and requests. Do get them just open a terminal, cd to the folder where the program is located and run:
```
pip install -r requirements.txt
```
or run:
```
pip install beautifulsoup4
pip install requests
pip install selenium
```
### Usage

Before running the script make sure you copied PhantomJS into the project folder. If you running something else then Windows, you'll need to change the name of the PhantomJS executable in webnovel2ebook.py on line 38.

Navigate to the folder using the console then write:

```
python webnovel2ebook.py
```

If you didn't add Python to the PATH variable during the installation or afterward then write

```
path/where/you/installed/python.exe webnovel2ebook.py
```

then you should see a list of categories. Enter a number to select a category which then gives you a list of Novels to choose from. And again enter a number to choose a novel.
Afterwards, the program will gather chapter information and metadata. When everything is finished it'll ask for the starting chapter and the end chapter. Just enter the chapters you want and hit enter.
Now it should download the chapters you wanted and will save them into an ePub file that is located in the folder the script is located in.

## Keep in mind!

Although the code works as far as I know there are a lot of small bugs that I have yet to fix. If you come across some of them feel free to let me know so I have a general idea what is still necessary to fix.

### ToDo list

- Chapter names sometimes are not displayed correctly
- The ePubs don't have a stylesheet (Fixed ✓)
- Some novels are not working

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

The base code for this script was provided by MrHaCkEr

## Want to support a poor student?

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/sramg)