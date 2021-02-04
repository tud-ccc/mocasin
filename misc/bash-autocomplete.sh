#What about copyright here?

export _HYDRA_OLD_COMP=$(complete -p mocasin 2> /dev/null)
hydra_bash_completion()
{
    MOCASIN_HOME=<path-to-your-mocasin-installation>
    words=($COMP_LINE)
        if [ "${words[0]}" != "mocasin" ]; then
	    #we don't support autocomplete outside the mocasin entry point
            return
	fi 
        if (( ${#words[@]} < 3 )); then
	    #here we should ask autocompletion for tasks
            return
        fi
        task=${words[1]}
        task_pyfile=$MOCASIN_HOME/tasks/${task}.py 
        grep "@hydra.main" $task_pyfile -q
        if [ ! -f "$task_pyfile" ]; then
            return
        fi
        helper="mocasin ${task}"
    EXECUTABLE=($(command -v $helper))
    if [ "$HYDRA_COMP_DEBUG" == "1" ]; then
        printf "EXECUTABLE_FIRST='${EXECUTABLE[0]}'\n"
    fi
    if ! [ -x "${EXECUTABLE[0]}" ]; then
        false
    fi
    COMP_LINE=${COMP_LINE/mocasin ${task}/mocasin} 

    if [ $? == 0 ]; then
        options=$( COMP_POINT=$COMP_POINT COMP_LINE=$COMP_LINE $helper -sc query=bash)
        word=${words[$COMP_CWORD]}

        if [ "$HYDRA_COMP_DEBUG" == "1" ]; then
            printf "\n"
            printf "COMP_LINE='$COMP_LINE'\n"
            printf "COMP_POINT='$COMP_POINT'\n"
            printf "Word='$word'\n"
            printf "Output suggestions:\n"
            printf "\t%s\n" ${options[@]}
        fi
        COMPREPLY=($( compgen -o nospace -o default -W '$options' -- "$word" ));
    fi
}

COMP_WORDBREAKS=${COMP_WORDBREAKS//=}
COMP_WORDBREAKS=$COMP_WORDBREAKS complete -o nospace -o default -F hydra_bash_completion mocasin

