
Primeramente es necesario estar seguros que tenemos la version 2.7.(algo) dado que google app engine solo soporta hasta esta versión.

    $ /usr/bin/env python -V

luego hay  descargar el google app Engine Sdk file:

    $ wget https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.7.zip

despues de tener el SDK hay que descomprimirlo 

    $ unzip google_appengine_1.9.7.zip

Para correr la aplicacion tengo sobre la misma rama la carpeta de google app engine y la carpeta de mi app 


├── helloworld

│   ├── app.yaml

│   ├── helloworld.py

│   ├── index.yaml

│   └── README.md

├── google_appengine

│   └── (subcarpetas {son muchas})

con el siguiente comando en la terminal lo corro.

	$ google_appengine/dev_appserver.py helloworld/

-----------------------------------------------------------
