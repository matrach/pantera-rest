A simple dockerized and REST-ized version of PANTERA Morphosyntactic Tagger for Polish
=====

Pantera homepage can be found [here](http://zil.ipipan.waw.pl/PANTERA) and sources [here](https://github.com/accek/pantera-tagger). I am not associated with IPIPAN in any way.

Usage
====

Run
```bash
docker-compose up
```
to build the image and start REST-ful service on localhost:5001. See the code or tests for documentation...


You can access pantera from outside by just running:
```bash
$ ./pantera
```
To tag a file, simply run `./pantera file.txt`.

If you want anything advanced, try mounting a directory and using interactive mode:
```bash
$ docker run -it -v $PWD:/data matrach/pantera bash
```
