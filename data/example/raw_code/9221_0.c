static const char * cmd_rule_engine ( cmd_parms * cmd , void * _dcfg , const char * p1 ) {
 directory_config * dcfg = ( directory_config * ) _dcfg ;
 if ( dcfg == NULL ) return NULL ;
 if ( strcasecmp ( p1 , "on" ) == 0 ) dcfg -> is_enabled = MODSEC_ENABLED ;
 else if ( strcasecmp ( p1 , "off" ) == 0 ) dcfg -> is_enabled = MODSEC_DISABLED ;
 else if ( strcasecmp ( p1 , "detectiononly" ) == 0 ) {
 dcfg -> is_enabled = MODSEC_DETECTION_ONLY ;
 dcfg -> of_limit_action = RESPONSE_BODY_LIMIT_ACTION_PARTIAL ;
 dcfg -> if_limit_action = REQUEST_BODY_LIMIT_ACTION_PARTIAL ;
 }
 else return apr_psprintf ( cmd -> pool , "ModSecurity: Invalid value for SecRuleEngine: %s" , p1 ) ;
 return NULL ;
 }