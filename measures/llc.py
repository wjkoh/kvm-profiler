import oprofile_wrapper

def get(guest):
    refs_old = guest.op_data.refs
    guest.op_data.refs = oprofile_wrapper.get_measure( guest, "LLC_REFS", refs_old )

    misses_old = guest.op_data.misses
    guest.op_data.misses = oprofile_wrapper.get_measure( guest, "LLC_MISSES", misses_old )

    res = {}
    
    res[ "LLC_REFS" ] = guest.op_data.refs - refs_old
    res[ "LLC_MISSES" ] = guest.op_data.misses - misses_old

    return res