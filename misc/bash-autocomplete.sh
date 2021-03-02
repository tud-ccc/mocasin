# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andres Goens, Christian Menard

mocasin_bash_completion()
{
    words=($COMP_LINE)
    # we don't support autocomplete outside the mocasin entry point
    if [ "${words[0]}" != "mocasin" ]; then
        return
    fi

    # We can only autocomplete if the mocasin command is avalaiable
    if ! command -v mocasin &> /dev/null; then
        return
    fi

    # get all choices by running `mocasin autocomplete`
    choices=$(COMP_POINT=$COMP_POINT COMP_LINE=$COMP_LINE COMP_CWORD=$COMP_CWORD "mocasin" "autocomplete")

    # print debug information if requested
    if [ "$MOCASIN_COMP_DEBUG" == "1" ]; then
        printf "\n"
        printf "COMP_LINE='$COMP_LINE'\n"
        printf "COMP_POINT='$COMP_POINT'\n"
        printf "COMP_CWORD='$COMP_CWORD'\n"
        printf "Word='$word'\n"
        printf "Output suggestions:\n"
        printf "\t%s\n" ${choices[@]}
    fi

    # prepare a reply
    word=${words[$COMP_CWORD]}
    COMPREPLY=($( compgen -o nospace -o default -W "$choices" -- "$word" ));
}

COMP_WORDBREAKS=${COMP_WORDBREAKS//=}
COMP_WORDBREAKS=$COMP_WORDBREAKS complete -o nospace -o default -F mocasin_bash_completion mocasin
