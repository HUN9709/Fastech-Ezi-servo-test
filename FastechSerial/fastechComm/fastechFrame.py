class FastechFrame:
    FRAME_GETSLAVEINFO              = 0x01
    FRAME_GETMOTORINFO              = 0x05
    #FRAME_GETFIRMWAREINFO          = 0x07
    FRAME_FAS_SAVEALLPARAM          = 0x10
    FRAME_FAS_GETROMPARAM           = 0x11
    FRAME_FAS_SETPARAMETER          = 0x12
    FRAME_FAS_GETPARAMETER          = 0x13
    FRAME_FAS_SETIO_OUTPUT          = 0x20
    FRAME_FAS_SETIO_INPUT           = 0x21
    FRAME_FAS_GETIO_INPUT           = 0x22
    FRAME_FAS_GETIO_OUTPUT          = 0x23
    FRAME_FAS_SET_IO_ASSGN_MAP      = 0x24
    FRAME_FAS_GET_IO_ASSGN_MAP      = 0x25
    FRAME_FAS_IO_ASSGN_MAP_READROM  = 0x26
    FRAME_FAS_TRIGGER_OUTPUT        = 0x27
    FRAME_FAS_TRIGGER_STATUS        = 0x28
    FRAME_FAS_SERVOENABLE           = 0x2A
    FRAME_FAS_ALARMRESET            = 0x2B
    FRAME_FAS_STEPALARMRESET        = 0x2C
    FRAME_FAS_GETALARMTYPE          = 0x2E
    FRAME_FAS_MOVESTOP              = 0x31
    FRAME_FAS_EMERGENCYSTOP         = 0x32
    FRAME_FAS_MOVEORIGIN            = 0x33
    FRAME_FAS_MOVESINGLEABS         = 0x34
    FRAME_FAS_MOVESINGLEINC         = 0x35
    FRAME_FAS_MOVETOLIMIT           = 0x36
    FRAME_FAS_MOVEVELOCITY          = 0x37
    FRAME_FAS_POSABSOVERRIDE        = 0x38
    FRAME_FAS_POSINCOVERRIDE        = 0x39
    FRAME_FAS_VELOVERRIDE           = 0x3A
    FRAME_FAS_ALLMOVESTOP           = 0x3B
    FRAME_FAS_ALLEMERGENCYSTOP      = 0x3C
    FRAME_FAS_ALLMOVEORIGIN         = 0x3D
    FRAME_FAS_ALLMOVESINGLEABS      = 0x3E
    FRAME_FAS_ALLMOVESINGLEINC      = 0x3F
    FRAME_FAS_GETAXISSTATUS         = 0x40
    FRAME_FAS_GETIOAXISSTATUS       = 0x41
    FRAME_FAS_GETMOTIONSTATUS       = 0x42
    FRAME_FAS_GETALLSTATUS          = 0x43
    FRAME_FAS_SETCMDPOS             = 0x50
    FRAME_FAS_GETCMDPOS             = 0x51
    FRAME_FAS_SETACTPOS             = 0x52
    FRAME_FAS_GETACTPOS             = 0x53
    FRAME_FAS_GETPOSERR             = 0x54
    FRAME_FAS_GETACTVEL             = 0x55
    FRAME_FAS_CLEARPOS              = 0x56
    FRAME_FAS_POSTAB_READ_ITEM      = 0x60
    FRAME_FAS_POSTAB_WRITE_ITEM     = 0x61
    FRAME_FAS_POSTAB_READ_ROM       = 0x62
    FRAME_FAS_POSTAB_WRITE_ROM      = 0x63
    FRAME_FAS_POSTAB_RUN_ITEM       = 0x64
    FRAME_FAS_POSTAB_IS_DATA        = 0x65
    FRAME_FAS_POSTAB_RUN_ONEITEM    = 0x68
    FRAME_FAS_POSTAB_CHECK_STOPMODE = 0x69
    FRAME_FAS_POSTAB_READ_ONEITEM   = 0x6A
    FRAME_FAS_POSTAB_WRITE_ONEITEM  = 0x6B
    FRAME_FAS_POSTAB_IS_DATA_EX     = 0x6C
    FRAME_FAS_MOVEPUSH              = 0x78
    FRAME_FAS_GETPUSHSTATUS         = 0x79
                