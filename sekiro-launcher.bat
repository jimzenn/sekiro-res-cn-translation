@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

title Sekiro: Resurrection 简中翻译更新

REM ================================================================
REM  配置: Sekiro 装在其他路径 / 想锁版本时改这里
REM ================================================================
set "SEKIRO_MODS=C:\Program Files (x86)\Steam\steamapps\common\Sekiro\mods"
set "REPO=jimzenn/sekiro-res-cn-translation"
set "BRANCH=main"
REM  锁特定版本: 把 BRANCH 改成 commit hash 或 tag, 比如:
REM    set "BRANCH=69eb64dd00213e49a9b673544eef21adb571dd34"
REM ================================================================

REM 自动 elevate (写入 Program Files 需要管理员)
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 申请管理员权限...
    powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

where curl >nul 2>&1
if %errorLevel% neq 0 (
    echo [错误] 没找到 curl. 需要 Windows 10 1803 或更新版本.
    pause
    exit /b 1
)

set "BASE=https://raw.githubusercontent.com/%REPO%/%BRANCH%/build"
set "TMP=%TEMP%\sekiro-res-cn-%RANDOM%"
mkdir "%TMP%\msg\zhocn" 2>nul
mkdir "%TMP%\font\zhocn_map" 2>nul
mkdir "%TMP%\font\zhocn_std" 2>nul

echo.
echo ===============================================================
echo   Sekiro: Resurrection 简中翻译更新
echo ===============================================================
echo   来源: %REPO% ^(%BRANCH%^)
echo   目标: %SEKIRO_MODS%
echo ===============================================================
echo.

if not exist "%SEKIRO_MODS%" (
    echo [错误] mods 目录不存在:
    echo   %SEKIRO_MODS%
    echo.
    echo 确认 Sekiro 装好了 Resurrection, 或改本脚本顶部的 SEKIRO_MODS.
    rmdir /s /q "%TMP%" 2>nul
    pause
    exit /b 1
)

set FAIL=0

echo [1/2] 从 GitHub 下载到临时目录...
echo.
call :dl "msg/zhocn/menu.msgbnd.dcx"   "menu  (菜单/对白/教程)"
call :dl "msg/zhocn/item.msgbnd.dcx"   "item  (道具/装备/技能)"
call :dl "font/zhocn_map/font.gfx"     "font  (地图字体)"
call :dl "font/zhocn_std/font.gfx"     "font  (标准字体)"

if !FAIL! neq 0 (
    echo.
    echo [错误] 有文件下载失败. mods 目录未被修改.
    echo        检查网络, 或确认 BRANCH=%BRANCH% 上确实有 build/ 文件.
    rmdir /s /q "%TMP%" 2>nul
    pause
    exit /b 1
)

echo.
echo [2/2] 覆盖到 mods 目录...
xcopy /e /y /i "%TMP%\*" "%SEKIRO_MODS%\" >nul
if %errorLevel% neq 0 (
    echo [错误] 复制失败. 检查权限或目录是否被占用.
    rmdir /s /q "%TMP%" 2>nul
    pause
    exit /b 1
)

rmdir /s /q "%TMP%" 2>nul

echo.
echo ===============================================================
echo   完成. 可以启动游戏了.
echo ===============================================================
pause
exit /b 0

:dl
set "REL=%~1"
set "LABEL=%~2"
echo   - %LABEL%
echo     %REL%
curl -fLsS -o "%TMP%\%REL%" "%BASE%/%REL%"
if errorlevel 1 (
    echo     X 下载失败
    set FAIL=1
)
exit /b 0
