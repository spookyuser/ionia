<p align="center">
 <img width=100 src="static/favicon/favicon.ico">
</p>
<p align="center">
  <h1 align="center">ionia</h1>
    <p align="center">so i had this idea...</p>
</p>

## what
a website i think i would like to use

<img width="1122" alt="image" src="https://user-images.githubusercontent.com/16196262/196995513-a2dc5ad9-10b6-48a0-87a9-0a9e3a320668.png"> 

^^ This is what it used to look like, was supposed to be like if reddit and twitter had a baby

## how
using Django, I tried in node but I realised I was slowly rebuilding Django 

## prerequisites 
-   [Python(3.7)](https://www.python.org/) is installed
-   [Pipenv](https://pipenv.readthedocs.io/en/latest/) is installed

## installing
1.  clone the repo  
2.  `$ cd ionia`  
3.  `$ pipenv install`  

## running
To run locally all you need is:

```bash
pipenv shell
python manage.py runserver
```

## deploying
at the moment, ionia is deployed using heroku for the webserver and s3 for storing avatars, to deploy it in the current state you need a heroku dyno with postgres, memcache (for cachalot) and redis (for session storage), you'll also need an s3 bucket for the avatars

## versioning
semver

## authors
[spookyUnknownUser](https://github.com/spookyUnknownUser)
