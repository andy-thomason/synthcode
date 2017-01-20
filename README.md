Synthcode
=========

This is a small project to compare tradtional C++ builds with single module builds.

It constructs a prgogram of arbitrary size which can then be compiled with CMake.

The python script has two parameters the first of which is "s" or "m" for single
or multimodule builds and the second is the number of classes that will be generated.

for example:

```
./synth.py s 1000
```

Generates a 1000 class single module build

```
./synth.py m 100
```

Generates a 100 class multi-module build

Having generated a build, build it with cmake:

```
mkdir rel
cmake -DCMAKE_BUILD_TYPE=Release ..
time make -j 8
```

or

```
mkdir debug
cmake -DCMAKE_BUILD_TYPE=Debug ..
time make -j 8
```

This enables you to compare the time required to make both kinds of build.

Note that we are giving the multimodule build a head start as it we are using -j 8
on the make command line which makes multimodule builds much faster.

However, if you perform this test, you will note that single module builds win by a factor
of 100 or more in most situations.

