# pyum

[![Code Issues](https://www.quantifiedcode.com/api/v1/project/1de18b64180a4bdc8121ceeebb239868/badge.svg)](https://www.quantifiedcode.com/app/project/1de18b64180a4bdc8121ceeebb239868)

[![Build Status](https://travis-ci.org/drewsonne/pyum.svg?branch=master)](https://travis-ci.org/drewsonne/pyum)

[![codecov.io](https://codecov.io/github/drewsonne/pyum/coverage.svg?branch=master)](https://codecov.io/github/drewsonne/pyum?branch=master)

## Why do we need this?
Why do we need this when there are perfectly good 'yum' and 'rpm' python packages?

Simple really: they don't work on systems without yum or rpm (eg. debian, osx).

I had a need to manipulate and/or extract data from rpms and yum repositories to manage rpms, but wasn't neccesarily
running a fedora/rhel/centos system. Or even in AWS Lambda. Which would allow S3 buckets to be used as yum repos without needing an EC2 instance.

So I build a platform agnostic system to help me.

## Where is it at?
I have another project [yum2s3](https://github.com/drewsonne/yum2s3) which was the driving factor behind building this
library. For this reason, the functionality in this library is driven primary by the needs of that project.

## What does it look like?

<img src="https://github.com/drewsonne/pyum/blob/develop/diagrams/pyum.png?raw=true" width="234" height="400" />

![Class Diagram](/diagrams/pyum.png?raw=true "Class Diagram")


## Can I help?
Please do! I've done my best to make this a test driven project, so if you can improve my tests; please do. If you can
write new tests; please do. If you can expand functionality after writing tests; please do.
But please, write tests. 

For the time being I'm not fussy about branching and such with pull requests, as any help is appreciated.
My only request is that when you submit them, __create pull requests it to go into the develop branch__.

But please write some tests. In conclusion, tests.
