cd react-ui
echo 'Building React App...'
npm run build
cd ..
echo 'Cleaning up old builds...'
rm -rf *.app
rm -rf ActiveWindowListener_Flair_exec
rm -rf dist
rm -rf templates
rm -rf static
mkdir templates
cp -r react-ui/build/index.html templates/index.html
cp -r react-ui/build/static static
echo 'Starting pip environment...'
pipenv run python setup.py py2app
cp -r dist/*.app ./ActiveWindowListener_Flair.app
rm *.spec
rm -rf build
rm -rf dist