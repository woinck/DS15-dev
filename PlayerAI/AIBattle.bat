@echo off 
setlocal enabledelayedexpansion 

dir>AIList.txt

for /f "skip=5 tokens=4,5 delims=. " %%i in (AIList.txt) do (
	if %%j EQU exe (
		for /f "skip=5 tokens=4,5 delims=. " %%k in (AIList.txt) do (
			if %%l EQU exe (
				echo %%i.%%j vs %%k.%%l
				rem RUN GAME HERE!!!!!!!!!!!!
			)
		)
	)
)
pause