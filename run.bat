@echo off
color 0A
title App User Behavior Segmentation Dashboard

echo ============================================================
echo    📊 App User Behavior Segmentation Dashboard
echo ============================================================
echo.
echo 📁 Project: D:\GITHUB_PROJECTS\app_user_segmentation
echo.
echo 🔍 Checking for model files...
echo.

cd /d D:\GITHUB_PROJECTS\app_user_segmentation

if exist "models\kmeans_user_segmentation.pkl" (
    echo ✅ K-Means Model found
) else (
    echo ⚠️ K-Means Model not found - predictions will not work
)

if exist "models\user_segmentation_scaler.pkl" (
    echo ✅ Scaler file found
) else (
    echo ⚠️ Scaler file not found - predictions will not work
)

echo.
echo 📦 Installing dependencies...
py -m pip install -q Flask pandas numpy scikit-learn matplotlib seaborn joblib

echo.
echo 🚀 Starting Flask application...
echo.
echo ============================================================
echo    🌐 Application will be available at: http://localhost:5000
echo    📊 Dashboard: http://localhost:5000/
echo    👥 Segments: http://localhost:5000/segments
echo    📈 Analytics: http://localhost:5000/analytics
echo    📋 Reports: http://localhost:5000/reports
echo    🔮 Predict: http://localhost:5000/predict
echo ============================================================
echo.
echo    Press Ctrl+C to stop the server
echo ============================================================
echo.

py app.py

echo.
echo ❌ Application stopped or crashed!
echo Press any key to exit...
pause