' VBScript to run Vigenere Cipher without showing CMD prompt
Set objShell = CreateObject("WScript.Shell")
strScriptPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
strPythonScript = strScriptPath & "\Vigenere Cipher (Enc&Dec).py"
objShell.Run "pythonw.exe """ & strPythonScript & """", 0, False
