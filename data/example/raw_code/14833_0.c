static void gst_asf_demux_check_segment_ts ( GstASFDemux * demux , GstClockTime payload_ts ) {
 if ( G_UNLIKELY ( ! GST_CLOCK_TIME_IS_VALID ( demux -> segment_ts ) && GST_CLOCK_TIME_IS_VALID ( demux -> first_ts ) ) ) {
 GST_DEBUG_OBJECT ( demux , "segment ts: %" GST_TIME_FORMAT , GST_TIME_ARGS ( demux -> first_ts ) ) ;
 demux -> segment_ts = payload_ts ;
 if ( demux -> streaming ) gst_segment_do_seek ( & demux -> segment , demux -> in_segment . rate , GST_FORMAT_TIME , ( GstSeekFlags ) demux -> segment . flags , GST_SEEK_TYPE_SET , demux -> segment_ts , GST_SEEK_TYPE_NONE , 0 , NULL ) ;
 }
 }