static void test_fetch_tiny ( ) {
 int rc ;
 myheader ( "test_fetch_tiny" ) ;
 rc = mysql_query ( mysql , "DROP TABLE IF EXISTS test_bind_fetch" ) ;
 myquery ( rc ) ;
 rc = mysql_query ( mysql , "CREATE TABLE test_bind_fetch(c1 tinyint unsigned, \ c2 tinyint, \ c3 tinyint unsigned, \ c4 tinyint, \ c5 tinyint, \ c6 tinyint, \ c7 tinyint unsigned)" ) ;
 myquery ( rc ) ;
 bind_fetch ( 3 ) ;
 }