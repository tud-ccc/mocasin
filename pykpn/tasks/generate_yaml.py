# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

import hydra
import os
import re

from pykpn.util.logging import getLogger


@hydra.main(config_path='conf/generate_yaml.yaml')
def generate_yaml(cfg):
    logger = getLogger('generate_yaml')

    dir_path = cfg['directory']
    template_path = cfg['template_path']
    hooks = cfg['hooks']

    #create output directory and copy template
    try:
        os.mkdir('../../../' + dir_path)
        template = open(os.getcwd() + '/../../../' + template_path, 'r')
        default_yaml = open(os.getcwd() + '/../../../' + dir_path + '/default.yaml', 'x')
        for line in template:
            default_yaml.write(line)
        template.close()
        default_yaml.close()
    except FileNotFoundError:
        logger.error('Error creating output directory!')

    try:
        default_yaml = open(os.getcwd() + '/../../../' + dir_path + '/default.yaml', 'r')
        lines_to_write = default_yaml.readlines()

    except FileNotFoundError:
        logger.error('Directory does not contain a yaml template!')
        return

    hook_dict = {}

    for hook in hooks.split(' '):
        hook_key = hook.split(':')[0]
        hook_value = hook.split(':')[1].split(',')

        if len(hook_value) > 1:
            #in case we're dealing with concrete values
            hook_dict.update( {hook_key : hook_value} )
        else:
            try:

                if hook_value[0] == 'all':
                    block_start = None

                    for line in lines_to_write:
                        if line.split(':')[0] == hook_key.split('.')[0]:
                            block_start = lines_to_write.index(line) + 1
                            break

                    directory = re.compile(r'\s+directory:\s(?P<path>.*)\n')
                    escape_sequence = re.compile(r'.*:\s*.\n')
                    path = None

                    for index in range(block_start, len(lines_to_write)):
                        line = lines_to_write[index]

                        match = directory.fullmatch(line)

                        if match:
                            path = match.group('path')
                            break

                        match = escape_sequence.fullmatch(line)
                        if match:
                            break

                    if path is not None:

                        for __, __, files in os.walk(path):

                            for file_name in files:

                                if hook_key not in hook_dict:
                                    hook_dict.update({hook_key : [file_name]})

                                else:
                                    hook_dict[hook_key].append(file_name)



                else:
                    #in case a number have been given
                    hook_dict.update( {hook_key : [int(hook_value[0])]} )

            except ValueError:
                #in case we're dealing with a single concrete value
                hook_dict.update( {hook_key : hook_value} )


    #generate different configs
    configs = []

    for key in hook_dict:

        if not configs:

            for value in hook_dict[key]:
                configs.append(["{0}:    {1}".format(key, value)])

        else:
            new_config = []
            while configs:
                to_add = configs.pop()

                for value in hook_dict[key]:
                    to_append = ["{0}:    {1}".format(key, value)]
                    for element in to_add:
                        to_append.append(element)
                    new_config.append(to_append)

            configs = new_config

    #generate a yaml for each config
    for i in range(0, len(configs)):
        file = open(os.getcwd() + '/../../../' + dir_path + '/config_{0}.yaml'.format(i), 'x')
        current_config = configs[i]

        current_conf_dict = {}

        for pair in current_config:
            keys = pair.split(':')[0]
            outer_key = keys.split('.')[0]
            inner_key = keys.split('.')[1]
            value = pair.split(':')[1]

            outer_regex = re.compile(re.escape(outer_key) + r':\s*\n')
            inner_regex = re.compile(r'\s+' + re.escape(inner_key) + r':\s+.*\n')

            if outer_regex not in current_conf_dict:
                current_conf_dict.update({outer_regex : {inner_regex : value}})
            else:
                current_conf_dict[outer_regex].update({inner_regex : value})

        in_outer_block = True
        current_block_key = None

        for line in lines_to_write:

            if in_outer_block:
                file.write(line)
                for key in current_conf_dict:
                    match = key.fullmatch(line)

                    if match:
                        in_outer_block = False
                        current_block_key = key
                        break


            else:
                for key in current_conf_dict[current_block_key]:
                    match = key.fullmatch(line)

                    if match:
                        current_inner_key = key
                        break

                if not match:
                    file.write(line)
                else:
                    new_line = line.split(':')[0] + ':' + current_conf_dict[current_block_key][key] + '\n'
                    file.write(new_line)
                    current_conf_dict[current_block_key].pop(current_inner_key)

                    if not current_conf_dict[current_block_key]:
                        in_outer_block = True
    default_yaml.close()
