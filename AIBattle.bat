@echo off 
setlocal enabledelayedexpansion 

dir PlayerAI>AIList.txt

for /f "skip=5 tokens=4,5 delims=. " %%i in (AIList.txt) do (
	if %%j EQU exe (
		for /f "skip=5 tokens=4,5 delims=. " %%k in (AIList.txt) do (
			if %%l EQU exe (
				python sserver.py %%i.%%j vs %%k.%%l
			)
		)
	)
)
pause