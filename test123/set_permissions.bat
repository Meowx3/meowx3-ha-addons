@echo off
icacls "c:\Users\tsniv\Documents\VS Code\qwen3-code-test\meowx3-ha-addons\test123\rootfs\usr\bin\gps_echo" /grant Users:(RX)
icacls "c:\Users\tsniv\Documents\VS Code\qwen3-code-test\meowx3-ha-addons\test123\rootfs\etc\services.d\test123\run" /grant Users:(RX)
icacls "c:\Users\tsniv\Documents\VS Code\qwen3-code-test\meowx3-ha-addons\test123\rootfs\etc\services.d\test123\finish" /grant Users:(RX)
icacls "c:\Users\tsniv\Documents\VS Code\qwen3-code-test\meowx3-ha-addons\test123\rootfs\etc\cont-init.d\01-gpsd" /grant Users:(RX)
