@echo off
echo Portfolio Image Resizer
echo ======================
echo.
echo Installing dependencies...
pip install -r requirements_resize.txt
echo.
echo Running image resizer...
python resize_portfolio_images.py --portfolio-dir "static/img/portfolio"
echo.
echo Done! Check the resized images in your portfolio directory.
pause
