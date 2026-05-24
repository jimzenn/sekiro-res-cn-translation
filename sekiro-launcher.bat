@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

title Sekiro: Resurrection 简中翻译更新

REM ================================================================
REM  配置: 路径不对就改这里
REM ================================================================
set "SEKIRO_MODS=C:\Program Files (x86)\Steam\steamapps\common\Sekiro\mods"
set "GAME_LAUNCHER=%SEKIRO_MODS%\..\launchmod_sekiro.bat"
set "REPO=jimzenn/sekiro-res-cn-translation"
set "BRANCH=main"
REM  锁版本: 把 BRANCH 改成 commit hash 或 tag, 比如:
REM    set "BRANCH=e75afad1e870d7b52aed9dcf1dbb7e18675f8190"
REM ================================================================

REM ---------- 自动 elevate ----------
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo 请求管理员权限 ^(写入 Program Files 需要^)...
    echo.
    powershell -NoProfile -Command "try { Start-Process -FilePath '%~f0' -Verb RunAs -ErrorAction Stop } catch { exit 1 }"
    if errorlevel 1 (
        echo ===============================================================
        echo   没拿到管理员权限. 你点 "否" 了, 或 PowerShell 出错了.
        echo ===============================================================
        echo.
        echo 解决方法: 关掉这个窗口, 然后右键这个 .bat
        echo           -^> "以管理员身份运行".
        echo.
        echo 按任意键关闭.
        pause >nul
    )
    exit /b
)

REM ---------- 主流程 (admin 窗口跑这里) ----------
call :run
set "RUN_EXIT=!errorLevel!"

echo.
echo ===============================================================
if "!RUN_EXIT!"=="0" (
    echo   一切顺利.
) else (
    echo   出错了 ^(exit code !RUN_EXIT!^). 滚回去看上面的错误信息.
)
echo ===============================================================
echo.
echo 按任意键关闭...
pause >nul
exit /b !RUN_EXIT!


REM ================================================================
REM  :run - 全部失败都用 exit /b 1 返回, 顶层会统一 pause
REM ================================================================
:run
where curl >nul 2>&1
if %errorLevel% neq 0 (
    echo [错误] 没找到 curl. 需要 Windows 10 1803 或更新版本.
    exit /b 1
)

if not exist "%SEKIRO_MODS%" (
    echo [错误] Sekiro mods 目录不存在:
    echo   %SEKIRO_MODS%
    echo.
    echo 改本脚本顶部的 SEKIRO_MODS 变量, 指向你实际的 mods 目录.
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
echo   临时: %TMP%
echo ===============================================================
echo.

set FAIL=0

echo [1/3] 从 GitHub 下载到临时目录...
echo.
call :dl "msg/zhocn/menu.msgbnd.dcx"   "menu (菜单/对白/教程)"
call :dl "msg/zhocn/item.msgbnd.dcx"   "item (道具/装备/技能)"
call :dl "font/zhocn_map/font.gfx"     "font (地图字体)"
call :dl "font/zhocn_std/font.gfx"     "font (标准字体)"

if !FAIL! neq 0 (
    echo.
    echo [错误] 有文件下载失败. mods 目录未被修改.
    echo        检查网络, 或确认 %BRANCH% 分支上确实有 build/ 文件.
    rmdir /s /q "%TMP%" 2>nul
    exit /b 1
)

echo.
echo [2/3] 覆盖到 mods 目录...
xcopy /e /y /i "%TMP%\*" "%SEKIRO_MODS%\" >nul
if %errorLevel% neq 0 (
    echo [错误] 复制失败. 检查权限或文件是否被游戏占用 ^(关掉游戏再试^).
    rmdir /s /q "%TMP%" 2>nul
    exit /b 1
)
rmdir /s /q "%TMP%" 2>nul
echo   完成.

echo.
echo [3/3] 启动游戏...
if exist "%GAME_LAUNCHER%" (
    echo   launchmod_sekiro.bat
    start "" "%GAME_LAUNCHER%"
    echo   已启动 ^(modengine2 窗口会自己弹^).
) else (
    echo   ^(跳过^) 没找到 launchmod_sekiro.bat:
    echo     %GAME_LAUNCHER%
    echo   手动启动游戏即可, 或改脚本顶部的 GAME_LAUNCHER 变量.
)

echo.
echo ===============================================================
echo   汉化更新完成!
echo ===============================================================
exit /b 0


REM ================================================================
REM  :dl <relative-path> <label>
REM ================================================================
:dl
set "REL=%~1"
set "LABEL=%~2"
echo   - %LABEL%
echo     %REL%
curl -fLsS -o "%TMP%\%REL%" "%BASE%/%REL%"
if errorlevel 1 (
    echo     X 下载失败 ^(URL: %BASE%/%REL%^)
    set FAIL=1
)
exit /b 0
