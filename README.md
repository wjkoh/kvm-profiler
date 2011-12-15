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
<iframe width="1280" height="720" src="http://www.youtube.com/embed/videoseries?list=PL74358EE18BC4C358&amp;hl=en_US&amp;hd=1" frameborder="0" allowfullscreen></iframe>

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
