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

    choices=$(COMP_POINT=$COMP_POINT COMP_LINE=$COMP_LINE COMP_CWORD=$COMP_CWORD "mocasin" "autocomplete")
    word=${words[$COMP_CWORD]}

    if [ "$MOCASIN_COMP_DEBUG" == "1" ]; then
        printf "\n"
        printf "COMP_LINE='$COMP_LINE'\n"
        printf "COMP_POINT='$COMP_POINT'\n"
        printf "COMP_CWORD='$COMP_CWORD'\n"
        printf "Word='$word'\n"
        printf "Output suggestions:\n"
        printf "\t%s\n" ${choices[@]}
    fi

    COMPREPLY=($( compgen -o nospace -o default -W "$choices" -- "$word" ));
}

COMP_WORDBREAKS=${COMP_WORDBREAKS//=}
COMP_WORDBREAKS=$COMP_WORDBREAKS complete -o nospace -o default -F mocasin_bash_completion mocasin
