@echo off
rem Build dlrl.exe with the Japanese layer.
rem Needs Git, CMake and Visual Studio 2022/2026 (Desktop C++). Output: build\dlrl\build-win\Release
rem build.bat test: test build with DLRL_DUMP_* debug output (DLRL_JA_TEST). Output: build\dlrl\build-win-test\Release
rem The test build is not for distribution.
setlocal
set ROOT=%~dp0..
set WORK=%ROOT%\build\dlrl
set UPSTREAM=https://github.com/hasseily/Deathlord-Relorded.git
set COMMIT=f5c453fcf004324f07f9a71428cf820ee5cc1a4b
set BDIR=build-win
set OPT=-DDLRL_JA_TEST=OFF
if "%1"=="test" set BDIR=build-win-test
if "%1"=="test" set OPT=-DDLRL_JA_TEST=ON

if not exist "%WORK%\.git" git clone %UPSTREAM% "%WORK%" || exit /b 1
pushd "%WORK%"
git fetch -q origin %COMMIT% 2>nul
git checkout -q -f %COMMIT% || exit /b 1
git clean -q -f -d -e build-win -e build-win-test
git apply --whitespace=nowarn "%ROOT%\patch\deathlord-relorded-ja.patch" || exit /b 1
if not exist "Deathlord-Relorded\Assets\ja" mkdir "Deathlord-Relorded\Assets\ja"
copy /y "%ROOT%\data\ja\*.json" "Deathlord-Relorded\Assets\ja\" >nul
copy /y "%ROOT%\data\fonts\*" "assets\pp\assets\" >nul
cmake -S . -B %BDIR% -A x64 %OPT% || exit /b 1
cmake --build %BDIR% --config Release --target dlrl || exit /b 1
popd
echo Built: %WORK%\%BDIR%\Release\dlrl.exe
