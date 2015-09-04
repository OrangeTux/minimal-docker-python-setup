# Minimal Docker Python setup
A demo of a minimal Nginx-uWSGI-Flask stack using Docker. 

![Image showing size of both containers.][docker_images]

## Quickstart
Create an image from the tarred filesystem:
	
```shell
$ docker import - orangetux/nginx < nginx/rootfs.tar
```

Now build the other images and run them by using `docker-compose`:

```shell
$ docker-compose up
```

And head over `http://localhost:1337`.

## uWSGI and Flask
uWSGI and the Flask app are running from a custom image based on
[advancedclimatesystems/python:2.7.10][python_image]. The Dockerfile for this
image can be found [here][dockerfile_app]. 

## Installing C-extensions
Installation of Python dependencies is done in 2 steps. First the dependency is
build. Compiling a C extension is one of the steps during this stage. After
building the depedency is installed. This step isn't do much more than copying
files produced by the build phase to their correct location.

The Python image doesn't contain a C compiler. For pure Python dependencies
this is not a problem, but C extensions can't be build inside the image. These
depencies must be build on the host before they can be installed inside image.

Dependencies can be build using [Wheel][wheel]: a built-package format for
Python. All required wheels are supplied, but if you want to build the wheels
yourself run the following command. It requires pip, wheel and setuptools >=
0.8.0.

```shell
$ pip wheel --wheel-dir wheelhouse flask uwsgi
```
Installing depedencies from wheels is now simple:

```shell
$ pip install --find-links wheelhouse flask uwsgi
```

## License
This software is licensed under the [MIT license][license].

© 2015 Auke Willem Oosterhoff

[license]: LICENSE
[python_image]: https://hub.docker.com/r/advancedclimatesystems/python/
[dockerfile_app]: https://github.com/OrangeTux/minimal-docker-python-setup/blob/master/app/Dockerfile
[wheel]:http://wheel.readthedocs.org/en/latest/
[docker_images]: docker_images.png "Size of images."
