static __always_inline __u16 __swab16p ( const __u16 * p ) {
 # ifdef __arch_swab16p return __arch_swab16p ( p ) ;
 # else return __swab16 ( * p ) ;
 # endif }