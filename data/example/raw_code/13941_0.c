static void option_error_reporter ( enum loglevel level , const char * format , ... ) {
 va_list args ;
 va_start ( args , format ) ;
 if ( level == ERROR_LEVEL || ! opt_bootstrap || global_system_variables . log_warnings ) {
 vprint_msg_to_log ( level , format , args ) ;
 }
 va_end ( args ) ;
 }