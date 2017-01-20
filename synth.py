#!/usr/bin/python

import sys
import random

random.seed(1)

if len(sys.argv) < 3:
  print("usage: synth.py s|m num_classes")
  sys,exit(1)

single_module = sys.argv[1] == 's'
numclasses = int(sys.argv[2])

if single_module:
  cxx = ""
else:
  cxx = " ".join(["c%d" % i for i in range(numclasses)])

with open("CMakeLists.txt", "wb") as f:
  f.write("""
cmake_minimum_required (VERSION 2.6)
project(synthcode)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14")
add_executable(synthcode main.cpp %s)
""" % cxx)


for i in range(numclasses):
  with open("c%d.hpp" % i, "wb") as f:
    f.write("#ifndef INCLUDED_C%d_HPP_\n" % i);
    f.write("#define INCLUDED_C%d_HPP_\n" % i);

    f.write('#include <vector>\n');
    f.write('#include <iostream>\n');
    f.write('#include <algorithm>\n');
    f.write('#include <cstdint>\n');
    f.write('#include <future>\n');

    used = []
    if i != 0:
      for z in range(5):
        j = random.randrange(100)
        if j < 20:
          c = random.randrange(i)
          if not c in used:
            used.append(c)
        

    for c in used:
      f.write('#include "c%d.hpp"\n' % c); 


    f.write("""
class c%d {
public:
  c%d() {
  }
""" % (i, i))

    if single_module:
      f.write("  void f1() {\n")
      for c in used:
        f.write("   i%d_.f1();\n" % c); 
      f.write("  }\n")
    else:
      f.write("  void f1();\n")

    f.write("private:\n")

    for c in used:
      f.write(" c%d i%d_;\n" % (c,c)); 
    
    f.write("};\n")
    f.write("#endif\n")

  if not single_module:
    with open("c%d.cpp" % i, "wb") as f:
      f.write('#include "c%d.hpp"\n' % i)
      f.write("void c%d::f1() {\n" % i);
      for c in used:
        f.write(" i%d_.f1();\n" % c); 
      f.write("}\n")

      


with open("main.cpp", "wb") as f:
  for i in range(numclasses):
    f.write('#include "c%d.hpp"\n' % i)

  f.write("""

class everything {
public:
  everything() {
""")

  for i in range(numclasses):
    f.write('    i%d_.f1();\n' % (i))
  f.write("""
  };
private:
""")

  for i in range(numclasses):
    f.write('  c%d i%d_;\n' % (i,i))
  

  f.write("""
};

int main() {
  std::cout << "size=" << sizeof(everything) << "\\n";
  everything *p = new everything{};
}

""")

