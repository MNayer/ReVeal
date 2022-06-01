static gboolean copy_move_directory ( CopyMoveJob * copy_job , GFile * src , GFile * * dest , gboolean same_fs , gboolean create_dest , char * * parent_dest_fs_type , SourceInfo * source_info , TransferInfo * transfer_info , GHashTable * debuting_files , gboolean * skipped_file , gboolean readonly_source_fs ) {
 GFileInfo * info ;
 GError * error ;
 GFile * src_file ;
 GFileEnumerator * enumerator ;
 char * primary , * secondary , * details ;
 char * dest_fs_type ;
 int response ;
 gboolean skip_error ;
 gboolean local_skipped_file ;
 CommonJob * job ;
 GFileCopyFlags flags ;
 job = ( CommonJob * ) copy_job ;
 if ( create_dest ) {
 switch ( create_dest_dir ( job , src , dest , same_fs , parent_dest_fs_type ) ) {
 case CREATE_DEST_DIR_RETRY : {
 return FALSE ;
 }
 case CREATE_DEST_DIR_FAILED : {
 * skipped_file = TRUE ;
 return TRUE ;
 }
 case CREATE_DEST_DIR_SUCCESS : default : {
 }
 break ;
 }
 if ( debuting_files ) {
 g_hash_table_replace ( debuting_files , g_object_ref ( * dest ) , GINT_TO_POINTER ( TRUE ) ) ;
 }
 }
 local_skipped_file = FALSE ;
 dest_fs_type = NULL ;
 skip_error = should_skip_readdir_error ( job , src ) ;
 retry : error = NULL ;
 enumerator = g_file_enumerate_children ( src , G_FILE_ATTRIBUTE_STANDARD_NAME , G_FILE_QUERY_INFO_NOFOLLOW_SYMLINKS , job -> cancellable , & error ) ;
 if ( enumerator ) {
 error = NULL ;
 while ( ! job_aborted ( job ) && ( info = g_file_enumerator_next_file ( enumerator , job -> cancellable , skip_error ? NULL : & error ) ) != NULL ) {
 src_file = g_file_get_child ( src , g_file_info_get_name ( info ) ) ;
 copy_move_file ( copy_job , src_file , * dest , same_fs , FALSE , & dest_fs_type , source_info , transfer_info , NULL , NULL , FALSE , & local_skipped_file , readonly_source_fs ) ;
 if ( local_skipped_file ) {
 transfer_add_file_to_count ( src_file , job , transfer_info ) ;
 report_copy_progress ( copy_job , source_info , transfer_info ) ;
 }
 g_object_unref ( src_file ) ;
 g_object_unref ( info ) ;
 }
 g_file_enumerator_close ( enumerator , job -> cancellable , NULL ) ;
 g_object_unref ( enumerator ) ;
 if ( error && IS_IO_ERROR ( error , CANCELLED ) ) {
 g_error_free ( error ) ;
 }
 else if ( error ) {
 if ( copy_job -> is_move ) {
 primary = f ( _ ( "Error while moving." ) ) ;
 }
 else {
 primary = f ( _ ( "Error while copying." ) ) ;
 }
 details = NULL ;
 if ( IS_IO_ERROR ( error , PERMISSION_DENIED ) ) {
 secondary = f ( _ ( "Files in the folder “%B” cannot be copied because you do " "not have permissions to see them." ) , src ) ;
 }
 else {
 secondary = f ( _ ( "There was an error getting information about the files in the folder “%B”." ) , src ) ;
 details = error -> message ;
 }
 response = run_warning ( job , primary , secondary , details , FALSE , CANCEL , _ ( "_Skip files" ) , NULL ) ;
 g_error_free ( error ) ;
 if ( response == 0 || response == GTK_RESPONSE_DELETE_EVENT ) {
 abort_job ( job ) ;
 }
 else if ( response == 1 ) {
 local_skipped_file = TRUE ;
 }
 else {
 g_assert_not_reached ( ) ;
 }
 }
 transfer_info -> num_files ++ ;
 report_copy_progress ( copy_job , source_info , transfer_info ) ;
 if ( debuting_files ) {
 g_hash_table_replace ( debuting_files , g_object_ref ( * dest ) , GINT_TO_POINTER ( create_dest ) ) ;
 }
 }
 else if ( IS_IO_ERROR ( error , CANCELLED ) ) {
 g_error_free ( error ) ;
 }
 else {
 if ( copy_job -> is_move ) {
 primary = f ( _ ( "Error while moving." ) ) ;
 }
 else {
 primary = f ( _ ( "Error while copying." ) ) ;
 }
 details = NULL ;
 if ( IS_IO_ERROR ( error , PERMISSION_DENIED ) ) {
 secondary = f ( _ ( "The folder “%B” cannot be copied because you do not have " "permissions to read it." ) , src ) ;
 }
 else {
 secondary = f ( _ ( "There was an error reading the folder “%B”." ) , src ) ;
 details = error -> message ;
 }
 response = run_warning ( job , primary , secondary , details , FALSE , CANCEL , SKIP , RETRY , NULL ) ;
 g_error_free ( error ) ;
 if ( response == 0 || response == GTK_RESPONSE_DELETE_EVENT ) {
 abort_job ( job ) ;
 }
 else if ( response == 1 ) {
 local_skipped_file = TRUE ;
 }
 else if ( response == 2 ) {
 goto retry ;
 }
 else {
 g_assert_not_reached ( ) ;
 }
 }
 if ( create_dest ) {
 flags = ( readonly_source_fs ) ? G_FILE_COPY_NOFOLLOW_SYMLINKS | G_FILE_COPY_TARGET_DEFAULT_PERMS : G_FILE_COPY_NOFOLLOW_SYMLINKS ;
 g_file_copy_attributes ( src , * dest , flags , job -> cancellable , NULL ) ;
 }
 if ( ! job_aborted ( job ) && copy_job -> is_move && ! local_skipped_file ) {
 if ( ! g_file_delete ( src , job -> cancellable , & error ) ) {
 if ( job -> skip_all_error ) {
 goto skip ;
 }
 primary = f ( _ ( "Error while moving “%B”." ) , src ) ;
 secondary = f ( _ ( "Could not remove the source folder." ) ) ;
 details = error -> message ;
 response = run_cancel_or_skip_warning ( job , primary , secondary , details , source_info -> num_files , source_info -> num_files - transfer_info -> num_files ) ;
 if ( response == 0 || response == GTK_RESPONSE_DELETE_EVENT ) {
 abort_job ( job ) ;
 }
 else if ( response == 1 ) {
 job -> skip_all_error = TRUE ;
 local_skipped_file = TRUE ;
 }
 else if ( response == 2 ) {
 local_skipped_file = TRUE ;
 }
 else {
 g_assert_not_reached ( ) ;
 }
 skip : g_error_free ( error ) ;
 }
 }
 if ( local_skipped_file ) {
 * skipped_file = TRUE ;
 }
 g_free ( dest_fs_type ) ;
 return TRUE ;
 }