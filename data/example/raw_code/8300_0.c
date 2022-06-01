PHP_MINIT_FUNCTION ( uwsgi_php_minit ) {
 php_session_register_module ( & ps_mod_uwsgi ) ;
 struct uwsgi_string_list * usl = uphp . constants ;
 while ( usl ) {
 char * equal = strchr ( usl -> value , '=' ) ;
 if ( equal ) {
 size_t name_len = equal - usl -> value ;
 char * name = usl -> value ;
 char * strval = equal + 1 ;
 equal = NULL ;
 # ifndef UWSGI_PHP7 name_len = name_len + 1 ;
 # endif zend_register_string_constant ( name , name_len , strval , CONST_CS | CONST_PERSISTENT , module_number TSRMLS_CC ) ;
 }
 usl = usl -> next ;
 }
 return SUCCESS ;
 }