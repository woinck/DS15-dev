@echo off 
setlocal enabledelayedexpansion 

dir PlayerAI>AIList.txt

 for /f "skip=13 tokens=4,5 delims=. " %%i in (AIList.txt) do (
 	if %%j EQU exe (
		for /f "skip=5 tokens=4,5 delims=. " %%k in (AIList.txt) do (
			if %%l EQU exe (
			    if %%i NEQ %%k (
					python sserver.py PlayerAI/%%i.exe PlayerAI/%%k.exe map.map
				)
			)
		)
 	)
 )
pause