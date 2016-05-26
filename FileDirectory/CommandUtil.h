#ifndef _COMMANDUTIL_H_
#define _COMMANDUTIL_H_

#include <stdio.h>
#include <math.h>
#include <process.h>
#include <windows.h>

#define COMMAND_SUCCESS          9000
#define COMMAND_STOP_REQUESTED   9001  
#define COMMAND_TIMEOUT          9002
#define COMMAND_WAIT_FAILED      9003
#define COMMAND_ERROR_UNKNOWN    9004
#define COMMAND_START_ERROR      9005
#define BUFFER_TOO_SMALL         9006
#define OUTPUT_EMPTY             9007
#define NULL_BUFFER              9008
#define PIPE_ERROR               9009
#define LOGON_FAILED             9010

#define PIPE_MAX_INSTANCE        PIPE_UNLIMITED_INSTANCES
#define PIPE_OUTPUT_BUFFER_SIZE  (DWORD)pow(2,17)

#define RUN_COMMAND_TIMEOUT           60
#define RUN_COMMAND_FUNCTION_TIMEOUT  3

#define MAX_PIPNAME_LENGTH  256

#define NUM_WAIT_OBJ           2
#define MAX_MESSAGE            500
#define MAX_DIR_LENGTH         1000
#define MAX_CREDENTIAL_LENGTH  1000
#define COMMAND_RUNNING        100
#define COMMAND_FINISHED       101
class CommandUtilException {

public:

  CommandUtilException();

  ~CommandUtilException();
};

class CommandUtil {

public:

  CommandUtil(char *SessionName = NULL);

  ~CommandUtil();

  char Message[MAX_MESSAGE];

  void EnableDisplay(BOOL Enable);

  void SetWindowPosition(DWORD StartPosPercentMaxX,
                         DWORD StartPosPercentMaxY,
                         DWORD WidthPercentMaxX,
                         DWORD WidthPercentMaxY);

  unsigned short GetCommandStatus(void);

  DWORD RunCommand(char *Command,
                   DWORD TimeoutInSec = RUN_COMMAND_TIMEOUT,
                   BOOL TerminateOnTimeout = TRUE);

  DWORD GetStdOutput(char *StdOutputString,DWORD *StdOutputStringSize);

  DWORD GetStdError(char *StdErrorString,DWORD *StdErrorStringSize);

  DWORD SetStdInput(char *StdInputString);

  DWORD SetUserCredentials(char *User,DWORD UserSize,char *Password,DWORD PasswordSize);

  void SetWorkingDirectory(char *WorkingDirectory);

  void KillCommand(DWORD TimeoutInSec = RUN_COMMAND_FUNCTION_TIMEOUT);

private:

  char User[MAX_CREDENTIAL_LENGTH];
  char Password[MAX_CREDENTIAL_LENGTH];
  char WorkingDirectory[MAX_DIR_LENGTH];
  char StdOutputPipeName[MAX_PIPNAME_LENGTH];
  char StdErrorPipeName[MAX_PIPNAME_LENGTH];
  char StdInputPipeName[MAX_PIPNAME_LENGTH];
  char *StdOutput;
  char *StdError;
  char *StdInput;
  DWORD ReturnValue;
  DWORD UserSize;
  DWORD PasswordSize;
  DWORD TimeoutInMilliSec;
  DWORD dwResult;
  DWORD dwBytesRead;
  DWORD dwBytesInPipe;
  STARTUPINFO si;
  PROCESS_INFORMATION pi;
  SECURITY_ATTRIBUTES sa;
  HANDLE hToken;
  HANDLE hWaitObj[NUM_WAIT_OBJ];
  HANDLE hStopRequest;
  HANDLE hRunCommandDone;
  HANDLE hStdOutClientPipe;
  HANDLE hStdOutServerPipe;
  HANDLE hStdErrClientPipe;
  HANDLE hStdErrServerPipe;
  HANDLE hStdInClientPipe;
  HANDLE hStdInServerPipe;

  DWORD FormatGetLastError(DWORD WinError = 0xFFFFFFFF);

  BOOL SetCreateProcessAsUserPrivileges(void);

  BOOL CryptData(char *Data,DWORD *DataSize);

  BOOL DecryptData(char *Data,DWORD DataSize);
};

#endif // _COMMANDUTIL_H_