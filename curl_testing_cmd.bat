@echo off
curl -X POST https://linebot2023-1rzn.onrender.com/callback ^
  -H "Content-Type: application/json" ^
  -d "{\"events\":[{\"type\":\"message\",\"message\":{\"type\":\"text\",\"text\":\"hello\"}}]}"
pause