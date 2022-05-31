static int sort_key_read ( MI_SORT_PARAM * sort_param , void * key ) {
 int error ;
 SORT_INFO * sort_info = sort_param -> sort_info ;
 MI_INFO * info = sort_info -> info ;
 DBUG_ENTER ( "sort_key_read" ) ;
 if ( ( error = sort_get_next_record ( sort_param ) ) ) DBUG_RETURN ( error ) ;
 if ( info -> state -> records == sort_info -> max_records ) {
 mi_check_print_error ( sort_info -> param , "Key %d - Found too many records;
 Can't continue" , sort_param -> key + 1 ) ;
 DBUG_RETURN ( 1 ) ;
 }
 sort_param -> real_key_length = ( info -> s -> rec_reflength + _mi_make_key ( info , sort_param -> key , ( uchar * ) key , sort_param -> record , sort_param -> filepos ) ) ;
 # ifdef HAVE_purify bzero ( key + sort_param -> real_key_length , ( sort_param -> key_length - sort_param -> real_key_length ) ) ;
 # endif DBUG_RETURN ( sort_write_record ( sort_param ) ) ;
 }