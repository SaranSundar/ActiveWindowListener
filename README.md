# ActiveWindowListener

## Requirements

1. Must be using Windows 10 and have Python 3.7 installed
2. Make sure no other python version is installed on system, must only contain `Python 3.7`
    * Make Sure Python is properly added to the user and system variables path
        * User Path - `C:\Python37, C:\Python37\Scripts`
        * System Path - `C:\Python37, C:\Python37\Scripts`
        
3. This project uses the Flair framework, so read through all documentation [here](https://flair-1.gitbook.io/flair/) for installing the pre-req python packages
4. This project also uses several other dependencies such as MongoDB, and GraphViz, so install the [Mongo server](https://www.mongodb.com/download-center/community) and [GraphViz](https://graphviz.gitlab.io/_pages/Download/Download_windows.html) choose the msi option
    * Make sure Mongo is added to User path as well
        * User Path - C:\Program Files\MongoDB\Server\4.2\bin
    * Make sure GraphViz path is in both User and System path
        * User Path - C:\Program Files (x86)\Graphviz2.38\bin
        * System Path - C:\Program Files (x86)\Graphviz2.38\bin
        
5. Clone this repo https://github.com/SaranSundar/ActiveWindowListener
6. Navigate into it and run `rm -rf dist/ build/`
    * Navigate into react-ui and run `npm install` and then navigate back
7. Make sure you install all the pip modules listed in `setup.py` under `OPTIONS.packages` such as
```
'packages': ['flask', 'werkzeug', 'jinja2', 'gevent', 'geventwebsocket', 'flask_cors', 'pynput', 'pymongo', 'graphviz', 'pymongo', 'Pillow', 'pynput']
```
8. Then try building the exe by running `sh create_windows_exe.sh`
9. You can then navigate into the `dist/flair` folder and run `./fair.exe` in git bash if the previous step said the exe was built successfully
10. Once the build command was run you can also run `flair.py` from the root of the project to debug any errors
11. Optionally you can also run `app.py` on its own, and then npm start in the react-ui folder to test the backend and front end separately without having to compile them together into a exe
