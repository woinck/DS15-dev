@echo off 
setlocal enabledelayedexpansion 

dir FinalAI>AIList.txt

 rem for /f "skip=7 tokens=4,5 delims=. " %%i in (AIList.txt) do (
 rem	if %%j EQU exe (
		for /f "skip=7 tokens=4,5 delims=. " %%k in (AIList.txt) do (
			if %%l EQU exe (
			    if %%i NEQ %%k (
					python sserver.py FinalAI/WXYZ_new.exe FinalAI/%%k.exe Map_final6.map
				)
			)
		)

		for /f "skip=7 tokens=4,5 delims=. " %%k in (AIList.txt) do (
			if %%l EQU exe (
			    if %%i NEQ %%k (
					python sserver.py FinalAI/%%k.exe FinalAI/WXYZ_new.exe Map_final6.map
				)
			)
		)

 rem	)
 rem )
pause