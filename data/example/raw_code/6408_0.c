static void pdo_stmt_iter_get_data ( zend_object_iterator * iter , zval * * * data TSRMLS_DC ) {
 struct php_pdo_iterator * I = ( struct php_pdo_iterator * ) iter -> data ;
 if ( ! I -> fetch_ahead ) {
 * data = NULL ;
 return ;
 }
 * data = & I -> fetch_ahead ;
 }