#!/bin/bash

OPTIND=1
TARGET=""
SPACE="----------------------------------------------------------"
GREETER="Starting Python virtual environment. Press CTRL-D to exit."

show_help() {
    echo ""
    echo "Usage: pykpn_env.sh -t <path/to/local/python_env>"
    echo "-h Show help message"
    echo "-t Specify target for virtual Python installation"
}

install_packages() {
    echo Install virtualenv to: ${TARGET}
    mkdir -p ${TARGET}
    virtualenv --python=python3 ${TARGET}
    $SHELL --init-file <(echo ". \"$HOME/.bashrc\"; 
                     source ${TARGET}/bin/activate; 
                     pip3 install -r requirements; 
                     echo $SPACE; 
                     echo $GREETER")
    
    #enter virtualenv manually
    #export VIRTUAL_ENV=$1
    #export PATH=${TARGET}/bin:$PATH
    #unset PYTHON_HOME
    #pip3 install -r requirements
    #$SHELL
}


while getopts ":ht:" opt; do
    case "$opt" in
    h|\?)
        show_help
        exit 0
        ;;
    t)  TARGET=$OPTARG
        install_packages
        exit 0
        ;;
    :)
       echo "Argument required"
       show_help
       exit 1
       ;;
    esac
done

if [[ -z $TARGET ]]
then 
     echo "Option required"
     show_help
     exit 1
fi

shift $((OPTIND-1))

[ "$1" = "--" ] && shift
