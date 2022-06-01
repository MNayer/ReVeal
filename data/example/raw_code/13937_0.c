static bool read_init_file ( char * file_name ) {
 MYSQL_FILE * file ;
 DBUG_ENTER ( "read_init_file" ) ;
 DBUG_PRINT ( "enter" , ( "name: %s" , file_name ) ) ;
 if ( ! ( file = mysql_file_fopen ( key_file_init , file_name , O_RDONLY , MYF ( MY_WME ) ) ) ) DBUG_RETURN ( TRUE ) ;
 bootstrap ( file ) ;
 mysql_file_fclose ( file , MYF ( MY_WME ) ) ;
 DBUG_RETURN ( FALSE ) ;
 }