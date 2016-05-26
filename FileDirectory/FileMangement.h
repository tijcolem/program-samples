#ifndef FILEMANGEMENT_H
#define FILEMANGEMENT_H

#pragma once

class FileMangement
{
public:
	FileMangement(const char * TargDir, int mode = 0); 
    FileMangement(CString &TargDir, boost::regex &re); 
	~FileMangement(void);
	void FileMangement::ReSetFileCounter(int i) { TotalFileCount = 0;} 
	int GetFileCounter() { return TotalFileCount;}
	int GetMatchedCount() {return RegExMatchedFileCount;} 
	int GetUnMatchedCount() {return RegExUnMatchedFileCount;} 
	CString GetFileBreakDown() {return FileBreakDown;}
	std::vector<CString> GetDirectoryNames() {return DirectoryNames;} 
	std::vector<std::string> GetFileNames() {return FileNames;} // returns all FileNames in directory
	std::vector<std::string> GetUnMatchedFileNames() {return UnMatchedFileNames;} 
	bool TargetDirFound(); 
	std::string FileGaps(const char * DirString,int Mode = 0, int StartPos = 0, int Length = 0); // Method to determine data outages using file names. 
	void FileCount(const char * DirString); // Counts # of files 
	void FileCountRecursive(const char * DirString);  // Counts # of file and subdirectories' files. 
	bool CopyFiles(const char * SourceDir, const char * DestinationDir); // Copy files from one directory to another
private: 
	int TotalFileCount; 
	int RegExMatchedFileCount; 
	int RegExUnMatchedFileCount;
	std::vector<CString> DirectoryNames;
	CString FileBreakDown; 
	CString TargetDirectory; 
	CString MatchedFileStats; 
	std::vector<std::string> FileNames; 
	std::vector<std::string> UnMatchedFileNames; 

	void BreakDownByPathRecursive(CString &DirString);
	
	void RegExFileMatch(CString &TargDir, boost::regex &re); 
};
#endif 