#include "stdafx.h"
#include ".\filemangement.h"


/*  Two Constructors:
	1.  Two Arguments. Target Directory, and mode. Two Modes. Mode 1 = Non recursive. Does not look in sub-directories. 
		Mode 0 (default) looks in sub-directories. 
    2.  Two Arguments. Target Directory, and regular expression representing the file name. 

*/


FileMangement::FileMangement(const char * TargDir, int mode){
	TotalFileCount = 0;
	RegExMatchedFileCount = 0; 
	RegExUnMatchedFileCount = 0; 
	TargetDirectory = TargDir; 


	if(TargetDirFound()) {
		if (mode == 0) { 
		FileCountRecursive(TargetDirectory); 
		BreakDownByPathRecursive(TargetDirectory); 
		}
		if (mode == 1) { 
		FileCount(TargetDirectory);
		TargetDirectory = TargDir;
		}
	}
	
}

FileMangement::FileMangement(CString &TargDir, boost::regex &re) { 
	
	TotalFileCount = 0;
	RegExMatchedFileCount = 0; 
	RegExUnMatchedFileCount = 0; 

	if(TargetDirFound()) {
		TargetDirectory = TargDir;
		FileCount(TargetDirectory);
		RegExFileMatch(TargetDirectory, re); 
	}

}

FileMangement::~FileMangement(void)
{
}

bool FileMangement::TargetDirFound() {

	DIR * pDir = opendir(TargetDirectory);
	if(pDir)
		 return true; 
	else
		return false; 
}




void FileMangement::FileCountRecursive(const char * DirString) {
	CString RcurPath; 
	struct dirent *pent = NULL; 
	DIR * pDir = opendir(DirString);
	
	if(pDir){
			
		while ((pent=readdir(pDir))) {
					
			if(pent->data.dwFileAttributes != FILE_ATTRIBUTE_DIRECTORY) {
						
				TotalFileCount++; 
			}
			else if (strcmp(pent->d_name, ".") != 0 && strcmp(pent->d_name, "..") != 0) {
			RcurPath.Append(DirString); 
			RcurPath.Append("\\");
			RcurPath.Append(pent->d_name);
			FileCountRecursive(RcurPath);
			RcurPath = ""; 
			}
		}
		closedir(pDir);
	}
}


	

void FileMangement::FileCount(const char * DirString) {
	
	struct dirent *pent = NULL; 
	DIR * pDir = opendir(DirString);
	
	if(pDir){
			
		while ((pent=readdir(pDir))) {
					
			if(pent->data.dwFileAttributes != FILE_ATTRIBUTE_DIRECTORY) {
						
				TotalFileCount++; 
				FileNames.push_back(pent->d_name); 
			}
		}	
		closedir(pDir);
	}


}




void FileMangement::BreakDownByPathRecursive(CString &DirString) {
	CString RcurPath; 
	CString FileCounterFormat; 
	struct dirent *pent = NULL; 
	DIR * pDir = opendir(DirString);
	int FileCounter = 0; 
	if(pDir){
			
		
		while ((pent=readdir(pDir))) {
					
			if(pent->data.dwFileAttributes != FILE_ATTRIBUTE_DIRECTORY) {
						
				FileCounter++; 
			}
			else if (strcmp(pent->d_name, ".") != 0 && strcmp(pent->d_name, "..") != 0) {
			RcurPath.Append(DirString); 
			RcurPath.Append("\\");
			RcurPath.Append(pent->d_name);
			BreakDownByPathRecursive(RcurPath);
			RcurPath = ""; 
			}
		
		}
		 DirectoryNames.push_back(DirString); 

			FileBreakDown.Append(DirString);
			FileBreakDown.Append(": "); 
			FileCounterFormat.Format("%d", FileCounter); 
			FileBreakDown.Append(FileCounterFormat); 
			FileBreakDown.Append("\r\n"); 
		closedir(pDir);
	}
}



void FileMangement::RegExFileMatch(CString &TargDir, boost::regex &re) {

			struct dirent *pent = NULL; 
			
			DIR * pDir = opendir(TargDir);
			if(pDir){
			
				while ((pent=readdir(pDir))) {
					
					 if(pent->data.dwFileAttributes != FILE_ATTRIBUTE_DIRECTORY) {
						
						if(!boost::regex_match(pent->d_name, re)) {
					
							RegExUnMatchedFileCount++; 	
							UnMatchedFileNames.push_back(pent->d_name); 
						}
						else
							RegExMatchedFileCount++; 
					}
				}
			
				closedir(pDir);
			}

}

				
			


bool FileMangement::CopyFiles(const char * SourceDir, const char * DestinationDir) {
	

	bool Success = true; 
	

	struct dirent *pent = NULL; 
	DIR * pDir = opendir(SourceDir);
	
	if(pDir){
			
		while ((pent=readdir(pDir))) {
					
			if(pent->data.dwFileAttributes != FILE_ATTRIBUTE_DIRECTORY) {

				std::string SourceDirectory = SourceDir; 
				SourceDirectory.append("\\"); 
				SourceDirectory.append(pent->d_name); 
				
				std::string DestinationDirectory = DestinationDir; 
				DestinationDirectory.append("\\"); 
				DestinationDirectory.append(pent->d_name); 


				if(!CopyFile(SourceDirectory.c_str(), DestinationDirectory.c_str(), TRUE)) {
					 Success = false; 
				}


			}
		}	
		closedir(pDir);
	}
	else{ 
		Success = false; 
	}


	
return Success;

}



std::string FileMangement::FileGaps(const char * DirString, int Mode, int StartPos, int Length) {

	std::string ReturnString = ""; 
	int FileCounter = 0; 
	std::string StartTime = ""; 
	std::string BeginFileName; 
	std::string EndFileName; 

	int int_StartTime; 

	std::string str_temp; 

	struct dirent *pent = NULL; 
	DIR * pDir = opendir(DirString);
	
	if(pDir){
			
		while ((pent=readdir(pDir))) {
					
			if(pent->data.dwFileAttributes != FILE_ATTRIBUTE_DIRECTORY && (strlen(pent->d_name) >= (Length + StartPos))) {
				
					str_temp = pent->d_name; 
						
					if (FileCounter == 0) {
				
						StartTime = str_temp.substr(StartPos,Length); 

						int_StartTime = atoi(StartTime.c_str());  

						FileCounter++; 
					}
					else {
							int_StartTime += 1; 

							StartTime = str_temp.substr(StartPos,Length); 

							int FileTime = atoi(StartTime.c_str()); 
							
							size_t pos = StartTime.find("001"); 

							if(pos == std::string::npos) {
	
								if (int_StartTime != FileTime) {

									ReturnString.append(BeginFileName); 
									ReturnString.append(" TO "); 
									ReturnString.append(str_temp); 
									ReturnString.append("\r\n"); 

									int_StartTime = FileTime; 
								}
							}
							else{
									int_StartTime = FileTime;
							}
					
							BeginFileName = pent->d_name;
					}
				
			}
		
		}
	}	
		closedir(pDir);

return ReturnString; 
}