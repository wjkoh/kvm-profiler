import oprofile_wrapper

def get(guest):
    guest.op_data.inst_retired = oprofile_wrapper.get_measure( guest, "INST_RETIRED")
    guest.op_data.cpu_clk_unhalted = oprofile_wrapper.get_measure( guest, "CPU_CLK_UNHALTED")
    
    res = {}

    if( guest.op_data.cpu_clk_unhalted > 0 ):
        res[ "IPC" ] = float( "%.2f" % ( float( guest.op_data.inst_retired ) / float( guest.op_data.cpu_clk_unhalted ) ) )
        res[ "INST_RETIRED" ] = ( guest.op_data.inst_retired )
        res[ "CPU_CLK_UNHALTED" ] = ( guest.op_data.cpu_clk_unhalted )
    else:
        res[ "IPC" ] = 0
        res[ "INST_RETIRED" ] = 0
        res[ "CPU_CLK_UNHALTED" ] = 0
    
    return res