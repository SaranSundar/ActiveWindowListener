cd react-ui
echo 'Building React App...'
npm run build
if [ $? -ne 0 ]; then
  echo "npm build in react-ui failed"
  exit 1
fi
cd ..
echo 'Cleaning up old builds...'
rm -rf dist
rm -rf templates
rm -rf static
mkdir templates
cp -r react-ui/build/index.html templates/index.html
cp -r react-ui/build/static static/
echo 'Building exe...'
pyinstaller -w -F --hidden-import='pkg_resources.py2_warn' --hidden-import='pynput' --add-data "templates;templates" --add-data "static;static" --add-data 'icons/*.png;static/icons' -y flair.py
echo "Flair.exe created. Navigate to dist/ and double click flair.exe or run ./flair.exe in git-bash to launch the application. May take a couple seconds to launch"
rm -rf *.spec
