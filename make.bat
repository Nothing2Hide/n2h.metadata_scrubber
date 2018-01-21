@ECHO OFF

if "%1" == "" goto help

if "%1" == "help" (
	:help
	echo.Please use make ^<target^> where ^<target^> is one of
	echo.  pytest     run pytest
	echo.  flake8     run flake8 scan
	echo.  installer  build Windows installer
	goto end
)


if "%1" == "pytest" (
	echo."==== Running pytest ===="
	bin\py.test.exe --cov=src --cov-report=term-missing tests
	if errorlevel 1 exit /b 1
	goto end
)

if "%1" == "flake8" (
	echo."==== Running flake8 ===="
	bin\flake8.exe src
	if errorlevel 1 exit /b 1
	goto end
)

if "%1" == "installer" (
	echo."==== Building installer ===="
	pyinstaller.exe -p src\n2h -F -n scrubbertk src\n2h\metadata_scrubber\gui.py
	if errorlevel 1 exit /b 1
	goto end
)

:end
