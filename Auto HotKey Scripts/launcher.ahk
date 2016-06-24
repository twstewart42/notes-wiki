#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
!p::
  Run, C:\Program Files (x86)\PuTTY\Putty.exe 
  WinWaitActive,  PuTTY Configuration
  Send, stewt318@
Return
!c::
  Run, C:\Program Files (x86)\Google\Chrome\Application\chrome.exe 
Return
!n::
  Run, C:\Program Files\NetApp\OnCommand System Manager\SystemManager.exe
Return
!r::
  Run, C:\Windows\system32\mstsc.exe
Return
!v::
  Run, C:\Program Files (x86)\VMware\Infrastructure\Virtual Infrastructure Client\Launcher\VpxClient.exe
Return
!u::
  Run, C:\Users\stewt318\Desktop\rufus-2.2.exe
Return
!l::
  Run, C:\Users\stewt318\Desktop\LdapAdmin.exe
Return
!f::
  Run, C:\Program Files (x86)\Mozilla Firefox\firefox.exe
Return
!w::
  Run, C:\Program Files (x86)\WinSCP\WinSCP.exe
Return
NumpadDot & NumpadSub::
  SoundSet -10
Return
NumpadDot & NumpadAdd::
  SoundSet +10
Return
NumpadDot & NumpadMult::
  SoundSet, +1, , mute
Return