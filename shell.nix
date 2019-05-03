with import <nixpkgs> {};

stdenv.mkDerivation {

  name = "pykpn";
  buildInputs = [ 
    python3Full
    python36Packages.virtualenvwrapper
    freetype
    libpng
    libxml2
    libxslt
    python36Packages.numpy
    cmake
    gcc
    gfortran
    readline
    python36Packages.pip
    python36Packages.pkgconfig
    liblapack
    openblas
    tk
    python36Packages.tkinter
 ];

  src = null;
  
  shellHook = ''
  SOURCE_DATE_EPOCH=$(date +%s)

  #export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${R}/lib/R/lib:${readline}/lib

  #alias pip="PIP_PREFIX='$(pwd)/_build/pip_packages' \pip"

  #export PYTHONPATH="$(pwd)/_build/pip_packages/lib/python3.6/site-packages:$PYTHONPATH"
  '';
}
