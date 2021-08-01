# Rate My Professor extenssion

## Description
There are many such extensions in the wild, this one aims to work on all college websites.
It is directed to aid students to select the courses without much hassle of going to the Rate My Professor
website. Simply install the application and compare the teachers on your portal. No tab switching is needed.

## Deployment

### Setup your dataroot paths
```
python app/src/rmp/utils/general.py
```

### To start Flask server run the following (currently under construction):
```
cd web
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

### UI:
To launch React webpage:
`npm start`

To deploy as a web extension:
`npm run build`
This will dump all of the files into `build` folder

Open your browser of preference and go to the settings where you can import extensions.
Import the build folder by selecting any file.
