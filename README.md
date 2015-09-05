# Minimal Docker Python setup
A demo of a minimal Nginx-uWSGI-Flask stack using Docker. 

![Image showing size of both containers.][docker_images]

## Quickstart
Create an image with Nginx from the tarred filesystem:
	
```shell
user@host $ docker import - orangetux/nginx < nginx/rootfs.tar
```

Now build the other images and run them by using `docker-compose`:

```shell
user@host $ docker-compose up
```

And head over `http://localhost:1337` and you should see an IP address.

## uWSGI and Flask
uWSGI and the Flask app are running from a custom image based on
[advancedclimatesystems/python:2.7.10][python_image]. The Dockerfile for this
image can be found [here][dockerfile_app]. See 
'Installing C extensions' for more information about how 
`uWSGI` is installed.

## Nginx
Nginx runs from an image which is based on a small filesystem. This filesystem
is build with [Buildroot][buildroot]. You can build the filesystem using the
supplied [defconfig][docker_nginx_defconfig].

## Installing C extensions

### Wheel
Installation of Python dependencies is done in 2 steps. First the dependency is
build. Compiling a C extension is one of the steps during this stage. After
building the depedency is installed. This step isn't do much more than copying
files produced by the build phase to their correct location.

The Python image doesn't contain a C compiler. For pure Python dependencies
this is not a problem, but C extensions can't be build inside the image. These
depencies must be build on the host before they can be installed inside image.

Dependencies can be build using [Wheel][wheel]: a built-package format for
Python. All required wheels are supplied and can be found at
[app/wheelhouse][wheelhouse], but if you want to build the wheels yourself run
the following command. It requires pip, wheel and setuptools >= 0.8.0.

```shell
user@host $ pip wheel --wheel-dir wheelhouse flask uwsgi
```
Installing depedencies from wheels is now simple:

```shell
root@container # pip install --find-links wheelhouse flask uwsgi
```

### Shared libraries
`uWSGI` relies on a few shared libraries which are not all available in the
image. They need to be added. If you run `uWSGI` without supplying all
missing shared libraries you'll see see something like this:

```shell
root@container # uwsgi
uwsgi: error while loading shared libraries: libpcre.so.3: cannot open shared object file: No such file or directory
```

If you add this library to the Docker image and run `uwsgi` you'll find out
that another depedency is missing. The following shared libraries must be added
before `uWSGI` is able to run:

* liblzma.so.5  
* libpcre.so.3  
* libxml2.so.2

These libraries are included in the repository and located at
[app/shared_libs][shared_libs]. But they can be copied from any x86_64 machine
to `/lib/` in the image. To locate them, use `ldd`:

```shell
user@host $ ldd uwsgi | grep -e lzma -e xml -e pcre
libpcre.so.3 => /lib/x86_64-linux-gnu/libpcre.so.3 (0x00007f2ad8b91000)
libxml2.so.2 => /usr/lib/x86_64-linux-gnu/libxml2.so.2 (0x00007f2ad81d7000)
liblzma.so.5 => /lib/x86_64-linux-gnu/liblzma.so.5 (0x00007f2ad72ed000)
```

## License
This software is licensed under the [MIT license][license].

© 2015 Auke Willem Oosterhoff

[buildroot]: https://github.com/AdvancedClimateSystems/docker-buildroot
[dockerfile_app]: https://github.com/OrangeTux/minimal-docker-python-setup/blob/master/app/Dockerfile
[docker_images]: docker_images.png "Size of images."
[docker_nginx_defconfig]: nginx/docker_nginx_defconfig
[license]: LICENSE
[python_image]: https://hub.docker.com/r/advancedclimatesystems/python/
[shared_libs]: app/shared_libs
[wheel]:http://wheel.readthedocs.org/en/latest/
[wheelhouse]: app/wheelhouse
