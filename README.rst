pyum
====

Why do we need this?
--------------------

Why do we need this when there are perfectly good 'yum' and 'rpm' python
packages?

Simple really: they don't work on systems without yum or rpm (eg.
debian, osx).

I had a need to manipulate and/or extract data from rpms and yum
repositories to manage rpms, but wasn't neccesarily running a
fedora/rhel/centos system. So I build a platform agnostic system to help
me.

Where is it at?
---------------

I have another project (yum2s3)[https://github.com/drewsonne/yum2s3]
which was the driving factor behind building this library. For this
reason, the functionality in this library is driven primary by the needs
of that project.

Can I help?
-----------

Please do! I've done my best to make this a test driven project, so if
you can improve my tests; please do. If you can write new tests; please
do. If you can expand functionality after writing tests; please do. But
please, write tests. For the most part I'm not fussy about branching and
such with pull requests. But please write some tests. In conclusion,
tests.
