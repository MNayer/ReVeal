static void encode_picture_header ( VC2EncContext * s ) {
 avpriv_align_put_bits ( & s -> pb ) ;
 put_bits32 ( & s -> pb , s -> picture_number ++ ) ;
 }