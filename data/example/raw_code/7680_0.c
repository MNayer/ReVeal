int table2myisam ( TABLE * table_arg , MI_KEYDEF * * keydef_out , MI_COLUMNDEF * * recinfo_out , uint * records_out ) {
 uint i , j , recpos , minpos , fieldpos , temp_length , length ;
 enum ha_base_keytype type = HA_KEYTYPE_BINARY ;
 uchar * record ;
 KEY * pos ;
 MI_KEYDEF * keydef ;
 MI_COLUMNDEF * recinfo , * recinfo_pos ;
 HA_KEYSEG * keyseg ;
 TABLE_SHARE * share = table_arg -> s ;
 uint options = share -> db_options_in_use ;
 DBUG_ENTER ( "table2myisam" ) ;
 if ( ! ( my_multi_malloc ( MYF ( MY_WME ) , recinfo_out , ( share -> fields * 2 + 2 ) * sizeof ( MI_COLUMNDEF ) , keydef_out , share -> keys * sizeof ( MI_KEYDEF ) , & keyseg , ( share -> key_parts + share -> keys ) * sizeof ( HA_KEYSEG ) , NullS ) ) ) DBUG_RETURN ( HA_ERR_OUT_OF_MEM ) ;
 keydef = * keydef_out ;
 recinfo = * recinfo_out ;
 pos = table_arg -> key_info ;
 for ( i = 0 ;
 i < share -> keys ;
 i ++ , pos ++ ) {
 keydef [ i ] . flag = ( ( uint16 ) pos -> flags & ( HA_NOSAME | HA_FULLTEXT | HA_SPATIAL ) ) ;
 keydef [ i ] . key_alg = pos -> algorithm == HA_KEY_ALG_UNDEF ? ( pos -> flags & HA_SPATIAL ? HA_KEY_ALG_RTREE : HA_KEY_ALG_BTREE ) : pos -> algorithm ;
 keydef [ i ] . block_length = pos -> block_size ;
 keydef [ i ] . seg = keyseg ;
 keydef [ i ] . keysegs = pos -> key_parts ;
 for ( j = 0 ;
 j < pos -> key_parts ;
 j ++ ) {
 Field * field = pos -> key_part [ j ] . field ;
 type = field -> key_type ( ) ;
 keydef [ i ] . seg [ j ] . flag = pos -> key_part [ j ] . key_part_flag ;
 if ( options & HA_OPTION_PACK_KEYS || ( pos -> flags & ( HA_PACK_KEY | HA_BINARY_PACK_KEY | HA_SPACE_PACK_USED ) ) ) {
 if ( pos -> key_part [ j ] . length > 8 && ( type == HA_KEYTYPE_TEXT || type == HA_KEYTYPE_NUM || ( type == HA_KEYTYPE_BINARY && ! field -> zero_pack ( ) ) ) ) {
 if ( j == 0 ) keydef [ i ] . flag |= HA_PACK_KEY ;
 if ( ! ( field -> flags & ZEROFILL_FLAG ) && ( field -> type ( ) == MYSQL_TYPE_STRING || field -> type ( ) == MYSQL_TYPE_VAR_STRING || ( ( int ) ( pos -> key_part [ j ] . length - field -> decimals ( ) ) ) >= 4 ) ) keydef [ i ] . seg [ j ] . flag |= HA_SPACE_PACK ;
 }
 else if ( j == 0 && ( ! ( pos -> flags & HA_NOSAME ) || pos -> key_length > 16 ) ) keydef [ i ] . flag |= HA_BINARY_PACK_KEY ;
 }
 keydef [ i ] . seg [ j ] . type = ( int ) type ;
 keydef [ i ] . seg [ j ] . start = pos -> key_part [ j ] . offset ;
 keydef [ i ] . seg [ j ] . length = pos -> key_part [ j ] . length ;
 keydef [ i ] . seg [ j ] . bit_start = keydef [ i ] . seg [ j ] . bit_end = keydef [ i ] . seg [ j ] . bit_length = 0 ;
 keydef [ i ] . seg [ j ] . bit_pos = 0 ;
 keydef [ i ] . seg [ j ] . language = field -> charset_for_protocol ( ) -> number ;
 if ( field -> null_ptr ) {
 keydef [ i ] . seg [ j ] . null_bit = field -> null_bit ;
 keydef [ i ] . seg [ j ] . null_pos = ( uint ) ( field -> null_ptr - ( uchar * ) table_arg -> record [ 0 ] ) ;
 }
 else {
 keydef [ i ] . seg [ j ] . null_bit = 0 ;
 keydef [ i ] . seg [ j ] . null_pos = 0 ;
 }
 if ( field -> type ( ) == MYSQL_TYPE_BLOB || field -> type ( ) == MYSQL_TYPE_GEOMETRY ) {
 keydef [ i ] . seg [ j ] . flag |= HA_BLOB_PART ;
 keydef [ i ] . seg [ j ] . bit_start = ( uint ) ( field -> pack_length ( ) - share -> blob_ptr_size ) ;
 }
 else if ( field -> type ( ) == MYSQL_TYPE_BIT ) {
 keydef [ i ] . seg [ j ] . bit_length = ( ( Field_bit * ) field ) -> bit_len ;
 keydef [ i ] . seg [ j ] . bit_start = ( ( Field_bit * ) field ) -> bit_ofs ;
 keydef [ i ] . seg [ j ] . bit_pos = ( uint ) ( ( ( Field_bit * ) field ) -> bit_ptr - ( uchar * ) table_arg -> record [ 0 ] ) ;
 }
 }
 keyseg += pos -> key_parts ;
 }
 if ( table_arg -> found_next_number_field ) keydef [ share -> next_number_index ] . flag |= HA_AUTO_KEY ;
 record = table_arg -> record [ 0 ] ;
 recpos = 0 ;
 recinfo_pos = recinfo ;
 while ( recpos < ( uint ) share -> reclength ) {
 Field * * field , * found = 0 ;
 minpos = share -> reclength ;
 length = 0 ;
 for ( field = table_arg -> field ;
 * field ;
 field ++ ) {
 if ( ( fieldpos = ( * field ) -> offset ( record ) ) >= recpos && fieldpos <= minpos ) {
 if ( ! ( temp_length = ( * field ) -> pack_length_in_rec ( ) ) ) continue ;
 if ( ! found || fieldpos < minpos || ( fieldpos == minpos && temp_length < length ) ) {
 minpos = fieldpos ;
 found = * field ;
 length = temp_length ;
 }
 }
 }
 DBUG_PRINT ( "loop" , ( "found: 0x%lx recpos: %d minpos: %d length: %d" , ( long ) found , recpos , minpos , length ) ) ;
 if ( recpos != minpos ) {
 bzero ( ( char * ) recinfo_pos , sizeof ( * recinfo_pos ) ) ;
 recinfo_pos -> type = ( int ) FIELD_NORMAL ;
 recinfo_pos ++ -> length = ( uint16 ) ( minpos - recpos ) ;
 }
 if ( ! found ) break ;
 if ( found -> flags & BLOB_FLAG ) recinfo_pos -> type = ( int ) FIELD_BLOB ;
 else if ( found -> type ( ) == MYSQL_TYPE_VARCHAR ) recinfo_pos -> type = FIELD_VARCHAR ;
 else if ( ! ( options & HA_OPTION_PACK_RECORD ) ) recinfo_pos -> type = ( int ) FIELD_NORMAL ;
 else if ( found -> zero_pack ( ) ) recinfo_pos -> type = ( int ) FIELD_SKIP_ZERO ;
 else recinfo_pos -> type = ( int ) ( ( length <= 3 || ( found -> flags & ZEROFILL_FLAG ) ) ? FIELD_NORMAL : found -> type ( ) == MYSQL_TYPE_STRING || found -> type ( ) == MYSQL_TYPE_VAR_STRING ? FIELD_SKIP_ENDSPACE : FIELD_SKIP_PRESPACE ) ;
 if ( found -> null_ptr ) {
 recinfo_pos -> null_bit = found -> null_bit ;
 recinfo_pos -> null_pos = ( uint ) ( found -> null_ptr - ( uchar * ) table_arg -> record [ 0 ] ) ;
 }
 else {
 recinfo_pos -> null_bit = 0 ;
 recinfo_pos -> null_pos = 0 ;
 }
 ( recinfo_pos ++ ) -> length = ( uint16 ) length ;
 recpos = minpos + length ;
 DBUG_PRINT ( "loop" , ( "length: %d type: %d" , recinfo_pos [ - 1 ] . length , recinfo_pos [ - 1 ] . type ) ) ;
 }
 * records_out = ( uint ) ( recinfo_pos - recinfo ) ;
 DBUG_RETURN ( 0 ) ;
 }