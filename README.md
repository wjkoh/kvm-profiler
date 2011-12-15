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
* [KVM Profiler Demo Video](http://www.youtube.com/watch?v=P1cmw0tE0BU)
* [Case 1: High-High](http://www.youtube.com/watch?v=rByf6voRBSw)
* [Case 1: Low-Idle](http://www.youtube.com/watch?v=nw1chsnDC1g)
* [Case 2: High-Idle](http://www.youtube.com/watch?v=FwvZAngpanI)
* [Case 2: High-Low](http://www.youtube.com/watch?v=1r4XB7tTIeM)

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
