#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
; SYSTEMS
^p::
  Run, C:\Program Files (x86)\PuTTY\Putty.exe
;  send, 1 lines{!}{enter}
;  Send, me@testserber
Return
Numpad0 & 1::
  Run, C:\Program Files (x86)\PuTTY\Putty.exe -ssh me@machine002
Return
Numpad0 & 3::
  Run, C:\Program Files (x86)\PuTTY\Putty.exe -ssh me@machine001
Return
