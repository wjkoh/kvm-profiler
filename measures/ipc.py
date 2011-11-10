import oprofile_wrapper

def get(guest):
    inst_retired_old = guest.op_data.inst_retired
    guest.op_data.inst_retired = oprofile_wrapper.get_measure( guest, "INST_RETIRED", inst_retired_old )

    cpu_clk_unhalted_old = guest.op_data.cpu_clk_unhalted
    guest.op_data.cpu_clk_unhalted = oprofile_wrapper.get_measure( guest, "CPU_CLK_UNHALTED", cpu_clk_unhalted_old )
    
    res = {}

    if( ( guest.op_data.cpu_clk_unhalted - cpu_clk_unhalted_old ) > 0 ):
        res[ "IPC" ] = float( "%.2f" % ( float( guest.op_data.inst_retired - inst_retired_old ) / float( guest.op_data.cpu_clk_unhalted - cpu_clk_unhalted_old ) ) )
        res[ "INST_RETIRED" ] = ( guest.op_data.inst_retired - inst_retired_old )
        res[ "CPU_CLK_UNHALTED" ] = ( guest.op_data.cpu_clk_unhalted - cpu_clk_unhalted_old )
    else:
        res[ "IPC" ] = 0
        res[ "INST_RETIRED" ] = 0
        res[ "CPU_CLK_UNHALTED" ] = 0
    
    return res