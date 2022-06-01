int psf_ftruncate ( SF_PRIVATE * psf , sf_count_t len ) {
 int retval ;
 if ( len < 0 ) return - 1 ;
 if ( ( sizeof ( off_t ) < sizeof ( sf_count_t ) ) && len > 0x7FFFFFFF ) return - 1 ;
 retval = ftruncate ( psf -> file . filedes , len ) ;
 if ( retval == - 1 ) psf_log_syserr ( psf , errno ) ;
 return retval ;
 }