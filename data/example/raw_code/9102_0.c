ulong get_table_grant ( THD * thd , TABLE_LIST * table ) {
 ulong privilege ;
 Security_context * sctx = thd -> security_ctx ;
 const char * db = table -> db ? table -> db : thd -> db ;
 GRANT_TABLE * grant_table ;
 rw_rdlock ( & LOCK_grant ) ;
 # ifdef EMBEDDED_LIBRARY grant_table = NULL ;
 # else grant_table = table_hash_search ( sctx -> host , sctx -> ip , db , sctx -> priv_user , table -> table_name , 0 ) ;
 # endif table -> grant . grant_table = grant_table ;
 table -> grant . version = grant_version ;
 if ( grant_table ) table -> grant . privilege |= grant_table -> privs ;
 privilege = table -> grant . privilege ;
 rw_unlock ( & LOCK_grant ) ;
 return privilege ;
 }