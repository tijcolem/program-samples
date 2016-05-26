// FileDirectoryDlg.cpp : implementation file
//

#include "stdafx.h"
#include "FileDirectory.h"
#include "FileDirectoryDlg.h"
#include "CFolderDialog.h"
#include ".\filedirectorydlg.h"
#ifdef _DEBUG
#define new DEBUG_NEW
#endif
using std::string; 

std::string IntToString(int intValue);  
DWORD WINAPI ScpThread(LPVOID iValue); 
DWORD WINAPI PostResultsThread(LPVOID iValue); 


DWORD WINAPI ScpThread(LPVOID iValue)
{

	std::string SCPCommand = *(string *)iValue; 

	if (system(SCPCommand.c_str()) > 0) { 
	return 1; 
}

  
   return 0;
}


DWORD WINAPI PostResultsThread(LPVOID iValue)
{

	CFileDirectoryDlg *pCFileDirectoryDlg = (CFileDirectoryDlg *)iValue;

	DWORD lpExitCode; 
	char buffer[1000]; 
	int LineCount; 
	float PercentComplete; 
	float NumofFilestoCopy = pCFileDirectoryDlg->NumofFilestoCopy; 
	CString StringPercentComplete; 
	string OutPutText; 
    HWND m_dlghandle = pCFileDirectoryDlg->GetSafeHwnd(); 
	GetExitCodeThread( pCFileDirectoryDlg->hThread1,&lpExitCode); 
    

	while (lpExitCode == STILL_ACTIVE)  {

		std::ifstream FileScpResults ("/temp/results.txt", std::ios::in); 
	
	    LineCount = 0; 
		while (!FileScpResults.eof()) { 
			LineCount++; 
			FileScpResults.getline(buffer, sizeof(buffer)); 
			OutPutText.insert(0, buffer); 
			OutPutText.insert(0, "\r\n");
		}  
 

		PercentComplete =  (float(LineCount)  / NumofFilestoCopy) * 100; 
		if (PercentComplete > 100) {PercentComplete = 100;}
		StringPercentComplete.Format("%.2f", PercentComplete); 


		pCFileDirectoryDlg->m_editResult.SetWindowText(OutPutText.c_str()); 

		 ::SetDlgItemText(m_dlghandle,IDC_RESULT,OutPutText.c_str());
		 ::SetDlgItemText(m_dlghandle,IDC_PERCENT_COMP,StringPercentComplete);
	 
		FileScpResults.close(); 
		OutPutText = ""; 

		Sleep(1000); 
		GetExitCodeThread(pCFileDirectoryDlg->hThread1,&lpExitCode); 
		

	
		}

  
   return 0;
}









struct SMyStruct
{
string FieldDirectoryName;
string ArchiveDirectoryFileType;
string FileFormat; 
int DailyTimeStartPosition; 
string IncludeExclude; 
};

typedef CHashTable<struct SMyStruct> CMyStructHashT;

CMyStructHashT     MyHashTable;
struct SMyStruct * pStruct = NULL;

// CAboutDlg dialog used for App About

class CAboutDlg : public CDialog
{
public:
	CAboutDlg();

// Dialog Data
	enum { IDD = IDD_ABOUTBOX };

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

// Implementation
protected:
	DECLARE_MESSAGE_MAP()
};

CAboutDlg::CAboutDlg() : CDialog(CAboutDlg::IDD)
{
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialog)
END_MESSAGE_MAP()


// CFileDirectoryDlg dialog


CFileDirectoryDlg::CFileDirectoryDlg(CWnd* pParent /*=NULL*/)
	: CDialog(CFileDirectoryDlg::IDD, pParent)
{
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void CFileDirectoryDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	DDX_Control(pDX, IDC_RESULT, m_editResult);
	DDX_Control(pDX, IDC_SITEID, CEdit_SiteID);
	DDX_Control(pDX, IDC_LIST1, m_CListBox_Sites);
	DDX_Control(pDX, IDC_DRIVES, SysDrives_CComboBox);
	DDX_Control(pDX, IDC_PERCENT_COMP, m_IDC_Precent_Complete);
}

BEGIN_MESSAGE_MAP(CFileDirectoryDlg, CDialog)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	//}}AFX_MSG_MAP
	ON_BN_CLICKED(IDC_READ_DIR, OnBnClickedReadDir)
	ON_BN_CLICKED(IDC_PROCESS, OnBnClickedProcess)
	ON_BN_CLICKED(IDC_FINDUNKOWNDIR, OnBnClickedFindunkowndir)
	ON_BN_CLICKED(IDC_MATCHFILES, OnBnClickedMatchfiles)
	ON_BN_CLICKED(IDC_COPYFILES, OnBnClickedCopyfiles)
	ON_BN_CLICKED(IDC_FILEGAPS, OnBnClickedFilegaps)
	ON_EN_CHANGE(IDC_SITEID, OnEnChangeSiteid)
	ON_BN_CLICKED(IDC_BUTTON1, OnBnClickedButton1)
	ON_BN_CLICKED(IDC_REMOVESITE, OnBnClickedRemovesite)
	ON_CBN_SELENDOK(IDC_DRIVES, OnCbnEditupdateDrives)
END_MESSAGE_MAP()


// CFileDirectoryDlg message handlers

BOOL CFileDirectoryDlg::OnInitDialog()
{
	CDialog::OnInitDialog();

	// Add "About..." menu item to system menu.

	// IDM_ABOUTBOX must be in the system command range.
	ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
	ASSERT(IDM_ABOUTBOX < 0xF000);

	CMenu* pSysMenu = GetSystemMenu(FALSE);
	if (pSysMenu != NULL)
	{
		CString strAboutMenu;
		strAboutMenu.LoadString(IDS_ABOUTBOX);
		if (!strAboutMenu.IsEmpty())
		{
			pSysMenu->AppendMenu(MF_SEPARATOR);
			pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
		}
	}

	// Set the icon for this dialog.  The framework does this automatically
	//  when the application's main window is not a dialog
	SetIcon(m_hIcon, TRUE);			// Set big icon
	SetIcon(m_hIcon, FALSE);		// Set small icon

	// TODO: Add extra initialization here
	FilesAreClean = false; 
	SetSystemDrives();
	
	return TRUE;  // return TRUE  unless you set the focus to a control
}

void CFileDirectoryDlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX)
	{
		CAboutDlg dlgAbout;
		dlgAbout.DoModal();
	}
	else
	{
		CDialog::OnSysCommand(nID, lParam);
	}
}

// If you add a minimize button to your dialog, you will need the code below
//  to draw the icon.  For MFC applications using the document/view model,
//  this is automatically done for you by the framework.

void CFileDirectoryDlg::OnPaint() 
{
	if (IsIconic())
	{
		CPaintDC dc(this); // device context for painting

		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);

		// Center icon in client rectangle
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// Draw the icon
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialog::OnPaint();
	}
}

// The system calls this function to obtain the cursor to display while the user drags
//  the minimized window.
HCURSOR CFileDirectoryDlg::OnQueryDragIcon()
{
	return static_cast<HCURSOR>(m_hIcon);
}



void CFileDirectoryDlg::OnBnClickedReadDir()
{

bool Success = true; 

MyHashTable.RemoveAllKey(true);
	
for (int i = 0; i < m_CListBox_Sites.GetCount(); i++) { 

		char buffer[MAX_PATH +1]; 
		string tmpString[10];
		std::ifstream File ("DirectoryList.txt", std::ios::in); 
		
		File.getline(buffer, sizeof(buffer)); // check for correct file using header
		boost::regex re("Field Path.*"); 
		
		if(boost::regex_match(buffer, re)) {

		  CString SiteID; 


		  m_CListBox_Sites.GetText(i, SiteID); 
  
		  while (!File.eof()) { 
				File.getline(buffer, sizeof(buffer)); 
  
				char * pch;
  
				pch = strtok(buffer,",");
 
				int i = 0; 
				while (pch != NULL)  { 
					tmpString[i] = pch; 
					pch = strtok (NULL, ",");
					i++; 
				}
				i = 0; 
  
				pStruct = new SMyStruct;	
				if(pStruct){

					CString tmp_CString; 
					CEdit_SiteID.GetWindowText(tmp_CString); 
					tmpString[0].append("\\"); 
					tmpString[0].append(SiteID); 

					tmpString[1].append("/"); 
					tmpString[1].append(SiteID); 
	
					pStruct->FieldDirectoryName = tmpString[0]; 
					pStruct->ArchiveDirectoryFileType = tmpString[1]; 
					pStruct->FileFormat = tmpString[2]; 
					pStruct->DailyTimeStartPosition = atoi(tmpString[4].c_str()); 
					pStruct->IncludeExclude = tmpString[5]; 
					

					MyHashTable.AddKey(tmpString[0], pStruct);
				}
				else {
					Success = false; 
				}

		  }
		 
		} 
		else {
	   MessageBox(buffer); 
		}
  }
 if(Success) {
	MessageBox("Site's loaded succesfully");
	}
	else{
		MessageBox("Site's failed to load. Please check config file"); 
	}
	


}



void CFileDirectoryDlg::OnBnClickedProcess()
{

if(TargetRootPath.IsEmpty()){
	MessageBox("Target Drive not selected"); 
	return; 
}


CString str_WindowText; 


FileMangement flmgmet(TargetRootPath,0); 


str_WindowText.Append("Total Number of Files in Target Root Path and Sub directories: "); 
int i = flmgmet.GetFileCounter();
str_WindowText.Append(IntToString(i).c_str()); 
str_WindowText.Append("\r\n"); 
str_WindowText.Append(flmgmet.GetFileBreakDown()); 
str_WindowText.Append("\r\n");
str_WindowText.Append("\r\n");
str_WindowText.Append("All Files and Directories");
str_WindowText.Append("\r\n");
str_WindowText.Append("\r\n");

std::vector<CString> DirNames = flmgmet.GetDirectoryNames(); 

for (std::vector<CString>::iterator Diriter = DirNames.begin(); Diriter != DirNames.end(); ++Diriter) {

	str_WindowText.Append(*Diriter);
	str_WindowText.Append("\r\n"); 
	
	FileMangement FilesinDir(*Diriter,1);

	std::vector<string> FileNames = FilesinDir.GetFileNames(); 

	for (std::vector<string>::iterator Fileiter = FileNames.begin(); Fileiter != FileNames.end(); ++Fileiter) { 

    
    std::string FileName = *Fileiter;
    
	str_WindowText.Append(FileName.c_str());
	str_WindowText.Append("\r\n"); 

	}

}
m_editResult.SetWindowText(str_WindowText); 
UpdateData(FALSE);

}


void CFileDirectoryDlg::OnBnClickedFindunkowndir()
{
	
	
if(TargetRootPath.IsEmpty()){
	MessageBox("Target Drive not selected"); 
	return; 
}
	
	
	
	// Look for directories in target not in file listing. 



FileMangement flmgmet(TargetRootPath,0); 

std::vector<CString> DirNames = flmgmet.GetDirectoryNames(); 

CString PathFound; 

CString PathNotFound; 

int DirMatch = 0; 

for (std::vector<CString>::iterator DirIter = DirNames.begin(); DirIter != DirNames.end(); ++DirIter) { 

	std::string DirString = *DirIter;
	
	 for(CMyStructHashT::iterator Hashiter = MyHashTable.begin(); Hashiter != MyHashTable.end(); ++Hashiter ) {
		size_t pos; 
		size_t found; 

		std::string HashDirString = Hashiter->c_str(); 

		pos = DirString.find("\\");

		found = HashDirString.find(DirString.substr(pos+1)); 

		if (found != string::npos) {
			DirMatch = 1; 
		}
			   
	 }
	 if(DirMatch == 1){

		 PathFound.Append("\r\n");
		 PathFound.Append(" Directory found: ");
		 PathFound.Append(DirString.c_str());
		 DirMatch = 0; 


	 }
	 else{
		  PathNotFound.Append("\r\n");
		  PathNotFound.Append(" UnKnownDirectory: ");
		  PathNotFound.Append(DirString.c_str()); 
		  CString strFormat; 
		  FileMangement DirMatched(DirString.c_str(),1);
		  strFormat.Format("  %d",DirMatched.GetFileCounter()); 
		  PathNotFound.Append(strFormat); 

	 }

}

PathFound.Append("\r\n"); 
PathFound.Append(PathNotFound); 



	  m_editResult.SetWindowText(PathFound); 
		   UpdateData(FALSE);


}






void CFileDirectoryDlg::SetSystemDrives() {

int dr_type=99;
char dr_avail[256];
char *temp=dr_avail;
        
      
GetLogicalDriveStrings(sizeof(dr_avail),dr_avail);
while(*temp!=NULL) { 
                
	dr_type=GetDriveType(temp);
	SysDrives_CComboBox.AddString(temp);

                temp += lstrlen(temp) +1; 
        }

}

void CFileDirectoryDlg::OnBnClickedMatchfiles()
{




if(TargetRootPath.IsEmpty()){
	MessageBox("Target Drive not selected"); 
	return; 
}



bool AllFilesMatched = true; 
CString str_WindowText; 
	
	
CMyStructHashT::iterator iter = MyHashTable.begin();


  while(iter != MyHashTable.end())
  {

	  
	   pStruct = MyHashTable.GetMember(iter->c_str()); 

	 
	   if(pStruct) {
            
		   CString DirString = TargetRootPath + pStruct->FieldDirectoryName.c_str(); 
		 
		  
		   boost::regex re(pStruct->FileFormat,  boost::regex_constants::icase); 
		   
		   FileMangement flmgmet(DirString, re); 
		
		   
				if (flmgmet.TargetDirFound()) { 
			

					str_WindowText.Append(DirString);
					str_WindowText.Append("\r\n");
					str_WindowText.Append("	Matched Files: ");
				
					str_WindowText.Append(IntToString(flmgmet.GetMatchedCount()).c_str());
					str_WindowText.Append("\r\n");

					str_WindowText.Append("	UnMatched Files: ");
					str_WindowText.Append(IntToString(flmgmet.GetUnMatchedCount()).c_str());
					str_WindowText.Append("\r\n");


					if (flmgmet.GetUnMatchedCount() > 0) {

						AllFilesMatched = false;
					
					
						std::vector<string> FileNames = flmgmet.GetUnMatchedFileNames(); 
						for (std::vector<string>::iterator iter = FileNames.begin(); iter != FileNames.end(); ++iter) {
						
							str_WindowText.Append("\t\t"); 
							
							str_WindowText.Append(iter->c_str());
							
							str_WindowText.Append("\r\n");
						}
					
					}
				
				}
	   }
	    iter++;
 } 
   m_editResult.SetWindowText(str_WindowText); 
   UpdateData(FALSE);

  if (!AllFilesMatched) {
	  MessageBox("Found files that are UnMatched!");
	  FilesAreClean = false; 
  }
  else { 
	  MessageBox("Files are clean");
	  FilesAreClean = true; 
  } 

}



void CFileDirectoryDlg::OnBnClickedCopyfiles()
{

string FieldDirPath; 
CString FileCount; 
NumofFilestoCopy = 0;


if(TargetRootPath.IsEmpty()){
	MessageBox("Target Drive not selected"); 
	return; 
}

//if(!FilesAreClean) { 
//	MessageBox("There are UnMatched files on the target drive, or you have not Matched files yet.");
//	return; 
//}


if (MessageBox("You are about to copy the contents of the target drive to the Archive. Proceed?","SCP Copy",MB_YESNO) == IDNO) { 
	return;
}


string SCPCommand = "Winscp.com \"dms7:R@dar1ove@psdobs.psd.esrl.noaa.gov\" /script=/temp/ScpScript.txt > /temp/results.txt "; 

string Script = "option batch on\r\n";

for(CMyStructHashT::iterator iter = MyHashTable.begin(); iter != MyHashTable.end(); ++iter ) { // looping through directories in config file 

   pStruct = MyHashTable.GetMember(iter->c_str()); 

   if(pStruct) {


	   if(pStruct->IncludeExclude == "Y") {  // only copy files that are included in config file. 


			FieldDirPath = TargetRootPath; 
			FieldDirPath.append(pStruct->FieldDirectoryName.c_str()); 

			FileMangement flmngr(FieldDirPath.c_str(),1); 
           
			if (flmngr.GetFileCounter() > 0) { 	// checking for files 

				NumofFilestoCopy +=  flmngr.GetFileCounter(); 
			     
				 Script.append("cd "); 
				 Script.append(pStruct->ArchiveDirectoryFileType);  
				 Script.append("\r\n"); 
	
			 }
		}
   }

}

CString msgbox; 

msgbox.Format("%d", NumofFilestoCopy); 

MessageBox(msgbox); 

Script.append("exit"); 

std::ofstream File("/temp/ScpScript.txt", std::ios::out);

File << Script.c_str(); 
File.close(); 


//CommandUtil ScpCommandUtil("Secure Copy"); 

//ScpCommandUtil.RunCommand("Winscp.com \"dms7:R@dar1ove@psdobs.psd.esrl.noaa.gov\" /script=/temp/ScpScript.txt > /temp/results.txt "); 

if (system(SCPCommand.c_str()) > 0) { 
	MessageBox("Error issuing SCP command. Please check WinSCP is installed.");
}

m_editResult.SetWindowText(SCPCommand.c_str()); 

UpdateData(FALSE);


string ErrorChck; 
char buffer[1000]; 
std::ifstream ScpFile ("/temp/results.txt", std::ios::in); 
string OutPutText = "Checking directories\r\n\r\n"; 
bool Success = true; 
		
while (!ScpFile.eof()) { // looking for directories that do not exist in the archive.  

	ScpFile.getline(buffer, sizeof(buffer)); 
	ErrorChck = buffer; 
	size_t found = ErrorChck.find("Error"); 
	if(found != string::npos) {

			Success = false; 
			OutPutText.append(ErrorChck); 
			OutPutText.append("\r\n"); 
	}
}
ScpFile.close();  

m_editResult.SetWindowText(OutPutText.c_str()); 

   UpdateData(FALSE);



if (Success) { 



	SCPCommand = "Winscp.com \"dms7:R@dar1ove@psdobs.psd.esrl.noaa.gov\" /script=/temp/ScpRunScript.txt > /temp/results.txt "; 

	string ScpRunScript = "option batch on\r\noption confirm off\r\n";

	for(CMyStructHashT::iterator iter = MyHashTable.begin(); iter != MyHashTable.end(); ++iter ) { // looping through directories in config file 

		pStruct = MyHashTable.GetMember(iter->c_str()); 

		if(pStruct) {

			if(pStruct->IncludeExclude == "Y") { 

				string FieldDirString = TargetRootPath; 
				FieldDirString.append(pStruct->FieldDirectoryName.c_str()); 

				FileMangement flmngr(FieldDirString.c_str(),1); 
           
				if (flmngr.GetFileCounter() > 0) { 	// checking for files 

					//MessageBox("About to Copy"); 
			
					ScpRunScript.append("cd "); 
					ScpRunScript.append(pStruct->ArchiveDirectoryFileType); 
					ScpRunScript.append("\r\n"); 
					ScpRunScript.append("put ");
				    ScpRunScript.append(TargetRootPath); 
				    ScpRunScript.append(pStruct->FieldDirectoryName);
				    ScpRunScript.append("\\*.*"); 
					ScpRunScript.append("\r\n"); 
			
				}
			}
		}

	}

	ScpRunScript.append("exit"); 

	std::ofstream ScpRunFile("/temp/ScpRunScript.txt", std::ios::out);

	ScpRunFile << ScpRunScript.c_str(); 
	ScpRunFile.close(); 

	m_editResult.SetWindowText(ScpRunScript.c_str()); 

	UpdateData(FALSE);

    DWORD dwGenericThread1;

	hThread1 = CreateThread(NULL,0,ScpThread,&SCPCommand,0,&dwGenericThread1);

	  if(hThread1 == NULL)
      {
            DWORD dwError = GetLastError();
            MessageBox("SCM:Error in Creating thread");
            return;
       }

   HANDLE hThread2; 
   DWORD dwGenericThread2;
   hThread2 = CreateThread(NULL,0,PostResultsThread,this,0,&dwGenericThread2);

     if(hThread2 == NULL)
      {
            DWORD dwError = GetLastError();
            MessageBox("SCM:Error in Creating thread");
            return;
       }


   

//	if (system(SCPCommand.c_str()) > 0) { 
//		MessageBox("Error issuing SCP command");
//	}
//	else 
//	 { 
	OutPutText.clear(); 
	string ScpResults = ""; 
	
	OutPutText.append("Results of SCP transfer:\n\r\n\r"); 
	
 //   DWORD lpExitCode; 
//	GetExitCodeThread(hThread1,&lpExitCode); 

	/*
	
	while (lpExitCode == STILL_ACTIVE)  {

		std::ifstream FileScpResults ("/temp/results1.txt", std::ios::in); 
	
		while (!FileScpResults.eof()) { 

			FileScpResults.getline(buffer, sizeof(buffer)); 
			ScpResults = buffer; 

			OutPutText.append(ScpResults); 
			OutPutText.append("\r\n"); 
		}  

		OutPutText.append(""); 

	m_editResult.SetWindowText(OutPutText.c_str()); 

	UpdateData(FALSE);


	Sleep(3000); 
	FileScpResults.close(); 
	OutPutText = ""; 
	GetExitCodeThread(hThread1,&lpExitCode); 
	}
	
*/



//	}

}
else {
MessageBox("Can't copy until directories have been added"); 
}


}

void CFileDirectoryDlg::OnBnClickedFilegaps() {

	if(TargetRootPath.IsEmpty()){
	MessageBox("Target Drive not selected"); 
	return; 
}

	
string FileGaps; 
CString str_WindowText = "Searching for gaps in daily files.\r\n\r\n"; 

CMyStructHashT::iterator iter = MyHashTable.begin();


  while(iter != MyHashTable.end()) {
	  
	   pStruct = MyHashTable.GetMember(iter->c_str()); 


	   if(pStruct) {

		   if (pStruct->DailyTimeStartPosition >= 0) {
            
				CString DirString = TargetRootPath + pStruct->FieldDirectoryName.c_str(); 

			    FileMangement flmgmet(DirString, 0); 
		   
				if (flmgmet.TargetDirFound()) { 

					str_WindowText.Append(DirString); 
					str_WindowText.Append(": \r\n"); 

					FileGaps = flmgmet.FileGaps(DirString,0,pStruct->DailyTimeStartPosition,5); 

					str_WindowText.Append("File Gaps: \r\n");
					str_WindowText.Append(FileGaps.c_str()); 
					str_WindowText.Append("\r\n");
				
				}
		   }
		
	   }
	    iter++;
 }
m_editResult.SetWindowText(str_WindowText); 
					UpdateData(FALSE);


}



void CFileDirectoryDlg::OnEnChangeSiteid()
{
	
	CString tmp_String; 
	CEdit_SiteID.GetWindowText(tmp_String); 
	if (strlen(tmp_String) > 3) {
		MessageBox("Error, SiteID can only be 3 characters"); 
		CEdit_SiteID.SetWindowText(""); 
	}
UpdateData(true); 
}

void CFileDirectoryDlg::OnBnClickedButton1()
{
	CString Site; 
	UpdateData();
	CEdit_SiteID.GetWindowText(Site); 
	UpdateData(false); 
	m_CListBox_Sites.AddString(Site); 



}

void CFileDirectoryDlg::OnBnClickedRemovesite()
{
        int index;
        CString strText;
        index = m_CListBox_Sites.GetCurSel();
        m_CListBox_Sites.DeleteString(index);
		
   
}



void CFileDirectoryDlg::OnCbnEditupdateDrives()
{
	int index;
	CString DriveSelection; 
	index = SysDrives_CComboBox.GetCurSel();
	SysDrives_CComboBox.GetLBText(index,DriveSelection); 
	TargetRootPath = DriveSelection;
}



std::string IntToString(int intValue) {
  char *myBuff;
  string strRetVal;


  myBuff = new char[100];


  memset(myBuff,'\0',100);


  itoa(intValue,myBuff,10);


  strRetVal = myBuff;
  

  delete[] myBuff;

  return(strRetVal);
}















