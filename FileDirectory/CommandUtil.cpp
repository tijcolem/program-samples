//
// CommandUtil.cpp: implementation of the 
//                  CommandUtil class.
//
//
#include "CommandUtil.h"
#include <Wincrypt.h>

CommandUtil::CommandUtil(char *SessionName) {

  dwResult = 0;

  if(SessionName != NULL) {

    ZeroMemory(StdOutputPipeName,sizeof(StdOutputPipeName));

    ZeroMemory(StdErrorPipeName,sizeof(StdErrorPipeName));

    ZeroMemory(StdInputPipeName,sizeof(StdInputPipeName));

    sprintf(StdOutputPipeName,"\\\\.\\pipe\\%s_StdOut\0",SessionName);

    sprintf(StdErrorPipeName,"\\\\.\\pipe\\%s_StdErr\0",SessionName);

    sprintf(StdInputPipeName,"\\\\.\\pipe\\%s_StdIn\0",SessionName);
  }

  ZeroMemory(&si,sizeof(STARTUPINFO));
  ZeroMemory(&pi,sizeof(PROCESS_INFORMATION));
  ZeroMemory(&sa,sizeof(SECURITY_ATTRIBUTES));

  ZeroMemory(User,sizeof(User));
  ZeroMemory(Password,sizeof(Password));

  sprintf(WorkingDirectory,".\0");

  si.cb = sizeof(STARTUPINFO);
  si.dwFlags = STARTF_USESHOWWINDOW | STARTF_USESTDHANDLES;
  si.wShowWindow = SW_HIDE;

  si.hStdInput  = GetStdHandle(STD_INPUT_HANDLE);
  si.hStdOutput = GetStdHandle(STD_OUTPUT_HANDLE);
  si.hStdError  = GetStdHandle(STD_ERROR_HANDLE);

  sa.nLength = sizeof(SECURITY_ATTRIBUTES);
  sa.lpSecurityDescriptor = NULL;
  sa.bInheritHandle = TRUE;

  hRunCommandDone = CreateEvent(NULL,TRUE,TRUE,NULL);
  hStopRequest    = CreateEvent(NULL,TRUE,FALSE,NULL);

  TimeoutInMilliSec = RUN_COMMAND_TIMEOUT * 1000;

  StdOutput         = NULL;
  hStdOutClientPipe = INVALID_HANDLE_VALUE;
  hStdOutServerPipe = INVALID_HANDLE_VALUE;

  StdError          = NULL;
  hStdErrClientPipe = INVALID_HANDLE_VALUE;
  hStdErrServerPipe = INVALID_HANDLE_VALUE;

  StdInput          = NULL;
  hStdInClientPipe  = INVALID_HANDLE_VALUE;
  hStdInServerPipe  = INVALID_HANDLE_VALUE;

  UserSize     = 0;
  PasswordSize = 0;

  // create standard output pipe
  if((hStdOutServerPipe = CreateNamedPipe(StdOutputPipeName,
                                          PIPE_ACCESS_OUTBOUND,
                                          PIPE_TYPE_BYTE | PIPE_READMODE_BYTE | PIPE_NOWAIT,
                                          PIPE_MAX_INSTANCE,
                                          PIPE_OUTPUT_BUFFER_SIZE,
                                          0,
                                          NMPWAIT_USE_DEFAULT_WAIT, 
                                          &sa)) != INVALID_HANDLE_VALUE) {
    si.hStdOutput = hStdOutServerPipe;

    if((hStdOutClientPipe = CreateFile(StdOutputPipeName,
                                       GENERIC_READ, 
                                       0, 
                                       &sa, 
                                       OPEN_EXISTING, 
                                       0, 
                                       NULL)) == INVALID_HANDLE_VALUE) {

      if(hStdOutServerPipe != INVALID_HANDLE_VALUE) {

        CloseHandle(hStdOutServerPipe);
      }

      sprintf(Message,"Error opening standard-output pipe for reading. \0");

      FormatGetLastError();
    }
  }
  else {

    sprintf(Message,"Error creating standard-output pipe. \0");

    FormatGetLastError();
  }

  // create standard error pipe
  if((hStdErrServerPipe = CreateNamedPipe(StdErrorPipeName,
                                          PIPE_ACCESS_OUTBOUND,
                                          PIPE_TYPE_BYTE | PIPE_READMODE_BYTE | PIPE_NOWAIT,
                                          PIPE_MAX_INSTANCE,
                                          PIPE_OUTPUT_BUFFER_SIZE,
                                          0,
                                          NMPWAIT_USE_DEFAULT_WAIT, 
                                          &sa)) != INVALID_HANDLE_VALUE) {
    si.hStdError = hStdErrServerPipe;

    if((hStdErrClientPipe = CreateFile(StdErrorPipeName,
                                       GENERIC_READ, 
                                       0, 
                                       &sa, 
                                       OPEN_EXISTING, 
                                       0, 
                                       NULL)) == INVALID_HANDLE_VALUE) {

      if(hStdErrServerPipe != INVALID_HANDLE_VALUE) {

        CloseHandle(hStdErrServerPipe);
      }

      sprintf(Message,"Error opening standard-error pipe for reading. \0");

      FormatGetLastError();
    }
  }
  else {

    sprintf(Message,"Error creating standard-error pipe. \0");

    FormatGetLastError();
  }

  // create standard input pipe
  if((hStdInServerPipe = CreateNamedPipe(StdInputPipeName,
                                         PIPE_ACCESS_INBOUND,
                                         PIPE_TYPE_BYTE | PIPE_READMODE_BYTE | PIPE_NOWAIT,
                                         PIPE_MAX_INSTANCE,
                                         PIPE_OUTPUT_BUFFER_SIZE,
                                         PIPE_OUTPUT_BUFFER_SIZE,
                                         NMPWAIT_USE_DEFAULT_WAIT, 
                                         &sa)) != INVALID_HANDLE_VALUE) {
    si.hStdInput = hStdInServerPipe;

    if((hStdInClientPipe = CreateFile(StdInputPipeName,
                                      GENERIC_WRITE, 
                                      0, 
                                      &sa, 
                                      OPEN_EXISTING, 
                                      0, 
                                      NULL)) == INVALID_HANDLE_VALUE) {

      if(hStdInServerPipe != INVALID_HANDLE_VALUE) {

        CloseHandle(hStdInServerPipe);
      }

      sprintf(Message,"Error opening standard-input pipe for reading. \0");

      FormatGetLastError();
    }
  }
  else {

    sprintf(Message,"Error creating standard-input pipe. \0");

    FormatGetLastError();
  }
}

CommandUtil::~CommandUtil(void) {

  KillCommand(0);

  WaitForSingleObject(hRunCommandDone,INFINITE);

  // destroy standard output pipe
  if(hStdOutServerPipe != INVALID_HANDLE_VALUE) {

    DisconnectNamedPipe(hStdOutServerPipe);

    CloseHandle(hStdOutServerPipe);

    hStdOutServerPipe = INVALID_HANDLE_VALUE;
  }

  if(hStdOutClientPipe != INVALID_HANDLE_VALUE) {

    CloseHandle(hStdOutClientPipe);

    hStdOutClientPipe = INVALID_HANDLE_VALUE;
  }

  // destroy standard error pipe
  if(hStdErrServerPipe != INVALID_HANDLE_VALUE) {

    DisconnectNamedPipe(hStdErrServerPipe);

    CloseHandle(hStdErrServerPipe);

    hStdErrServerPipe = INVALID_HANDLE_VALUE;
  }

  if(hStdErrClientPipe != INVALID_HANDLE_VALUE) {

    CloseHandle(hStdErrClientPipe);

    hStdErrClientPipe = INVALID_HANDLE_VALUE;
  }

  // destroy standard input pipe
  if(hStdInServerPipe != INVALID_HANDLE_VALUE) {

    DisconnectNamedPipe(hStdInServerPipe);

    CloseHandle(hStdInServerPipe);

    hStdInServerPipe = INVALID_HANDLE_VALUE;
  }

  if(hStdInClientPipe != INVALID_HANDLE_VALUE) {

    CloseHandle(hStdInClientPipe);

    hStdInClientPipe = INVALID_HANDLE_VALUE;
  }

  if(pi.hProcess != NULL) {

    CloseHandle(pi.hProcess);

    pi.hProcess = NULL;
  }

  if(pi.hThread != NULL) {

    CloseHandle(pi.hThread);

    pi.hThread = NULL;
  }

  if(hStopRequest != NULL)    CloseHandle(hStopRequest);

  if(hRunCommandDone != NULL) CloseHandle(hRunCommandDone);
}

void CommandUtil::SetWorkingDirectory(char *WorkingDirectory) {

  ZeroMemory(this->WorkingDirectory,sizeof(this->WorkingDirectory));

  strncpy(this->WorkingDirectory,WorkingDirectory,sizeof(this->WorkingDirectory) - 1);
}

void CommandUtil::EnableDisplay(BOOL Enable) {

// *** IMPORTANT NOTE ABOUT CURRENT IMPLEMENTATION ***
//
// If running from a service and the EnableDisplay is enabled,
// apps will only be displayed properly if the service is
// running as LocalSystem and the user credentials (SetUserCredentials)
// are never set (i.e., commands are run from RunCommand as LocalSystem)

  if(Enable) {

    si.wShowWindow = SW_SHOWDEFAULT;
    si.lpDesktop   = "winsta0\\default";
  }
  else {

    si.wShowWindow = SW_HIDE;
    si.lpDesktop = "\0";
  }
}

DWORD CommandUtil::SetUserCredentials(char *User,DWORD UserSize,char *Password,DWORD PasswordSize) {

  this->UserSize     = 0;
  this->PasswordSize = 0;

  if((User != NULL) && UserSize) {

    this->UserSize = UserSize;

    memcpy(this->User,User,UserSize);

    if((Password != NULL) && PasswordSize) {

      this->PasswordSize = PasswordSize;

      memcpy(this->Password,Password,PasswordSize);

      SetCreateProcessAsUserPrivileges();
    }
  }

  return(FALSE);
}

BOOL CommandUtil::SetCreateProcessAsUserPrivileges(void) {

  TOKEN_PRIVILEGES tp; 
  HANDLE hToken = NULL; 

  if(!OpenProcessToken(GetCurrentProcess(),
                       TOKEN_ADJUST_PRIVILEGES, 
                       &hToken)) { 

    sprintf(Message,"An error occurred while opening the process token of the current process. \0");

    FormatGetLastError();

    CloseHandle(hToken);

    return(TRUE);
  } 
    
  tp.PrivilegeCount = 1; 
  tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED; 

  if(!LookupPrivilegeValue(NULL,
                           SE_ASSIGNPRIMARYTOKEN_NAME,
                           &tp.Privileges[0].Luid)) {

    sprintf(Message,"An error occurred while looking up the SE_ASSIGNPRIMARYTOKEN_NAME privilege. \0");

    FormatGetLastError();

    CloseHandle(hToken);

    return(TRUE);
  }

  if(!AdjustTokenPrivileges(hToken,
                            FALSE,
                            &tp,
                            0,
                            NULL,
                            NULL)) {

    sprintf(Message,"An error occurred while adjusting the SE_ASSIGNPRIMARYTOKEN_NAME privilege. \0");

    FormatGetLastError();

    CloseHandle(hToken);

    return(TRUE);
  }


  if(!LookupPrivilegeValue(NULL,
                           SE_INCREASE_QUOTA_NAME,
                           &tp.Privileges[0].Luid)) {

    sprintf(Message,"An error occurred while looking up the SE_INCREASE_QUOTA_NAME privilege. \0");

    FormatGetLastError();

    CloseHandle(hToken);

    return(TRUE);
  }

  if(!AdjustTokenPrivileges(hToken,
                            FALSE,
                            &tp,
                            0,
                            NULL,
                            NULL)) {

    sprintf(Message,"An error occurred while adjusting the SE_INCREASE_QUOTA_NAME privilege. \0");

    FormatGetLastError();

    CloseHandle(hToken);

    return(TRUE);
  }

  if(!LookupPrivilegeValue(NULL,
                           SE_TCB_NAME,
                           &tp.Privileges[0].Luid)) {

    sprintf(Message,"An error occurred while looking up the SE_TCB_NAME privilege. \0");

    FormatGetLastError();

    CloseHandle(hToken);

    return(TRUE);
  }

  if(!AdjustTokenPrivileges(hToken,
                            FALSE,
                            &tp,
                            0,
                            NULL,
                            NULL)) {

    sprintf(Message,"An error occurred while adjusting the SE_TCB_NAME privilege. \0");

    FormatGetLastError();

    CloseHandle(hToken);

    return(TRUE);
  }

  CloseHandle(hToken);

  return(FALSE);
}

DWORD CommandUtil::RunCommand(char *Command,
                              DWORD TimeoutInSec,
                              BOOL TerminateOnTimeout) {
  hToken = NULL;

  ReturnValue = COMMAND_SUCCESS;

  TimeoutInMilliSec = TimeoutInSec * 1000;

  ResetEvent(hRunCommandDone);

  if(UserSize && PasswordSize) {

    if(!DecryptData(User,UserSize) && !DecryptData(Password,PasswordSize)) {

      if(!LogonUser(User,
                    NULL,
                    Password,
                    LOGON32_LOGON_INTERACTIVE,
                    LOGON32_PROVIDER_DEFAULT,
                    &hToken)) {

        ReturnValue = LOGON_FAILED;

        sprintf(Message,"An error occurred while logging on as user %s. \0",User);

        FormatGetLastError();
      }

      UserSize = strlen(User);
      if(CryptData(User,&UserSize)) UserSize = 0;

      PasswordSize = strlen(Password);
      if(CryptData(Password,&PasswordSize)) PasswordSize = 0;
    }
    else {

      ReturnValue = LOGON_FAILED;

      sprintf(Message,"An error occurred while while decrypting the user credentials.\0");
    }

    if(ReturnValue == COMMAND_SUCCESS) {

// *** IMPORTANT NOTE ***
// CreateProcessAsUser can fail with the error "A required privilege is not held by the client."
// To resolve this problem, you'll need to elevate the rights of the account calling CreateProcessAsUser
// with the "Replace a process level token" right. To do so, open the Control Panel / Administrative Tools / 
// Local Security Policy and add the user account to the "Replace a process level token" right. 
// (You may have to logout or even reboot to have this change take effect.)"

      ImpersonateLoggedOnUser(hToken);

      dwResult = CreateProcessAsUser(hToken,
                                     NULL,
                                     Command,
                                     NULL,
                                     NULL,
                                     TRUE,
                                     HIGH_PRIORITY_CLASS,
                                     NULL,
                                     WorkingDirectory,
                                     &si,
                                     &pi);
    }
  }
  else {

    dwResult = CreateProcess(NULL,
                             Command,
                             NULL,
                             NULL,
                             TRUE,
                             HIGH_PRIORITY_CLASS,
                             NULL,
                             WorkingDirectory,
                             &si,
                             &pi);
  }

  if(ReturnValue == COMMAND_SUCCESS) {

    if(dwResult) {

      ResetEvent(hStopRequest);

      hWaitObj[0] = hStopRequest;

      hWaitObj[1] = pi.hProcess;

      dwResult = WaitForMultipleObjects(NUM_WAIT_OBJ,
                                        hWaitObj,
                                        FALSE,
                                        TimeoutInMilliSec);
      switch(dwResult) {

        case(WAIT_OBJECT_0):

          ReturnValue = COMMAND_STOP_REQUESTED;

          sprintf(Message,"Stop requested. Terminating %s.\0",Command);

          TerminateProcess(pi.hProcess,0);

          break;

        case(WAIT_OBJECT_0 + 1):

          ReturnValue = COMMAND_SUCCESS;

          break;

        case(WAIT_TIMEOUT):

          ReturnValue = COMMAND_TIMEOUT;

          if(TerminateOnTimeout) {

            sprintf(Message,"Timeout waiting for %s to finish. Terminating process.\0",Command);

            TerminateProcess(pi.hProcess,0);
          }
          else {

            sprintf(Message,"Timeout waiting for %s to finish.\0",Command);
          }

        break;

        case(WAIT_FAILED):

          ReturnValue = COMMAND_WAIT_FAILED;

          sprintf(Message,"An error occurred while waiting for %s to finish. \0",Command);

          FormatGetLastError();

          strcat(Message," Terminating process.");

          TerminateProcess(pi.hProcess,0);

          break;

        default:

          ReturnValue = COMMAND_ERROR_UNKNOWN;

          sprintf(Message,"An unknown error occurred while waiting for %s to finish.\0",Command);

          FormatGetLastError();

          strcat(Message," Terminating process.");

          TerminateProcess(pi.hProcess,0);

          break;
      }

      if(pi.hProcess != NULL) {

        CloseHandle(pi.hProcess);

        pi.hProcess = NULL;
      }

      if(pi.hThread != NULL) {

        CloseHandle(pi.hThread);

        pi.hThread = NULL;
      }
    }
    else {

      ReturnValue = COMMAND_START_ERROR;

      sprintf(Message,"An error occurred while creating \"%s\". \0",Command);

      FormatGetLastError();
    }
  }

  if(ReturnValue == COMMAND_SUCCESS) sprintf(Message,"Command executed successfully.\0");

  if(hToken != NULL) CloseHandle(hToken);

  SetEvent(hRunCommandDone);

  return(ReturnValue);
}

DWORD CommandUtil::GetStdOutput(char *StdOutputString,DWORD *StdOutputStringSize) {

  dwBytesRead = dwBytesInPipe = 0;

  if(PeekNamedPipe(hStdOutClientPipe,NULL,0,NULL,&dwBytesInPipe,NULL)) {

    if(dwBytesInPipe == 0) {

      *StdOutputStringSize = dwBytesInPipe;

      sprintf(Message,"Standard Output is empty.\0");

      return(OUTPUT_EMPTY);
    }

    if(*StdOutputStringSize <= dwBytesInPipe) {

      *StdOutputStringSize = dwBytesInPipe + 1;

      sprintf(Message,"The buffer is too small to store the contents of Standard Output.\0");

      return(BUFFER_TOO_SMALL);
    }

    if(StdOutputString == NULL) {

      *StdOutputStringSize = dwBytesInPipe + 1;

      sprintf(Message,"The Standard Output buffer is invalid.\0");

      return(NULL_BUFFER);
    }

    StdOutput = new char [dwBytesInPipe + 1];

    ZeroMemory(StdOutput,dwBytesInPipe + 1);

    ReadFile(hStdOutClientPipe,StdOutput,dwBytesInPipe,&dwBytesRead,NULL);

    strncpy(StdOutputString,StdOutput,dwBytesRead);

    StdOutputString[dwBytesRead] = '\0';

    delete [] StdOutput; 
  }
  else {

    *StdOutputStringSize = 0;

    sprintf(Message,"Error acquiring Standard Output information. \0");

    FormatGetLastError();

    return(PIPE_ERROR);
  }

  return(ERROR_SUCCESS);
}

DWORD CommandUtil::GetStdError(char *StdErrorString,DWORD *StdErrorStringSize) {

  dwBytesRead = dwBytesInPipe = 0;

  if(PeekNamedPipe(hStdErrClientPipe,NULL,0,NULL,&dwBytesInPipe,NULL)) {

    if(dwBytesInPipe == 0) {

      *StdErrorStringSize = dwBytesInPipe;

      sprintf(Message,"Standard Error is empty.\0");

      return(OUTPUT_EMPTY);
    }

    if(*StdErrorStringSize <= dwBytesInPipe) {

      *StdErrorStringSize = dwBytesInPipe + 1;

      sprintf(Message,"The buffer is too small to store the contents of Standard Error.\0");

      return(BUFFER_TOO_SMALL);
    }

    if(StdErrorString == NULL) {

      *StdErrorStringSize = dwBytesInPipe + 1;

      sprintf(Message,"The Standard Error buffer is invalid.\0");

      return(NULL_BUFFER);
    }

    StdError = new char [dwBytesInPipe + 1];

    ZeroMemory(StdError,dwBytesInPipe + 1);

    ReadFile(hStdErrClientPipe,StdError,dwBytesInPipe,&dwBytesRead,NULL);

    strncpy(StdErrorString,StdError,dwBytesRead);

    StdErrorString[dwBytesRead] = '\0';

    delete [] StdError; 
  }
  else {

    *StdErrorStringSize = 0;

    sprintf(Message,"Error acquiring Standard Error information. \0");

    FormatGetLastError();

    return(PIPE_ERROR);
  }

  return(ERROR_SUCCESS);
}

DWORD CommandUtil::SetStdInput(char *StdInputString) {

  DWORD dwBytesWritten = 0;

  WriteFile(hStdInClientPipe,StdInputString,strlen(StdInputString),&dwBytesWritten,NULL);

  return(dwBytesWritten);
}

unsigned short CommandUtil::GetCommandStatus(void) {

  if(pi.hProcess != NULL) {

    if(WaitForSingleObject(pi.hProcess,0) == WAIT_OBJECT_0) {

      return(COMMAND_FINISHED);
    }
    else {

      return(COMMAND_RUNNING);
    }
  }
  else {

    return(COMMAND_FINISHED);
  }
}

void CommandUtil::KillCommand(DWORD TimeoutInSec) {

  SetEvent(hStopRequest);

  TimeoutInMilliSec = TimeoutInSec * 1000;

  if(pi.hProcess != NULL) {

    dwResult = WaitForSingleObject(pi.hProcess,TimeoutInMilliSec);

    if(dwResult != WAIT_OBJECT_0) {

      TerminateProcess(pi.hProcess,0);
    }

    WaitForSingleObject(hRunCommandDone,INFINITE);
  }
}

DWORD CommandUtil::FormatGetLastError(DWORD WinError) {

  DWORD dwError = 0;
  LPVOID lpMsgBuf;

  if(WinError == 0xFFFFFFFF) {

    dwError = GetLastError();
  }
  else {

    dwError = WinError;
  }

  if(FormatMessage(FORMAT_MESSAGE_ALLOCATE_BUFFER | 
                   FORMAT_MESSAGE_FROM_SYSTEM | 
                   FORMAT_MESSAGE_IGNORE_INSERTS,
                   NULL,
                   dwError,
                   MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
                   (LPTSTR) &lpMsgBuf,
                   0,
                   NULL)) {

    if(lpMsgBuf != NULL) {

      *((char *)lpMsgBuf + strlen((char *)lpMsgBuf) - 2) = '\0';  // remove line feed

      strcat(Message,(LPCTSTR)lpMsgBuf);

      LocalFree(lpMsgBuf);
    }
  }

  return(dwError);
}

BOOL CommandUtil::CryptData(char *Data,DWORD *DataSize) {

  char SwapByte     = { 0 };
  BOOL ReturnValue  = FALSE;
  DATA_BLOB DataIn  = { 0 };
  DATA_BLOB DataOut = { 0 };

  DataIn.pbData = (BYTE *)Data;
  DataIn.cbData = (DWORD)*DataSize;

  if(CryptProtectData(&DataIn,L"\0",NULL,NULL,NULL,CRYPTPROTECT_LOCAL_MACHINE,&DataOut)) {

    *DataSize = (DWORD)DataOut.cbData;

    memcpy(Data,(char *)DataOut.pbData,*DataSize);

    SwapByte            = Data[*DataSize - 1];
    Data[*DataSize - 1] = Data[10];
    Data[10]            = SwapByte;

    SwapByte            = Data[*DataSize - 1];
    Data[*DataSize - 1] = Data[*DataSize - 2];
    Data[*DataSize - 2] = SwapByte;
  }
  else ReturnValue = TRUE;

  if(DataOut.pbData != NULL) LocalFree(DataOut.pbData);

  return(ReturnValue);
}

BOOL CommandUtil::DecryptData(char *Data,DWORD DataSize) {

  char SwapByte     = { 0 };
  DATA_BLOB DataIn  = { 0 };
  DATA_BLOB DataOut = { 0 };

  SwapByte           = Data[DataSize - 1];
  Data[DataSize - 1] = Data[DataSize - 2];
  Data[DataSize - 2] = SwapByte;

  SwapByte           = Data[DataSize - 1];
  Data[DataSize - 1] = Data[10];
  Data[10]           = SwapByte;

  DataIn.pbData = (BYTE *)Data;
  DataIn.cbData = DataSize;

  if(CryptUnprotectData(&DataIn,NULL,NULL,NULL,NULL,0,&DataOut)) {

    strncpy(Data,(char *)DataOut.pbData,(DWORD)DataOut.cbData);

    Data[DataOut.cbData] = '\0';

    return(FALSE);
  }
  else {

    return(TRUE);
  }
}

void CommandUtil::SetWindowPosition(DWORD StartPosPercentMaxX,
                                    DWORD StartPosPercentMaxY,
                                    DWORD WidthPercentMaxX,
                                    DWORD WidthPercentMaxY) {
  DEVMODE DevMode = { 0 };

  if(!StartPosPercentMaxX && !StartPosPercentMaxY && !WidthPercentMaxX && !WidthPercentMaxY) {

    si.dwFlags = STARTF_USESHOWWINDOW | STARTF_USESTDHANDLES;
  }
  else {

    si.dwFlags = STARTF_USESHOWWINDOW | STARTF_USESTDHANDLES | STARTF_USEPOSITION | STARTF_USESIZE;
  }

  EnumDisplaySettings(NULL,ENUM_CURRENT_SETTINGS,&DevMode);

  // set window start position
  si.dwX = DWORD((StartPosPercentMaxX / 100.f) * DevMode.dmPelsWidth);
  si.dwY = DWORD((StartPosPercentMaxY / 100.f) * DevMode.dmPelsHeight);

  si.dwXSize = DWORD((WidthPercentMaxX / 100.f) * DevMode.dmPelsWidth);
  si.dwYSize = DWORD((WidthPercentMaxY / 100.f) * DevMode.dmPelsHeight);
}