VALUE rb_dlhandle_enable_close ( VALUE self ) {
 struct dl_handle * dlhandle ;
 Data_Get_Struct ( self , struct dl_handle , dlhandle ) ;
 dlhandle -> enable_close = 1 ;
 return Qnil ;
 }