# KVM Profiler
KVM Profiler is a profiler for [Kernel-based Virtual Machine (KVM)](http://www.linux-kvm.org).

# Usage
    $ python .

You need to ensure that your username is added to the groups: kvm and libvirtd.

    $ sudo adduser `id -un` kvm
    Adding user '<username>' to group 'kvm' ...
    $ sudo adduser `id -un` libvirtd
    Adding user '<username>' to group 'libvirtd' ...

# Dependencies
1. [python-libvirt](http://packages.ubuntu.com/search?keywords=python-libvirt)
1. [LXML](http://pypi.python.org/pypi/lxml)
1. [PSUtil](http://pypi.python.org/pypi/psutil)
1. [RRDtool](http://oss.oetiker.ch/rrdtool/)
1. [PyRRD](http://pypi.python.org/pypi/PyRRD)
1. [SQLAlchemy](http://www.sqlalchemy.org/)

# Authors
* Charles Hyun <tokki7@gmail.com>
* Jeehoon Kang <windmorning@gmail.com>
* Woojong Koh  <wjngkoh@gmail.com>
