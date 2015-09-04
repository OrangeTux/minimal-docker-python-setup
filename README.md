# Minimal Docker Python setup
A demo of a minimal Nginx-uWSGI-Flask stack using Docker. Checkout the size:

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

## License
This software is licensed under the [MIT license][license].

© 2015 Auke Willem Oosterhoff

[license]: LICENSE
[docker_images]: docker_images.png "Size of images."
