void usage_exit ( ) {
 int i ;
 fprintf ( stderr , "Usage: %s <options> -o dst_filename src_filename \n" , exec_name ) ;
 fprintf ( stderr , "\nOptions:\n" ) ;
 arg_show_usage ( stderr , main_args ) ;
 fprintf ( stderr , "\nEncoder Global Options:\n" ) ;
 arg_show_usage ( stderr , global_args ) ;
 fprintf ( stderr , "\nRate Control Options:\n" ) ;
 arg_show_usage ( stderr , rc_args ) ;
 fprintf ( stderr , "\nTwopass Rate Control Options:\n" ) ;
 arg_show_usage ( stderr , rc_twopass_args ) ;
 fprintf ( stderr , "\nKeyframe Placement Options:\n" ) ;
 arg_show_usage ( stderr , kf_args ) ;
 # if CONFIG_VP8_ENCODER fprintf ( stderr , "\nVP8 Specific Options:\n" ) ;
 arg_show_usage ( stderr , vp8_args ) ;
 # endif # if CONFIG_VP9_ENCODER fprintf ( stderr , "\nVP9 Specific Options:\n" ) ;
 arg_show_usage ( stderr , vp9_args ) ;
 # endif fprintf ( stderr , "\nStream timebase (--timebase):\n" " The desired precision of timestamps in the output, expressed\n" " in fractional seconds. Default is 1/1000.\n" ) ;
 fprintf ( stderr , "\nIncluded encoders:\n\n" ) ;
 for ( i = 0 ;
 i < get_vpx_encoder_count ( ) ;
 ++ i ) {
 const VpxInterface * const encoder = get_vpx_encoder_by_index ( i ) ;
 fprintf ( stderr , " %-6s - %s\n" , encoder -> name , vpx_codec_iface_name ( encoder -> codec_interface ( ) ) ) ;
 }
 exit ( EXIT_FAILURE ) ;
 }