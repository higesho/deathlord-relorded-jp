@echo off
rem Build dlrl.exe with the Japanese layer.
rem Needs Git, CMake and Visual Studio 2022/2026 (Desktop C++). Output: build\dlrl\build-win\Release
setlocal
set ROOT=%~dp0..
set WORK=%ROOT%\build\dlrl
set UPSTREAM=https://github.com/hasseily/Deathlord-Relorded.git
set COMMIT=f5c453fcf004324f07f9a71428cf820ee5cc1a4b

if not exist "%WORK%\.git" git clone %UPSTREAM% "%WORK%" || exit /b 1
pushd "%WORK%"
git fetch -q origin %COMMIT% 2>nul
git checkout -q -f %COMMIT% || exit /b 1
git clean -q -f -d -e build-win
git apply --whitespace=nowarn "%ROOT%\patch\deathlord-relorded-ja.patch" || exit /b 1
if not exist "Deathlord-Relorded\Assets\ja" mkdir "Deathlord-Relorded\Assets\ja"
copy /y "%ROOT%\data\ja\*.json" "Deathlord-Relorded\Assets\ja\" >nul
copy /y "%ROOT%\data\fonts\*" "assets\pp\assets\" >nul
cmake -S . -B build-win -A x64 || exit /b 1
cmake --build build-win --config Release --target dlrl || exit /b 1
popd
echo Built: %WORK%\build-win\Release\dlrl.exe
