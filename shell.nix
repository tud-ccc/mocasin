with import <nixpkgs> {};

stdenv.mkDerivation {

  name = "pykpn";
  buildInputs = [ 
    python3Full
    python37Packages.virtualenvwrapper
    freetype
    libpng
    libxml2
    libxslt
    python37Packages.numpy
    cmake
    gcc
    gfortran
    readline
    python37Packages.pip
    python37Packages.pkgconfig
    liblapack
    openblas
    tk
    python37Packages.tkinter
    python37Packages.cvxopt
 ];

  src = null;
  
  shellHook = ''
  SOURCE_DATE_EPOCH=$(date +%s)

  #export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${R}/lib/R/lib:${readline}/lib

  #alias pip="PIP_PREFIX='$(pwd)/_build/pip_packages' \pip"

  #export PYTHONPATH="$(pwd)/_build/pip_packages/lib/python3.7/site-packages:$PYTHONPATH"
  '';
}
