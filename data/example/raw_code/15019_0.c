static void test_bug9159 ( ) {
 MYSQL_STMT * stmt ;
 int rc ;
 const char * stmt_text = "select a, b from t1" ;
 const unsigned long type = CURSOR_TYPE_READ_ONLY ;
 myheader ( "test_bug9159" ) ;
 mysql_query ( mysql , "drop table if exists t1" ) ;
 mysql_query ( mysql , "create table t1 (a int not null primary key, b int)" ) ;
 rc = mysql_query ( mysql , "insert into t1 values (1,1)" ) ;
 myquery ( rc ) ;
 stmt = mysql_stmt_init ( mysql ) ;
 mysql_stmt_prepare ( stmt , stmt_text , strlen ( stmt_text ) ) ;
 mysql_stmt_attr_set ( stmt , STMT_ATTR_CURSOR_TYPE , ( const void * ) & type ) ;
 mysql_stmt_execute ( stmt ) ;
 mysql_stmt_close ( stmt ) ;
 rc = mysql_query ( mysql , "drop table if exists t1" ) ;
 myquery ( rc ) ;
 }