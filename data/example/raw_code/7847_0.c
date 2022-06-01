static void print_xml_tag ( FILE * xml_file , const char * sbeg , const char * line_end , const char * tag_name , const char * first_attribute_name , ... ) {
 va_list arg_list ;
 const char * attribute_name , * attribute_value ;
 fputs ( sbeg , xml_file ) ;
 fputc ( '<' , xml_file ) ;
 fputs ( tag_name , xml_file ) ;
 va_start ( arg_list , first_attribute_name ) ;
 attribute_name = first_attribute_name ;
 while ( attribute_name != NullS ) {
 attribute_value = va_arg ( arg_list , char * ) ;
 DBUG_ASSERT ( attribute_value != NullS ) ;
 fputc ( ' ' , xml_file ) ;
 fputs ( attribute_name , xml_file ) ;
 fputc ( '\"' , xml_file ) ;
 print_quoted_xml ( xml_file , attribute_value , strlen ( attribute_value ) , 0 ) ;
 fputc ( '\"' , xml_file ) ;
 attribute_name = va_arg ( arg_list , char * ) ;
 }
 va_end ( arg_list ) ;
 fputc ( '>' , xml_file ) ;
 fputs ( line_end , xml_file ) ;
 check_io ( xml_file ) ;
 }