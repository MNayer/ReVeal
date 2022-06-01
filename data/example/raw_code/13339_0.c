static void activation_mountable_mounted ( NautilusFile * file , GFile * result_location , GError * error , gpointer callback_data ) {
 ActivateParameters * parameters = callback_data ;
 NautilusFile * target_file ;
 LaunchLocation * location ;
 parameters -> mountables = g_list_remove ( parameters -> mountables , file ) ;
 nautilus_file_unref ( file ) ;
 if ( error == NULL ) {
 target_file = nautilus_file_get ( result_location ) ;
 location = find_launch_location_for_file ( parameters -> locations , file ) ;
 if ( location ) {
 launch_location_update_from_file ( location , target_file ) ;
 }
 nautilus_file_unref ( target_file ) ;
 }
 else {
 if ( error -> domain != G_IO_ERROR || ( error -> code != G_IO_ERROR_FAILED_HANDLED && error -> code != G_IO_ERROR_ALREADY_MOUNTED ) ) {
 location = find_launch_location_for_file ( parameters -> locations , file ) ;
 if ( location ) {
 parameters -> locations = g_list_remove ( parameters -> locations , location ) ;
 launch_location_free ( location ) ;
 }
 }
 if ( error -> domain != G_IO_ERROR || ( error -> code != G_IO_ERROR_CANCELLED && error -> code != G_IO_ERROR_FAILED_HANDLED && error -> code != G_IO_ERROR_ALREADY_MOUNTED ) ) {
 eel_show_error_dialog ( _ ( "Unable to access location" ) , error -> message , parameters -> parent_window ) ;
 }
 if ( error -> code == G_IO_ERROR_CANCELLED ) {
 activation_parameters_free ( parameters ) ;
 return ;
 }
 }
 activation_mount_mountables ( parameters ) ;
 }