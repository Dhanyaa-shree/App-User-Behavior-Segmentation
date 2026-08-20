# 🚀 App User Behavior Segmentation

> **Machine Learning • Customer Segmentation • User Analytics • Flask**

A machine learning–powered web application that analyzes user behavior and segments customers into meaningful behavioral groups using **K-Means clustering**. The project combines exploratory data analysis, feature engineering, clustering, PCA visualization, business profiling, and a Flask-based interactive dashboard with real-time segment prediction.

---

## 📌 Overview

Understanding user behavior is essential for improving engagement, reducing churn, and creating personalized customer experiences.

This project analyzes behavioral attributes such as:

* Session frequency
* Average session duration
* Daily active minutes
* Feature interactions
* Notifications
* In-app searches
* Content downloads
* Social sharing
* Engagement score

The behavioral data is transformed into meaningful features and used to identify **four customer segments** through K-Means clustering.

The resulting segments are integrated into an interactive Flask application for visualization, analysis, reporting, and prediction.

---

## 🎯 Objectives

* 📊 Analyze user engagement and behavioral patterns
* 👥 Identify distinct customer segments
* 🤖 Apply unsupervised machine learning for segmentation
* 🔍 Understand behavioral characteristics of each segment
* ⚠️ Identify low-engagement and potentially at-risk users
* 🎯 Support targeted customer strategies
* 🔮 Predict the segment of new users

---

## ✨ Key Features

### 📊 Interactive Dashboard

* Total user statistics
* Segment count
* Average engagement metrics
* Segment distribution
* User segment overview
* Quick navigation to analytics and reports

### 👥 Customer Segmentation

Four behavioral segments are identified:

| Segment                           | Description                                      |      Users |    Share |
| --------------------------------- | ------------------------------------------------ | ---------: | -------: |
| 🌟 **High Engagement**            | Highly active and valuable users                 |     17,110 |   34.22% |
| 📊 **Moderate Engagement**        | Regular users with consistent activity           |     11,200 |   22.40% |
| 📱 **Occasional / Content-Light** | Users with limited or sporadic interaction       |      9,619 |   19.24% |
| ⚠️ **Low Engagement / At-Risk**   | Users with low activity and potential churn risk |     12,071 |   24.14% |
| **Total**                         |                                                  | **50,000** | **100%** |

The segment labels are assigned from the behavioral profiles of the resulting clusters.

### 📈 Analytics

The application provides:

* Segment distribution visualization
* PCA cluster visualization
* Engagement analysis
* Behavioral correlation heatmap
* Segment behavior profiles
* Comparative behavioral insights

### 📋 Business Reports

The reporting module provides:

* Executive summary
* Segment-level insights
* Business recommendations
* Retention opportunities
* Segment-specific action strategies

### 🔮 Real-Time Prediction

Users can enter behavioral metrics and receive a predicted customer segment.

Prediction inputs include:

* Sessions per week
* Average session duration
* Daily active minutes
* Engagement score
* Feature clicks per session
* Notifications opened
* In-app search count
* Content downloads
* Social shares

---

# 🤖 Machine Learning

## Algorithm

The project uses **K-Means clustering** for unsupervised customer segmentation.

### Model Configuration

| Parameter                | Value          |
| ------------------------ | -------------- |
| Algorithm                | K-Means        |
| Number of Users          | 50,000         |
| Number of Clusters       | **4**          |
| Feature Scaling          | StandardScaler |
| Dimensionality Reduction | PCA            |
| Final Silhouette Score   | **0.2518**     |

The clustering pipeline applies log transformation followed by standard scaling before model training.

---

## 🧩 Feature Engineering

Three behavioral features are created for clustering:

```text
weekly_engagement_minutes
interaction_score
content_activity
```

### Feature Definitions

**Weekly Engagement Minutes**

```text
sessions_per_week × avg_session_duration_min
```

**Interaction Score**

```text
feature_clicks_per_session
+ notifications_opened_per_week
+ in_app_search_count
```

**Content Activity**

```text
content_downloads + social_shares
```

These engineered features are then transformed and standardized before clustering.

---

# 📊 Model Performance

The clustering models were evaluated using the **Silhouette Score**.

| Model                    | Clusters | Silhouette Score |
| ------------------------ | -------: | ---------------: |
| 🏆 **K-Means**           |    **4** |       **0.2518** |
| Agglomerative Clustering |        4 |           0.1794 |

K-Means produced the stronger clustering score and was selected as the final segmentation model. The final K-Means model achieved a silhouette score of **0.2518**.

> **Note:** The model comparison was performed on a sample because hierarchical clustering is computationally expensive for the full 50,000-user dataset.

---

# 🔄 Machine Learning Workflow

```text
                    ┌─────────────────────┐
                    │   Raw User Data     │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │   Data Cleaning     │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │ Feature Engineering │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │   Log Transform     │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │  Standard Scaling   │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │   K-Means Model     │
                    │      K = 4          │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │  User Segments      │
                    └──────────┬──────────┘
                               ↓
             ┌─────────────────┴─────────────────┐
             ↓                                   ↓
    ┌──────────────────┐                ┌──────────────────┐
    │ PCA Visualization│                │ Flask Web App    │
    └──────────────────┘                └────────┬─────────┘
                                                 ↓
                                      ┌─────────────────────┐
                                      │ Real-Time Prediction│
                                      └─────────────────────┘
```

---

# 💼 Business Insights

The segmentation supports different strategies for different user groups.

| Segment                           | Recommended Strategy                                    |
| --------------------------------- | ------------------------------------------------------- |
| 🌟 **High Engagement**            | Loyalty rewards, premium offers and referral programs   |
| 📊 **Moderate Engagement**        | Personalized recommendations and feature discovery      |
| 📱 **Occasional / Content-Light** | Personalized content and discovery campaigns            |
| ⚠️ **Low Engagement / At-Risk**   | Retention campaigns, reminders and re-engagement offers |

These business actions are defined from the project's segment-level behavioral analysis.

---

# 🔍 Exploratory Data Analysis

The project includes analysis of:

### Sessions per Week

Most users are concentrated in the moderate weekly session range, with fewer users at very low and very high frequencies.

### Session Duration

Session duration is right-skewed, with most sessions concentrated around shorter durations and a smaller number of longer sessions.

### Daily Active Minutes

Daily activity is concentrated around moderate levels, with fewer highly active users.

### Sessions vs Engagement

Session frequency alone does not strongly explain engagement, indicating that engagement is influenced by multiple behavioral factors.

### Behavioral Correlation

The behavioral variables demonstrate mostly weak linear correlations, supporting a multivariate approach to user segmentation.

---

# 📉 PCA Visualization

PCA is used to project the three-dimensional behavioral feature space into two principal components for visualization.

The PCA visualization provides an intuitive view of the four K-Means clusters and shows that the segments represent **broad behavioral groups with some overlap**.

> PCA is used for visualization and does not replace the original feature space used for clustering.

---

# 🛠️ Technology Stack

### Backend

* **Python**
* **Flask**
* **pandas**
* **NumPy**

### Machine Learning

* **scikit-learn**
* **K-Means**
* **Agglomerative Clustering**
* **StandardScaler**
* **PCA**
* **joblib**

### Visualization

* **Matplotlib**
* **Seaborn**

### Frontend

* **HTML5**
* **CSS3**
* **JavaScript**

### Development

* **Jupyter Notebook**
* **Git**
* **GitHub**

---

# 📁 Project Structure

```text
App-User-Behavior-Segmentation/
│
├── Customer_Segments_Data/          # Final customer segment results
│
├── Raw_User_Data/                   # Original raw user data
│
├── Segmentation_Analysis_Data/      # Processed data and analysis outputs
│
├── Trained_Notebook/                # Jupyter notebooks
│
├── models/                          # Trained ML models
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       ├── script.js
│       └── segments.js
│
├── templates/
│   ├── analytics.html
│   ├── base.html
│   ├── dashboard.html
│   ├── predict.html
│   ├── reports.html
│   ├── segment_detail.html
│   └── segments.html
│
├── app.py                           # Flask application
├── fix_model_v2.py                  # Model training utility
├── test_model.py                    # Model testing
├── requirements.txt                 # Python dependencies
├── run.bat                          # Windows launcher
├── .gitignore
└── README.md
```

---

# 🚀 Installation & Setup

## Prerequisites

* Python **3.8+**
* pip
* Git

## 1. Clone the Repository

```bash
git clone https://github.com/Dhanyaa-shree/App-User-Behavior-Segmentation.git
cd App-User-Behavior-Segmentation
```

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Run the Application

### Windows

```bash
run.bat
```

### Or manually

```bash
python app.py
```

Open the application at:

```text
http://localhost:5000
```

---

# 🧪 Model Training & Testing

## Train / Update Model

```bash
python fix_model_v2.py
```

The training pipeline:

1. Loads the behavioral dataset
2. Creates engineered features
3. Applies log transformation
4. Standardizes the features
5. Trains the K-Means model
6. Assigns cluster labels
7. Generates business segment names
8. Saves the segmentation outputs

The project generates:

```text
app_user_segmentation_results.csv
customer_segments.csv
```

## Test Model

```bash
python test_model.py
```

---

# 🌐 Application Modules

| Module        | Purpose                                |
| ------------- | -------------------------------------- |
| **Dashboard** | Overall user and segment statistics    |
| **Segments**  | Explore individual customer segments   |
| **Analytics** | Behavioral analysis and visualizations |
| **Reports**   | Business insights and recommendations  |
| **Predict**   | Real-time segment prediction           |

---

# 📡 API Endpoints

| Endpoint            | Method | Description                |
| ------------------- | ------ | -------------------------- |
| `/api/predict`      | POST   | Predict user segment       |
| `/api/clusters`     | GET    | Retrieve cluster summaries |
| `/api/cluster/<id>` | GET    | Retrieve cluster details   |
| `/api/stats`        | GET    | Retrieve statistics        |
| `/api/search`       | GET    | Search users               |
| `/api/export/<id>`  | GET    | Export segment data        |
| `/api/export/all`   | GET    | Export all data            |
| `/api/refresh`      | GET    | Refresh application data   |

---

# 📌 Key Results

```text
Users Analyzed          : 50,000
Algorithm               : K-Means
Optimal K               : 4
Final Silhouette Score  : 0.2518
Number of Segments      : 4
```

### Final Segment Distribution

```text
High Engagement             17,110
Moderate Engagement         11,200
Occasional / Content-Light   9,619
Low Engagement / At-Risk    12,071
──────────────────────────────────
Total                       50,000
```

The final project summary confirms the 50,000-user dataset, K-Means algorithm, four segments, and the final silhouette score.

---

# 🔮 Future Enhancements

* 📉 Churn prediction
* 💰 Customer Lifetime Value analysis
* 🤖 Automated model retraining
* 🎯 Personalized recommendations
* ☁️ Cloud deployment
* 📊 Advanced clustering comparison
* 🔐 User authentication and role-based access
* 📈 Automated business reporting

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the application
5. Submit a Pull Request

Example:

```bash
git checkout -b feature/new-feature
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
```

---

# 📄 License

This project is intended for **educational, analytical, and portfolio purposes**.

---

# 👨‍💻 Author

### Dhanyaa Shree T

Built as an end-to-end machine learning project combining:

**Data Analysis → Feature Engineering → Clustering → Business Segmentation → Web Application**

---

<div align="center">

## ⭐ App User Behavior Segmentation

**Turning user behavior into actionable customer insights.**

Made with ❤️ using **Python, Machine Learning & Flask**

</div>
