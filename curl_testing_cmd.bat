@echo off


curl -X POST https://linebot2023-1rzn.onrender.com/download ^
  -H "Content-Type: application/json" ^
  -d "{\"url\":\"https://www.youtube.com/watch?v=dQw4w9WgXcQ\",\"format\":\"mp3\"}"
pause