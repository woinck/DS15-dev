@echo off 
setlocal enabledelayedexpansion 

dir FinalAI>AIList.txt

for /f "skip=12 tokens=4,5 delims=. " %%i in (AIList.txt) do (
	if %%j EQU exe (
		for /f "skip=13 tokens=4,5 delims=. " %%k in (AIList.txt) do (
			if %%l EQU exe (
			    if %%i NEQ %%k (
					python sserver.py FinalAI/%%i.exe FinalAI/%%k.exe Map_final3.map
				)
			)
		)
	)
)
pause