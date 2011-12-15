# KVM Profiler
KVM Profiler is a profiler for [Kernel-based Virtual Machine (KVM)](http://www.linux-kvm.org).

# Usage
    $ python .
    Profiling and writing to database

    $ web/manage.py runserver 0.0.0.0:3000
    Serving Web front-end UI

You need to ensure that your username is added to the groups: kvm and libvirtd.

    $ sudo adduser `id -un` kvm
    Adding user '<username>' to group 'kvm' ...
    $ sudo adduser `id -un` libvirtd
    Adding user '<username>' to group 'libvirtd' ...

# Demo Videos
<object width="560" height="315"><param name="movie" value="http://www.youtube.com/v/P1cmw0tE0BU?version=3&amp;hl=en_US&amp;rel=0&amp;hd=1"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="http://www.youtube.com/v/P1cmw0tE0BU?version=3&amp;hl=en_US&amp;rel=0&amp;hd=1" type="application/x-shockwave-flash" width="560" height="315" allowscriptaccess="always" allowfullscreen="true"></embed></object>

# Dependencies
1. [python-libvirt](http://packages.ubuntu.com/search?keywords=python-libvirt)
1. [lxml](http://pypi.python.org/pypi/lxml)
1. [psutil](http://pypi.python.org/pypi/psutil)
1. [numpy](http://numpy.scipy.org/)
1. [matplotlib](http://matplotlib.sourceforge.net/)
1. [django](http://www.djangoproject.com/)

## Guest tools
1. [psutil](http://pypi.python.org/pypi/psutil)

# Authors
* Charles Hyun <tokki7@gmail.com>
* Jeehoon Kang <windmorning@gmail.com>
* Woojong Koh  <wjngkoh@gmail.com>
