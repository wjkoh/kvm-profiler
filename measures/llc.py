import oprofile_wrapper

def get(guest):
    guest.op_data.refs = oprofile_wrapper.get_measure( guest, "LLC_REFS")
    guest.op_data.misses = oprofile_wrapper.get_measure( guest, "LLC_MISSES")

    res = {}
    
    res[ "LLC_REFS" ] = guest.op_data.refs
    res[ "LLC_MISSES" ] = guest.op_data.misses

    return res