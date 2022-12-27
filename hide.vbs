Set oShell = CreateObject("Wscript.Shell")
oShell.CurrentDirectory = "C:\Users\Dric\PycharmProjects\PSE-Webscraper"
Dim strArgs
strArgs = "cmd /c run_script.bat"
oShell.Run strArgs, 0, false