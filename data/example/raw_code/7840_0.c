static int switch_character_set_results ( MYSQL * mysql , const char * cs_name ) {
 char query_buffer [ QUERY_LENGTH ] ;
 size_t query_length ;
 if ( ! server_supports_switching_charsets ) return FALSE ;
 query_length = my_snprintf ( query_buffer , sizeof ( query_buffer ) , "SET SESSION character_set_results = '%s'" , ( const char * ) cs_name ) ;
 return mysql_real_query ( mysql , query_buffer , query_length ) ;
 }