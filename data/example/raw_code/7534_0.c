int get_next_bit ( REP_SET * set , uint lastpos ) {
 uint pos , * start , * end , bits ;
 start = set -> bits + ( ( lastpos + 1 ) / WORD_BIT ) ;
 end = set -> bits + set -> size_of_bits ;
 bits = start [ 0 ] & ~ ( ( 1 << ( ( lastpos + 1 ) % WORD_BIT ) ) - 1 ) ;
 while ( ! bits && ++ start < end ) bits = start [ 0 ] ;
 if ( ! bits ) return 0 ;
 pos = ( uint ) ( start - set -> bits ) * WORD_BIT ;
 while ( ! ( bits & 1 ) ) {
 bits >>= 1 ;
 pos ++ ;
 }
 return pos ;
 }