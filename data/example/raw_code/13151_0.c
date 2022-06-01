static void run_shell ( char const * shell , char const * command , char * * additional_args , size_t n_additional_args ) {
 size_t n_args = 1 + fast_startup + 2 * ! ! command + n_additional_args + 1 ;
 char const * * args = xcalloc ( n_args , sizeof * args ) ;
 size_t argno = 1 ;
 if ( simulate_login ) {
 char * arg0 ;
 char * shell_basename ;
 shell_basename = basename ( shell ) ;
 arg0 = xmalloc ( strlen ( shell_basename ) + 2 ) ;
 arg0 [ 0 ] = '-' ;
 strcpy ( arg0 + 1 , shell_basename ) ;
 args [ 0 ] = arg0 ;
 }
 else args [ 0 ] = basename ( shell ) ;
 if ( fast_startup ) args [ argno ++ ] = "-f" ;
 if ( command ) {
 args [ argno ++ ] = "-c" ;
 args [ argno ++ ] = command ;
 }
 memcpy ( args + argno , additional_args , n_additional_args * sizeof * args ) ;
 args [ argno + n_additional_args ] = NULL ;
 execv ( shell , ( char * * ) args ) ;
 {
 int exit_status = ( errno == ENOENT ? EXIT_ENOENT : EXIT_CANNOT_INVOKE ) ;
 warn ( _ ( "failed to execute %s" ) , shell ) ;
 exit ( exit_status ) ;
 }
 }