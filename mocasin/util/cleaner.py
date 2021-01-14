import mocasin.tgff.tgffSimulation as tgff


def _cleanup():
    if tgff._parsed_tgff_files != {}:
        tgff._parsed_tgff_files = {}
