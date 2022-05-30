#!/usr/bin/env python
# coding: utf-8

# In[24]:


keywords = ["alignas", "alignof", "and", "and_eq", "asm", "atomic_cancel", "atomic_commit", 
            "atomic_noexcept", "auto", "bitand", "bitor", "bool", "break", "case", "catch", 
            "char", "char8_t", "char16_t", "char32_t", "class", "compl", "concept", "const", 
            "consteval", "constexpr", "constinit", "const_cast", "continue", "co_await", 
            "co_return", "co_yield", "decltype", "default", "delete", "do", "double", "dynamic_cast", 
            "else", "enum", "explicit", "export", "extern", "false", "float", "for", "friend", "goto", 
            "if", "inline", "int", "long", "mutable", "namespace", "new", "noexcept", "not", "not_eq", 
            "nullptr", "operator", "or", "or_eq", "private", "protected", "public", "reflexpr", 
            "register", "reinterpret_cast", "requires", "return", "short", "signed", "sizeof", "static", 
            "static_assert", "static_cast", "struct", "switch", "synchronized", "template", "this", 
            "thread_local", "throw", "true", "try", "typedef", "typeid", "typename", "union", "unsigned", 
            "using", "virtual", "void", "volatile", "wchar_t", "while", "xor", "xor_eq", "NULL"]
puncs = '~`!@#$%^&*()-+={[]}|\\;:\'\"<,>.?/'
puncs = list(puncs)

l_funcs = ['StrNCat', 'getaddrinfo', '_ui64toa', 'fclose', 'pthread_mutex_lock', 'gets_s', 'sleep', 
           '_ui64tot', 'freopen_s', '_ui64tow', 'send', 'lstrcat', 'HMAC_Update', '__fxstat', 'StrCatBuff', 
           '_mbscat', '_mbstok_s', '_cprintf_s', 'ldap_search_init_page', 'memmove_s', 'ctime_s', 'vswprintf', 
           'vswprintf_s', '_snwprintf', '_gmtime_s', '_tccpy', '*RC6*', '_mbslwr_s', 'random', 
           '__wcstof_internal', '_wcslwr_s', '_ctime32_s', 'wcsncat*', 'MD5_Init', '_ultoa', 
           'snprintf', 'memset', 'syslog', '_vsnprintf_s', 'HeapAlloc', 'pthread_mutex_destroy', 
           'ChangeWindowMessageFilter', '_ultot', 'crypt_r', '_strupr_s_l', 'LoadLibraryExA', '_strerror_s', 
           'LoadLibraryExW', 'wvsprintf', 'MoveFileEx', '_strdate_s', 'SHA1', 'sprintfW', 'StrCatNW', 
           '_scanf_s_l', 'pthread_attr_init', '_wtmpnam_s', 'snscanf', '_sprintf_s_l', 'dlopen', 
           'sprintfA', 'timed_mutex', 'OemToCharA', 'ldap_delete_ext', 'sethostid', 'popen', 'OemToCharW', 
           '_gettws', 'vfork', '_wcsnset_s_l', 'sendmsg', '_mbsncat', 'wvnsprintfA', 'HeapFree', '_wcserror_s', 
           'realloc', '_snprintf*', 'wcstok', '_strncat*', 'StrNCpy', '_wasctime_s', 'push*', '_lfind_s', 
           'CC_SHA512', 'ldap_compare_ext_s', 'wcscat_s', 'strdup', '_chsize_s', 'sprintf_s', 'CC_MD4_Init', 
           'wcsncpy', '_wfreopen_s', '_wcsupr_s', '_searchenv_s', 'ldap_modify_ext_s', '_wsplitpath', 
           'CC_SHA384_Final', 'MD2', 'RtlCopyMemory', 'lstrcatW', 'MD4', 'MD5', '_wcstok_s_l', '_vsnwprintf_s', 
           'ldap_modify_s', 'strerror', '_lsearch_s', '_mbsnbcat_s', '_wsplitpath_s', 'MD4_Update', '_mbccpy_s', 
           '_strncpy_s_l', '_snprintf_s', 'CC_SHA512_Init', 'fwscanf_s', '_snwprintf_s', 'CC_SHA1', 'swprintf', 
           'fprintf', 'EVP_DigestInit_ex', 'strlen', 'SHA1_Init', 'strncat', '_getws_s', 'CC_MD4_Final', 
           'wnsprintfW', 'lcong48', 'lrand48', 'write', 'HMAC_Init', '_wfopen_s', 'wmemchr', '_tmakepath', 
           'wnsprintfA', 'lstrcpynW', 'scanf_s', '_mbsncpy_s_l', '_localtime64_s', 'fstream.open', '_wmakepath', 
           'Connection.open', '_tccat', 'valloc', 'setgroups', 'unlink', 'fstream.put', 'wsprintfA', '*SHA1*', 
           '_wsearchenv_s', 'ualstrcpyA', 'CC_MD5_Update', 'strerror_s', 'HeapCreate', 'ualstrcpyW', '__xstat', 
           '_wmktemp_s', 'StrCatChainW', 'ldap_search_st', '_mbstowcs_s_l', 'ldap_modify_ext', '_mbsset_s', 
           'strncpy_s', 'move', 'execle', 'StrCat', 'xrealloc', 'wcsncpy_s', '_tcsncpy*', 'execlp', 
           'RIPEMD160_Final', 'ldap_search_s', 'EnterCriticalSection', '_wctomb_s_l', 'fwrite', '_gmtime64_s', 
           'sscanf_s', 'wcscat', '_strupr_s', 'wcrtomb_s', 'VirtualLock', 'ldap_add_ext_s', '_mbscpy', 
           '_localtime32_s', 'lstrcpy', '_wcsncpy*', 'CC_SHA1_Init', '_getts', '_wfopen', '__xstat64', 
           'strcoll', '_fwscanf_s_l', '_mbslwr_s_l', 'RegOpenKey', 'makepath', 'seed48', 'CC_SHA256', 
           'sendto', 'execv', 'CalculateDigest', 'memchr', '_mbscpy_s', '_strtime_s', 'ldap_search_ext_s', 
           '_chmod', 'flock', '__fxstat64', '_vsntprintf', 'CC_SHA256_Init', '_itoa_s', '__wcserror_s', 
           '_gcvt_s', 'fstream.write', 'sprintf', 'recursive_mutex', 'strrchr', 'gethostbyaddr', '_wcsupr_s_l', 
           'strcspn', 'MD5_Final', 'asprintf', '_wcstombs_s_l', '_tcstok', 'free', 'MD2_Final', 'asctime_s', 
           '_alloca', '_wputenv_s', '_wcsset_s', '_wcslwr_s_l', 'SHA1_Update', 'filebuf.sputc', 'filebuf.sputn', 
           'SQLConnect', 'ldap_compare', 'mbstowcs_s', 'HMAC_Final', 'pthread_condattr_init', '_ultow_s', 'rand', 
           'ofstream.put', 'CC_SHA224_Final', 'lstrcpynA', 'bcopy', 'system', 'CreateFile*', 'wcscpy_s', 
           '_mbsnbcpy*', 'open', '_vsnwprintf', 'strncpy', 'getopt_long', 'CC_SHA512_Final', '_vsprintf_s_l', 
           'scanf', 'mkdir', '_localtime_s', '_snprintf', '_mbccpy_s_l', 'memcmp', 'final', '_ultoa_s', 
           'lstrcpyW', 'LoadModule', '_swprintf_s_l', 'MD5_Update', '_mbsnset_s_l', '_wstrtime_s', '_strnset_s', 
           'lstrcpyA', '_mbsnbcpy_s', 'mlock', 'IsBadHugeWritePtr', 'copy', '_mbsnbcpy_s_l', 'wnsprintf', 
           'wcscpy', 'ShellExecute', 'CC_MD4', '_ultow', '_vsnwprintf_s_l', 'lstrcpyn', 'CC_SHA1_Final', 
           'vsnprintf', '_mbsnbset_s', '_i64tow', 'SHA256_Init', 'wvnsprintf', 'RegCreateKey', 'strtok_s', 
           '_wctime32_s', '_i64toa', 'CC_MD5_Final', 'wmemcpy', 'WinExec', 'CreateDirectory*', 
           'CC_SHA256_Update', '_vsnprintf_s_l', 'jrand48', 'wsprintf', 'ldap_rename_ext_s', 'filebuf.open', 
           '_wsystem', 'SHA256_Update', '_cwscanf_s', 'wsprintfW', '_sntscanf', '_splitpath', 'fscanf_s', 
           'strpbrk', 'wcstombs_s', 'wscanf', '_mbsnbcat_s_l', 'strcpynA', 'pthread_cond_init', 'wcsrtombs_s', 
           '_wsopen_s', 'CharToOemBuffA', 'RIPEMD160_Update', '_tscanf', 'HMAC', 'StrCCpy', 'Connection.connect', 
           'lstrcatn', '_mbstok', '_mbsncpy', 'CC_SHA384_Update', 'create_directories', 'pthread_mutex_unlock', 
           'CFile.Open', 'connect', '_vswprintf_s_l', '_snscanf_s_l', 'fputc', '_wscanf_s', '_snprintf_s_l', 
           'strtok', '_strtok_s_l', 'lstrcatA', 'snwscanf', 'pthread_mutex_init', 'fputs', 'CC_SHA384_Init', 
           '_putenv_s', 'CharToOemBuffW', 'pthread_mutex_trylock', '__wcstoul_internal', '_memccpy', 
           '_snwprintf_s_l', '_strncpy*', 'wmemset', 'MD4_Init', '*RC4*', 'strcpyW', '_ecvt_s', 'memcpy_s', 
           'erand48', 'IsBadHugeReadPtr', 'strcpyA', 'HeapReAlloc', 'memcpy', 'ldap_rename_ext', 'fopen_s', 
           'srandom', '_cgetws_s', '_makepath', 'SHA256_Final', 'remove', '_mbsupr_s', 'pthread_mutexattr_init', 
           '__wcstold_internal', 'StrCpy', 'ldap_delete', 'wmemmove_s', '_mkdir', 'strcat', '_cscanf_s_l', 
           'StrCAdd', 'swprintf_s', '_strnset_s_l', 'close', 'ldap_delete_ext_s', 'ldap_modrdn', 'strchr', 
           '_gmtime32_s', '_ftcscat', 'lstrcatnA', '_tcsncat', 'OemToChar', 'mutex', 'CharToOem', 'strcpy_s', 
           'lstrcatnW', '_wscanf_s_l', '__lxstat64', 'memalign', 'MD2_Init', 'StrCatBuffW', 'StrCpyN', 'CC_MD5', 
           'StrCpyA', 'StrCatBuffA', 'StrCpyW', 'tmpnam_r', '_vsnprintf', 'strcatA', 'StrCpyNW', '_mbsnbset_s_l', 
           'EVP_DigestInit', '_stscanf', 'CC_MD2', '_tcscat', 'StrCpyNA', 'xmalloc', '_tcslen', '*MD4*', 
           'vasprintf', 'strxfrm', 'chmod', 'ldap_add_ext', 'alloca', '_snscanf_s', 'IsBadWritePtr', 'swscanf_s', 
           'wmemcpy_s', '_itoa', '_ui64toa_s', 'EVP_DigestUpdate', '__wcstol_internal', '_itow', 'StrNCatW', 
           'strncat_s', 'ualstrcpy', 'execvp', '_mbccat', 'EVP_MD_CTX_init', 'assert', 'ofstream.write', 
           'ldap_add', '_sscanf_s_l', 'drand48', 'CharToOemW', 'swscanf', '_itow_s', 'RIPEMD160_Init', 
           'CopyMemory', 'initstate', 'getpwuid', 'vsprintf', '_fcvt_s', 'CharToOemA', 'setuid', 'malloc', 
           'StrCatNA', 'strcat_s', 'srand', 'getwd', '_controlfp_s', 'olestrcpy', '__wcstod_internal', 
           '_mbsnbcat', 'lstrncat', 'des_*', 'CC_SHA224_Init', 'set*', 'vsprintf_s', 'SHA1_Final', '_umask_s', 
           'gets', 'setstate', 'wvsprintfW', 'LoadLibraryEx', 'ofstream.open', 'calloc', '_mbstrlen', 
           '_cgets_s', '_sopen_s', 'IsBadStringPtr', 'wcsncat_s', 'add*', 'nrand48', 'create_directory', 
           'ldap_search_ext', '_i64toa_s', '_ltoa_s', '_cwscanf_s_l', 'wmemcmp', '__lxstat', 'lstrlen', 
           'pthread_condattr_destroy', '_ftcscpy', 'wcstok_s', '__xmknod', 'pthread_attr_destroy', 'sethostname', 
           '_fscanf_s_l', 'StrCatN', 'RegEnumKey', '_tcsncpy', 'strcatW', 'AfxLoadLibrary', 'setenv', 'tmpnam', 
           '_mbsncat_s_l', '_wstrdate_s', '_wctime64_s', '_i64tow_s', 'CC_MD4_Update', 'ldap_add_s', '_umask', 
           'CC_SHA1_Update', '_wcsset_s_l', '_mbsupr_s_l', 'strstr', '_tsplitpath', 'memmove', '_tcscpy', 
           'vsnprintf_s', 'strcmp', 'wvnsprintfW', 'tmpfile', 'ldap_modify', '_mbsncat*', 'mrand48', 'sizeof', 
           'StrCatA', '_ltow_s', '*desencrypt*', 'StrCatW', '_mbccpy', 'CC_MD2_Init', 'RIPEMD160', 'ldap_search', 
           'CC_SHA224', 'mbsrtowcs_s', 'update', 'ldap_delete_s', 'getnameinfo', '*RC5*', '_wcsncat_s_l', 
           'DriverManager.getConnection', 'socket', '_cscanf_s', 'ldap_modrdn_s', '_wopen', 'CC_SHA256_Final', 
           '_snwprintf*', 'MD2_Update', 'strcpy', '_strncat_s_l', 'CC_MD5_Init', 'mbscpy', 'wmemmove', 
           'LoadLibraryW', '_mbslen', '*alloc', '_mbsncat_s', 'LoadLibraryA', 'fopen', 'StrLen', 'delete', 
           '_splitpath_s', 'CreateFileTransacted*', 'MD4_Final', '_open', 'CC_SHA384', 'wcslen', 'wcsncat', 
           '_mktemp_s', 'pthread_mutexattr_destroy', '_snwscanf_s', '_strset_s', '_wcsncpy_s_l', 'CC_MD2_Final', 
           '_mbstok_s_l', 'wctomb_s', 'MySQL_Driver.connect', '_snwscanf_s_l', '*_des_*', 'LoadLibrary', 
           '_swscanf_s_l', 'ldap_compare_s', 'ldap_compare_ext', '_strlwr_s', 'GetEnvironmentVariable', 
           'cuserid', '_mbscat_s', 'strspn', '_mbsncpy_s', 'ldap_modrdn2', 'LeaveCriticalSection', 'CopyFile', 
           'getpwd', 'sscanf', 'creat', 'RegSetValue', 'ldap_modrdn2_s', 'CFile.Close', '*SHA_1*', 
           'pthread_cond_destroy', 'CC_SHA512_Update', '*RC2*', 'StrNCatA', '_mbsnbcpy', '_mbsnset_s', 
           'crypt', 'excel', '_vstprintf', 'xstrdup', 'wvsprintfA', 'getopt', 'mkstemp', '_wcsnset_s', 
           '_stprintf', '_sntprintf', 'tmpfile_s', 'OpenDocumentFile', '_mbsset_s_l', '_strset_s_l', 
           '_strlwr_s_l', 'ifstream.open', 'xcalloc', 'StrNCpyA', '_wctime_s', 'CC_SHA224_Update', '_ctime64_s', 
           'MoveFile', 'chown', 'StrNCpyW', 'IsBadReadPtr', '_ui64tow_s', 'IsBadCodePtr', 'getc', 
           'OracleCommand.ExecuteOracleScalar', 'AccessDataSource.Insert', 'IDbDataAdapter.FillSchema', 
           'IDbDataAdapter.Update', 'GetWindowText*', 'SendMessage', 'SqlCommand.ExecuteNonQuery', 'streambuf.sgetc', 
           'streambuf.sgetn', 'OracleCommand.ExecuteScalar', 'SqlDataSource.Update', '_Read_s', 'IDataAdapter.Fill', 
           '_wgetenv', '_RecordsetPtr.Open*', 'AccessDataSource.Delete', 'Recordset.Open*', 'filebuf.sbumpc', 'DDX_*', 
           'RegGetValue', 'fstream.read*', 'SqlCeCommand.ExecuteResultSet', 'SqlCommand.ExecuteXmlReader', 'main', 
           'streambuf.sputbackc', 'read', 'm_lpCmdLine', 'CRichEditCtrl.Get*', 'istream.putback', 
           'SqlCeCommand.ExecuteXmlReader', 'SqlCeCommand.BeginExecuteXmlReader', 'filebuf.sgetn', 
           'OdbcDataAdapter.Update', 'filebuf.sgetc', 'SQLPutData', 'recvfrom', 'OleDbDataAdapter.FillSchema', 
           'IDataAdapter.FillSchema', 'CRichEditCtrl.GetLine', 'DbDataAdapter.Update', 'SqlCommand.ExecuteReader', 
           'istream.get', 'ReceiveFrom', '_main', 'fgetc', 'DbDataAdapter.FillSchema', 'kbhit', 'UpdateCommand.Execute*', 
           'Statement.execute', 'fgets', 'SelectCommand.Execute*', 'getch', 'OdbcCommand.ExecuteNonQuery', 
           'CDaoQueryDef.Execute', 'fstream.getline', 'ifstream.getline', 'SqlDataAdapter.FillSchema', 
           'OleDbCommand.ExecuteReader', 'Statement.execute*', 'SqlCeCommand.BeginExecuteNonQuery', 
           'OdbcCommand.ExecuteScalar', 'SqlCeDataAdapter.Update', 'sendmessage', 'mysqlpp.DBDriver', 'fstream.peek', 
           'Receive', 'CDaoRecordset.Open', 'OdbcDataAdapter.FillSchema', '_wgetenv_s', 'OleDbDataAdapter.Update', 
           'readsome', 'SqlCommand.BeginExecuteXmlReader', 'recv', 'ifstream.peek', '_Main', '_tmain', '_Readsome_s', 
           'SqlCeCommand.ExecuteReader', 'OleDbCommand.ExecuteNonQuery', 'fstream.get', 'IDbCommand.ExecuteScalar', 
           'filebuf.sputbackc', 'IDataAdapter.Update', 'streambuf.sbumpc', 'InsertCommand.Execute*', 'RegQueryValue', 
           'IDbCommand.ExecuteReader', 'SqlPipe.ExecuteAndSend', 'Connection.Execute*', 'getdlgtext', 'ReceiveFromEx', 
           'SqlDataAdapter.Update', 'RegQueryValueEx', 'SQLExecute', 'pread', 'SqlCommand.BeginExecuteReader', 'AfxWinMain', 
           'getchar', 'istream.getline', 'SqlCeDataAdapter.Fill', 'OleDbDataReader.ExecuteReader', 'SqlDataSource.Insert', 
           'istream.peek', 'SendMessageCallback', 'ifstream.read*', 'SqlDataSource.Select', 'SqlCommand.ExecuteScalar', 
           'SqlDataAdapter.Fill', 'SqlCommand.BeginExecuteNonQuery', 'getche', 'SqlCeCommand.BeginExecuteReader', 'getenv', 
           'streambuf.snextc', 'Command.Execute*', '_CommandPtr.Execute*', 'SendNotifyMessage', 'OdbcDataAdapter.Fill', 
           'AccessDataSource.Update', 'fscanf', 'QSqlQuery.execBatch', 'DbDataAdapter.Fill', 'cin', 
           'DeleteCommand.Execute*', 'QSqlQuery.exec', 'PostMessage', 'ifstream.get', 'filebuf.snextc', 
           'IDbCommand.ExecuteNonQuery', 'Winmain', 'fread', 'getpass', 'GetDlgItemTextCCheckListBox.GetCheck', 
           'DISP_PROPERTY_EX', 'pread64', 'Socket.Receive*', 'SACommand.Execute*', 'SQLExecDirect', 
           'SqlCeDataAdapter.FillSchema', 'DISP_FUNCTION', 'OracleCommand.ExecuteNonQuery', 'CEdit.GetLine', 
           'OdbcCommand.ExecuteReader', 'CEdit.Get*', 'AccessDataSource.Select', 'OracleCommand.ExecuteReader', 
           'OCIStmtExecute', 'getenv_s', 'DB2Command.Execute*', 'OracleDataAdapter.FillSchema', 'OracleDataAdapter.Fill', 
           'CComboBox.Get*', 'SqlCeCommand.ExecuteNonQuery', 'OracleCommand.ExecuteOracleNonQuery', 'mysqlpp.Query', 
           'istream.read*', 'CListBox.GetText', 'SqlCeCommand.ExecuteScalar', 'ifstream.putback', 'readlink', 
           'CHtmlEditCtrl.GetDHtmlDocument', 'PostThreadMessage', 'CListCtrl.GetItemText', 'OracleDataAdapter.Update', 
           'OleDbCommand.ExecuteScalar', 'stdin', 'SqlDataSource.Delete', 'OleDbDataAdapter.Fill', 'fstream.putback', 
           'IDbDataAdapter.Fill', '_wspawnl', 'fwprintf', 'sem_wait', '_unlink', 'ldap_search_ext_sW', 'signal', 'PQclear', 
           'PQfinish', 'PQexec', 'PQresultStatus']

import re
import nltk 
import warnings
warnings.filterwarnings('ignore')


def symbolic_tokenize(code):
    tokens = nltk.word_tokenize(code)
    c_tokens = []
    for t in tokens:
        if t.strip() != '':
            c_tokens.append(t.strip())
    f_count = 1
    var_count = 1
    symbol_table = {}
    final_tokens = []
    for idx in range(len(c_tokens)):
        t = c_tokens[idx]
        if t in keywords:
            final_tokens.append(t)
        elif t in puncs:
            final_tokens.append(t)
        elif t in l_funcs:
            final_tokens.append(t)
        elif c_tokens[idx + 1] == '(':
            if t in keywords:
                final_tokens.append(t + '(')
            else:
                if t not in symbol_table.keys():
                    symbol_table[t] = "FUNC" + str(f_count)
                    f_count += 1
                final_tokens.append(symbol_table[t] + '(')
            idx += 1
        
        elif t.endswith('('):
            t = t[:-1]
            if t in keywords:
                final_tokens.append(t + '(')
            else:
                if t not in symbol_table.keys():
                    symbol_table[t] = "FUNC" + str(f_count)
                    f_count += 1
                final_tokens.append(symbol_table[t] + '(')
        elif t.endswith('()'):
            t = t[:-2]
            if t in keywords:
                final_tokens.append(t + '()')
            else:
                if t not in symbol_table.keys():
                    symbol_table[t] = "FUNC" + str(f_count)
                    f_count += 1
                final_tokens.append(symbol_table[t] + '()')
        elif re.match("^\"*\"$", t) is not None:
            final_tokens.append("STRING")
        elif re.match("^[0-9]+(\.[0-9]+)?$", t) is not None:
            final_tokens.append("NUMBER")
        elif re.match("^[0-9]*(\.[0-9]+)$", t) is not None:
            final_tokens.append("NUMBER")
        else:
            if t not in symbol_table.keys():
                symbol_table[t] = "VAR" + str(var_count)
                var_count += 1
            final_tokens.append(symbol_table[t])
    return ' '.join(final_tokens)


code = 'char *psz_fileName = calloc( ZIP_FILENAME_LEN, 1 );' + \
        '\nZIP_FILENAME_LEN, NULL, 0, NULL, 0 )' + \
        '\nif( unzGetCurrentFileInfo( file, p_fileInfo, psz_fileName,' +\
        '\nvlc_array_append( p_filenames, strdup( psz_fileName ) );' + \
        '\nfree( psz_fileName );'
print(code)
print('=' * 50)
print(symbolic_tokenize(code))


# In[25]:


import json
directory = '../data/VulDeePecker/'
vul_files = ['CWE-119', 'CWE-399']


sources = []

for vnum in vul_files:
    file_path = directory + 'unformatted/' + vnum + '.txt'
    all_examples = []
    with open(file_path) as fp:
        v, nv =  0, 0
        lines = fp.readlines()
        example = []
        for idx, line in enumerate(lines):
            if line.strip() == '':
                continue
            if '-------------------------' in line: #Example already complete
                if len(example) >= 3:
                    code = '\n'.join(example[1:-1])
                    try:
                        label = int(example[-1])
                        if label == 0:
                            nv += 1
                        else:
                            v += 1
                        tokenized = symbolic_tokenize(code)
                        all_examples.append({
                            'code': code,
                            'label': label,
                            'tokenized': tokenized
                        })
                    except:
                        pass
                    example = []
            else:
                example.append(line.strip())
        output_file = open(directory + vnum + '-processed.json', 'w')
        json.dump(all_examples, output_file)
        output_file.close()
        print(v, nv)
                    


# In[26]:


directory = '../data/SySeVR/'
vul_files = ['API_function_call', 'Arithmetic_expression', 'Array_usage', 'Pointer_usage']

sources = []

for vnum in vul_files:
    file_path = directory + 'unformatted/' + vnum + '.txt'
    all_examples = []
    with open(file_path) as fp:
        v, nv =  0, 0
        lines = fp.readlines()
        example = []
        for idx, line in enumerate(lines):
            if line.strip() == '':
                continue
            if '-------------------------' in line: #Example already complete
                if len(example) >= 3:
                    code = '\n'.join(example[1:-1])
                    try:
                        label = int(example[-1])
                        if label == 0:
                            nv += 1
                        else:
                            v += 1
                        tokenized = symbolic_tokenize(code)
                        all_examples.append({
                            'code': code,
                            'label': label,
                            'tokenized': tokenized
                        })
                    except:
                        pass
                    example = []
            else:
                example.append(line.strip())
        output_file = open(directory + vnum + '-processed.json', 'w')
        json.dump(all_examples, output_file)
        output_file.close()
        print(v, nv)


# In[ ]:




