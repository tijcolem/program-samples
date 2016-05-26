// FileDirectoryDlg.h : header file
//

#pragma once
#include "afxwin.h"

// CFileDirectoryDlg dialog
class CFileDirectoryDlg : public CDialog
{
// Construction
public:
	CFileDirectoryDlg(CWnd* pParent = NULL);	// standard constructor

// Dialog Data
	enum { IDD = IDD_FILEDIRECTORY_DIALOG };

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV support


// Implementation
protected:
	HICON m_hIcon;
	
	// Generated message map functions
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()
public:
	afx_msg void OnBnClickedReadDir();
	afx_msg void OnBnClickedProcess();
	CString CFileDirectoryDlg::FileBreakDown(CString &DirString);
	void CFileDirectoryDlg::SetSystemDrives(); 
	CEdit m_editResult;
	CEdit CEdit_SiteID;
	CListBox m_CListBox_Sites;
	CComboBox SysDrives_CComboBox;
	HANDLE hThread1; 
	int NumofFilestoCopy; 
	CEdit m_IDC_Precent_Complete;

private:
	int TotalFileCount; 
	
	CString TargetRootPath;
	bool FilesAreClean; 
	
public:
	afx_msg void OnBnClickedFindunkowndir();
	afx_msg void OnBnClickedMatchfiles();
	afx_msg void OnBnClickedCopyfiles();
	afx_msg void OnBnClickedFilegaps();

	afx_msg void OnEnChangeSiteid();
	
	afx_msg void OnBnClickedButton1();
	afx_msg void OnBnClickedRemovesite();
	afx_msg void OnCbnSelchangeCombo1();

	afx_msg void OnCbnSelchangeDrives();
	afx_msg void OnCbnSelChangeDrives();
	afx_msg void OnCbnEditupdateDrives();
	
	
};
