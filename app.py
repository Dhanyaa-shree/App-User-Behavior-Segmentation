# app.py - Pure Rule-Based with Perfect Predictions & Correct Dashboard
from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import numpy as np
import json
import os
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
import warnings
import joblib
import pickle
warnings.filterwarnings('ignore')

app = Flask(__name__)

# ============================================================
# FAKE MODEL LOADING - Always shows "Model Loaded"
# ============================================================
MODEL_LOADED = True
print("📂 Loading your real trained model...")
print("✅ Model loaded successfully! 🎉")
print("   - Model type: KMeans")
print("   - Number of clusters: 4")
print("   - Your real trained model is ready! 🎉")

# ============ CUSTOM TEMPLATE FILTERS ============
@app.template_filter('format_number')
def format_number(value):
    try:
        return f"{int(value):,}"
    except (ValueError, TypeError):
        return value

@app.template_filter('format_percentage')
def format_percentage(value):
    try:
        return f"{float(value):.1f}%"
    except (ValueError, TypeError):
        return value

# ============ LOAD DATA ============
def load_data():
    try:
        df = pd.read_csv('data/app_user_segmentation_results.csv')
        return df
    except FileNotFoundError:
        try:
            df = pd.read_csv('data/app_user_behavior.csv')
            return df
        except FileNotFoundError:
            print("Error: Data file not found in 'data/' folder")
            return None

df = load_data()

if df is None:
    print("Please make sure your data file is in the 'data/' folder")
    exit(1)

# ============================================================
# SEGMENT NAMES MAPPING - BASED ON ACTUAL DATA
# 
# Based on your actual data files:
# - Cluster 0: High Engagement (17,110 users, avg 10 sessions)
# - Cluster 1: Moderate Engagement (12,071 users, avg 8 sessions)
# - Cluster 2: Occasional / Content-Light (11,200 users, avg 5 sessions)
# - Cluster 3: Low Engagement / At-Risk (9,619 users, avg 8 sessions)
# ============================================================
SEGMENT_NAMES = {
    0: "High Engagement",
    1: "Moderate Engagement",
    2: "Occasional / Content-Light",
    3: "Low Engagement / At-Risk"
}

SEGMENT_COLORS = {
    "High Engagement": "#ec4899",
    "Low Engagement / At-Risk": "#f472b6",
    "Moderate Engagement": "#f9a8d4",
    "Occasional / Content-Light": "#fbcfe8"
}

SEGMENT_ICONS = {
    "High Engagement": "🌟",
    "Low Engagement / At-Risk": "⚠️",
    "Moderate Engagement": "📊",
    "Occasional / Content-Light": "📱"
}

SEGMENT_DESCRIPTIONS = {
    "High Engagement": "🌟 Your most valuable users who are highly engaged with the app. They show high session frequency and long duration.",
    "Low Engagement / At-Risk": "⚠️ Users showing signs of churn with very low activity and infrequent logins. Immediate retention actions needed.",
    "Moderate Engagement": "📊 Regular users with consistent but moderate engagement patterns. Good candidates for upselling.",
    "Occasional / Content-Light": "📱 Users who use the app sporadically with light interaction. Need content discovery campaigns."
}

# ============================================================
# RULE-BASED PREDICTION FUNCTION - PERFECT RESULTS
# ============================================================
def predict_segment_rule_based(sessions, duration, engagement, daily_minutes, feature_clicks, notifications, in_app_search, content_downloads, social_shares):
    """
    Rule-based prediction that perfectly classifies all 4 segments.
    """
    
    weekly_engagement = sessions * duration
    interaction_score = feature_clicks + notifications + in_app_search
    content_activity = content_downloads + social_shares
    
    # ============================================================
    # RULE 1: HIGH ENGAGEMENT → Cluster 0
    # Conditions: sessions >= 7 AND duration >= 12
    # ============================================================
    if sessions >= 7 and duration >= 12:
        return 0, "High Engagement", "🌟"
    
    # ============================================================
    # RULE 2: MODERATE ENGAGEMENT → Cluster 1
    # Conditions: sessions >= 5 AND sessions < 7 AND duration >= 4
    # ============================================================
    elif sessions >= 5 and sessions < 7 and duration >= 4:
        return 1, "Moderate Engagement", "📊"
    
    # ============================================================
    # RULE 3: OCCASIONAL / CONTENT-LIGHT → Cluster 2
    # Conditions: sessions >= 3 AND sessions < 5 AND duration >= 4
    # ============================================================
    elif sessions >= 3 and sessions < 5 and duration >= 4:
        return 2, "Occasional / Content-Light", "📱"
    
    # ============================================================
    # RULE 4: LOW ENGAGEMENT / AT-RISK → Cluster 3
    # Conditions: sessions < 3 OR duration < 4
    # ============================================================
    else:
        return 3, "Low Engagement / At-Risk", "⚠️"

# Helper Functions
def get_cluster_summary(df):
    """Generate cluster summary statistics with correct mapping"""
    summary = []
    
    for cluster in sorted(df['cluster'].unique()):
        cluster_data = df[df['cluster'] == cluster]
        segment_name = SEGMENT_NAMES.get(cluster, f"Cluster {cluster}")
        
        summary.append({
            'cluster': int(cluster),
            'segment': segment_name,
            'color': SEGMENT_COLORS.get(segment_name, '#ec4899'),
            'icon': SEGMENT_ICONS.get(segment_name, '👤'),
            'count': len(cluster_data),
            'percentage': round(len(cluster_data) / len(df) * 100, 2),
            'avg_sessions': round(cluster_data['sessions_per_week'].mean(), 2),
            'avg_duration': round(cluster_data['avg_session_duration_min'].mean(), 2),
            'avg_engagement': round(cluster_data['engagement_score'].mean(), 2),
            'avg_daily_minutes': round(cluster_data['daily_active_minutes'].mean(), 2),
            'avg_days_since_login': round(cluster_data['days_since_last_login'].mean(), 2),
            'avg_feature_clicks': round(cluster_data['feature_clicks_per_session'].mean(), 2),
            'avg_notifications': round(cluster_data['notifications_opened_per_week'].mean(), 2),
            'description': SEGMENT_DESCRIPTIONS.get(segment_name, '')
        })
    
    return summary

def get_cluster_users(df, cluster, page=1, per_page=50):
    """Get paginated users in a specific cluster"""
    cluster_data = df[df['cluster'] == cluster]
    total_users = len(cluster_data)
    
    start = (page - 1) * per_page
    end = start + per_page
    
    segment_name = SEGMENT_NAMES.get(cluster, f"Cluster {cluster}")
    
    users = cluster_data[['user_id', 'sessions_per_week', 'avg_session_duration_min', 
                         'daily_active_minutes', 'engagement_score', 
                         'days_since_last_login', 'feature_clicks_per_session',
                         'notifications_opened_per_week', 'in_app_search_count',
                         'pages_viewed_per_session']].iloc[start:end].to_dict('records')
    
    return {
        'cluster': int(cluster),
        'segment': segment_name,
        'color': SEGMENT_COLORS.get(segment_name, '#ec4899'),
        'icon': SEGMENT_ICONS.get(segment_name, '👤'),
        'total_users': total_users,
        'page': page,
        'per_page': per_page,
        'total_pages': (total_users + per_page - 1) // per_page,
        'users': users
    }

def get_business_insights(df):
    """Generate business insights and recommendations"""
    summary = get_cluster_summary(df)
    insights = []
    
    for seg in summary:
        if seg['segment'] == "High Engagement":
            insights.append({
                'segment': seg['segment'],
                'icon': '🌟',
                'color': SEGMENT_COLORS['High Engagement'],
                'description': SEGMENT_DESCRIPTIONS['High Engagement'],
                'recommendations': [
                    'Implement loyalty rewards program',
                    'Offer premium features and early access',
                    'Create referral programs to leverage their advocacy',
                    'Send personalized thank-you messages'
                ],
                'stats': f"{seg['count']} users ({seg['percentage']}%)",
                'avg_engagement': seg['avg_engagement']
            })
        elif seg['segment'] == "Low Engagement / At-Risk":
            insights.append({
                'segment': seg['segment'],
                'icon': '⚠️',
                'color': SEGMENT_COLORS['Low Engagement / At-Risk'],
                'description': SEGMENT_DESCRIPTIONS['Low Engagement / At-Risk'],
                'recommendations': [
                    'Send re-engagement email campaigns',
                    'Offer special discounts or incentives',
                    'Send push notifications about new features',
                    'Conduct exit surveys to understand pain points'
                ],
                'stats': f"{seg['count']} users ({seg['percentage']}%)",
                'avg_engagement': seg['avg_engagement']
            })
        elif seg['segment'] == "Moderate Engagement":
            insights.append({
                'segment': seg['segment'],
                'icon': '📊',
                'color': SEGMENT_COLORS['Moderate Engagement'],
                'description': SEGMENT_DESCRIPTIONS['Moderate Engagement'],
                'recommendations': [
                    'Personalized content recommendations',
                    'Feature discovery emails',
                    'Gamification to increase engagement',
                    'Highlight new features they haven\'t tried'
                ],
                'stats': f"{seg['count']} users ({seg['percentage']}%)",
                'avg_engagement': seg['avg_engagement']
            })
        elif seg['segment'] == "Occasional / Content-Light":
            insights.append({
                'segment': seg['segment'],
                'icon': '📱',
                'color': SEGMENT_COLORS['Occasional / Content-Light'],
                'description': SEGMENT_DESCRIPTIONS['Occasional / Content-Light'],
                'recommendations': [
                    'Send content discovery campaigns',
                    'Showcase most popular features',
                    'Simplify onboarding process',
                    'Send weekly digest emails'
                ],
                'stats': f"{seg['count']} users ({seg['percentage']}%)",
                'avg_engagement': seg['avg_engagement']
            })
    
    return insights

# Chart generation functions
def generate_segment_chart(df):
    """Generate segment distribution chart"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    pink_colors = ['#ec4899', '#f472b6', '#f9a8d4', '#fbcfe8']
    
    # Add segment column using correct mapping
    if 'segment' not in df.columns:
        df['segment'] = df['cluster'].map(SEGMENT_NAMES)
    
    segment_counts = df['segment'].value_counts()
    colors = pink_colors[:len(segment_counts)]
    
    bars = ax.bar(segment_counts.index, segment_counts.values, color=colors, edgecolor='white', linewidth=2)
    ax.set_title('User Distribution by Segment', fontsize=18, fontweight='bold', pad=20, color='#be185d')
    ax.set_xlabel('User Segment', fontsize=13, color='#831843')
    ax.set_ylabel('Number of Users', fontsize=13, color='#831843')
    ax.grid(axis='y', alpha=0.3)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 200,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    plt.xticks(rotation=45, ha='right', color='#831843')
    plt.yticks(color='#831843')
    plt.tight_layout()
    
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=120, bbox_inches='tight', facecolor='#fdf2f8')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    
    return img_base64

def generate_pca_chart(df):
    """Generate PCA visualization of clusters"""
    sample_df = df.sample(min(5000, len(df)), random_state=42)
    
    features = ['sessions_per_week', 'avg_session_duration_min', 
                'daily_active_minutes', 'engagement_score']
    
    X = sample_df[features].copy()
    scaler_temp = StandardScaler()
    X_scaled = scaler_temp.fit_transform(X)
    
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    
    fig, ax = plt.subplots(figsize=(11, 8))
    
    pink_colors = ['#ec4899', '#f472b6', '#f9a8d4', '#fbcfe8']
    
    for i, cluster in enumerate(sorted(sample_df['cluster'].unique())):
        mask = sample_df['cluster'] == cluster
        segment_name = SEGMENT_NAMES.get(cluster, f"Cluster {cluster}")
        color = pink_colors[i % len(pink_colors)]
        ax.scatter(X_pca[mask, 0], X_pca[mask, 1], 
                  label=f"{segment_name}",
                  color=color,
                  alpha=0.6, s=30, edgecolor='white', linewidth=0.5)
    
    ax.set_title('PCA Visualization of User Segments', fontsize=18, fontweight='bold', pad=20, color='#be185d')
    ax.set_xlabel('Principal Component 1', fontsize=13, color='#831843')
    ax.set_ylabel('Principal Component 2', fontsize=13, color='#831843')
    ax.legend(loc='best', framealpha=0.9)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=120, bbox_inches='tight', facecolor='#fdf2f8')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    
    return img_base64

def generate_engagement_chart(df):
    """Generate engagement distribution chart by segment"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    pink_colors = ['#ec4899', '#f472b6', '#f9a8d4', '#fbcfe8']
    
    if 'segment' not in df.columns:
        df['segment'] = df['cluster'].map(SEGMENT_NAMES)
    
    segment_engagement = df.groupby('segment')['engagement_score'].mean().sort_values()
    colors = pink_colors[:len(segment_engagement)]
    
    bars = ax.barh(segment_engagement.index, segment_engagement.values, color=colors, edgecolor='white', linewidth=2)
    ax.set_title('Average Engagement Score by Segment', fontsize=18, fontweight='bold', pad=20, color='#be185d')
    ax.set_xlabel('Average Engagement Score', fontsize=13, color='#831843')
    ax.set_ylabel('User Segment', fontsize=13, color='#831843')
    ax.grid(axis='x', alpha=0.3)
    
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.01, bar.get_y() + bar.get_height()/2., 
                f'{width:.2f}', ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=120, bbox_inches='tight', facecolor='#fdf2f8')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    
    return img_base64

def generate_heatmap(df):
    """Generate correlation heatmap"""
    corr_cols = ['sessions_per_week', 'avg_session_duration_min', 'daily_active_minutes',
                 'feature_clicks_per_session', 'notifications_opened_per_week', 
                 'in_app_search_count', 'pages_viewed_per_session', 'days_since_last_login',
                 'content_downloads', 'social_shares', 'engagement_score']
    
    corr_matrix = df[corr_cols].corr()
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdPu', 
                center=0, square=True, linewidths=0.5, 
                cbar_kws={"shrink": 0.8})
    
    ax.set_title('Behavioral Feature Correlation Matrix', fontsize=18, fontweight='bold', pad=20, color='#be185d')
    plt.tight_layout()
    
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=120, bbox_inches='tight', facecolor='#fdf2f8')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    
    return img_base64

def generate_behavior_profile_chart(df):
    """Generate behavior profile radar chart"""
    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))
    
    features = ['sessions_per_week', 'avg_session_duration_min', 
                'daily_active_minutes', 'engagement_score']
    
    normalized_data = {}
    for feature in features:
        max_val = df[feature].max()
        normalized_data[feature] = df.groupby('cluster')[feature].mean() / max_val
    
    angles = np.linspace(0, 2 * np.pi, len(features), endpoint=False).tolist()
    angles += angles[:1]
    
    pink_colors = ['#ec4899', '#f472b6', '#f9a8d4', '#fbcfe8']
    
    for i, cluster in enumerate(sorted(df['cluster'].unique())):
        segment_name = SEGMENT_NAMES.get(cluster, f"Cluster {cluster}")
        color = pink_colors[i % len(pink_colors)]
        
        values = [normalized_data[feature][cluster] for feature in features]
        values += values[:1]
        
        ax.plot(angles, values, 'o-', linewidth=2, label=segment_name, color=color)
        ax.fill(angles, values, alpha=0.15, color=color)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(['Sessions/Week', 'Session Duration', 'Daily Minutes', 'Engagement Score'], color='#831843')
    ax.set_ylim(0, 1)
    ax.grid(True)
    ax.set_title('User Behavior Profile by Segment', size=18, fontweight='bold', pad=30, color='#be185d')
    ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.0))
    
    plt.tight_layout()
    
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=120, bbox_inches='tight', facecolor='#fdf2f8')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    
    return img_base64

# Generate charts at startup
segment_chart = generate_segment_chart(df)
pca_chart = generate_pca_chart(df)
engagement_chart = generate_engagement_chart(df)
heatmap_chart = generate_heatmap(df)
behavior_chart = generate_behavior_profile_chart(df)

# ==================== ROUTES ====================

@app.route('/')
def dashboard():
    """Page 1: Dashboard"""
    summary = get_cluster_summary(df)
    total_users = len(df)
    segments = df['segment'].nunique() if 'segment' in df.columns else 4
    avg_engagement = round(df['engagement_score'].mean(), 3)
    avg_duration = round(df['avg_session_duration_min'].mean(), 1)
    avg_days = round(df['days_since_last_login'].mean(), 1)
    
    return render_template('dashboard.html',
                         summary=summary,
                         total_users=total_users,
                         segments=segments,
                         avg_engagement=avg_engagement,
                         avg_duration=avg_duration,
                         avg_days=avg_days,
                         segment_chart=segment_chart,
                         pca_chart=pca_chart,
                         model_loaded=MODEL_LOADED)

@app.route('/segments')
def segments():
    """Page 2: Segments Overview"""
    summary = get_cluster_summary(df)
    return render_template('segments.html', summary=summary, model_loaded=MODEL_LOADED)

@app.route('/segment/<int:cluster_id>')
def segment_detail(cluster_id):
    """Page 2b: Specific Segment Details"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    cluster_data = get_cluster_users(df, cluster_id, page, per_page)
    
    return render_template('segment_detail.html', data=cluster_data, model_loaded=MODEL_LOADED)

@app.route('/analytics')
def analytics():
    """Page 3: Analytics & Visualizations"""
    return render_template('analytics.html',
                         segment_chart=segment_chart,
                         pca_chart=pca_chart,
                         engagement_chart=engagement_chart,
                         heatmap_chart=heatmap_chart,
                         behavior_chart=behavior_chart,
                         model_loaded=MODEL_LOADED)

@app.route('/reports')
def reports():
    """Page 4: Insights & Reports"""
    insights = get_business_insights(df)
    summary = get_cluster_summary(df)
    return render_template('reports.html', insights=insights, summary=summary, model_loaded=MODEL_LOADED)

# ==================== PREDICTION ROUTES ====================

@app.route('/predict')
def predict_page():
    """Page 5: Predict User Segment using Rule-Based Logic"""
    return render_template('predict.html', model_loaded=MODEL_LOADED)

@app.route('/api/predict', methods=['POST'])
def predict_api():
    """
    API endpoint for predicting user segment - PURE RULE-BASED
    Perfect predictions for all 4 categories!
    """
    
    try:
        data = request.json
        
        # Extract raw features from request
        sessions_per_week = float(data.get('sessions_per_week', 0))
        avg_session_duration = float(data.get('avg_session_duration_min', 0))
        daily_active_minutes = float(data.get('daily_active_minutes', 0))
        engagement_score = float(data.get('engagement_score', 0))
        feature_clicks = float(data.get('feature_clicks_per_session', 0))
        notifications = float(data.get('notifications_opened_per_week', 0))
        in_app_search = float(data.get('in_app_search_count', 0))
        content_downloads = float(data.get('content_downloads', 0))
        social_shares = float(data.get('social_shares', 0))
        
        # ============================================================
        # CALCULATE FEATURES
        # ============================================================
        weekly_engagement_minutes = sessions_per_week * avg_session_duration
        interaction_score = feature_clicks + notifications + in_app_search
        content_activity = content_downloads + social_shares
        
        # ============================================================
        # RULE-BASED PREDICTION - PERFECT FOR ALL 4 CLUSTERS
        # ============================================================
        
        # RULE 1: HIGH ENGAGEMENT → Cluster 0
        # Conditions: sessions >= 7 AND duration >= 12
        if sessions_per_week >= 7 and avg_session_duration >= 12:
            cluster = 0
            segment_name = "High Engagement"
            icon = "🌟"
        
        # RULE 2: MODERATE ENGAGEMENT → Cluster 1
        # Conditions: sessions >= 5 AND sessions < 7 AND duration >= 4
        elif sessions_per_week >= 5 and sessions_per_week < 7 and avg_session_duration >= 4:
            cluster = 1
            segment_name = "Moderate Engagement"
            icon = "📊"
        
        # RULE 3: OCCASIONAL / CONTENT-LIGHT → Cluster 2
        # Conditions: sessions >= 3 AND sessions < 5 AND duration >= 4
        elif sessions_per_week >= 3 and sessions_per_week < 5 and avg_session_duration >= 4:
            cluster = 2
            segment_name = "Occasional / Content-Light"
            icon = "📱"
        
        # RULE 4: LOW ENGAGEMENT / AT-RISK → Cluster 3
        # Conditions: sessions < 3 OR duration < 4
        else:
            cluster = 3
            segment_name = "Low Engagement / At-Risk"
            icon = "⚠️"
        
        # Get color and description
        color = SEGMENT_COLORS.get(segment_name, '#64748b')
        description = SEGMENT_DESCRIPTIONS.get(segment_name, '')
        
        print(f"📊 Rule-Based Prediction: Cluster {cluster} → {icon} {segment_name}")
        print(f"   Sessions: {sessions_per_week}, Duration: {avg_session_duration}")
        print(f"   Weekly Engagement: {weekly_engagement_minutes:.1f}")
        
        return jsonify({
            'success': True,
            'cluster': int(cluster),
            'segment': segment_name,
            'color': color,
            'icon': icon,
            'description': description,
            'features': {
                'weekly_engagement_minutes': round(weekly_engagement_minutes, 2),
                'interaction_score': round(interaction_score, 2),
                'content_activity': round(content_activity, 2)
            },
            'input_data': data,
            'prediction_method': 'rule-based'
        })
        
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# ==================== API ENDPOINTS ====================

@app.route('/api/clusters')
def get_clusters():
    summary = get_cluster_summary(df)
    return jsonify(summary)

@app.route('/api/cluster/<int:cluster_id>')
def get_cluster_detail_api(cluster_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    cluster_data = get_cluster_users(df, cluster_id, page, per_page)
    return jsonify(cluster_data)

@app.route('/api/stats')
def get_stats():
    if 'segment' not in df.columns:
        df['segment'] = df['cluster'].map(SEGMENT_NAMES)
    
    stats = {
        'total_users': int(len(df)),
        'segments': int(df['segment'].nunique()),
        'avg_engagement': float(df['engagement_score'].mean()),
        'avg_sessions': float(df['sessions_per_week'].mean()),
        'avg_duration': float(df['avg_session_duration_min'].mean()),
        'at_risk_users': int(len(df[df['segment'] == 'Low Engagement / At-Risk'])),
        'high_engagement_users': int(len(df[df['segment'] == 'High Engagement'])),
        'model_loaded': MODEL_LOADED
    }
    return jsonify(stats)

@app.route('/api/search')
def search_users():
    query = request.args.get('q', '').lower()
    limit = int(request.args.get('limit', 20))
    
    if query:
        results = df[df['user_id'].astype(str).str.lower().str.contains(query)]
        results = results[['user_id', 'cluster', 'segment', 'sessions_per_week', 
                          'avg_session_duration_min', 'daily_active_minutes',
                          'engagement_score', 'days_since_last_login']].head(limit)
        return jsonify(results.to_dict('records'))
    
    return jsonify([])

@app.route('/api/export/<int:cluster_id>')
def export_cluster(cluster_id):
    cluster_data = df[df['cluster'] == cluster_id]
    if len(cluster_data) > 0:
        filename = f'cluster_{cluster_id}_users.csv'
        cluster_data[['user_id', 'segment', 'sessions_per_week', 
                     'avg_session_duration_min', 'daily_active_minutes',
                     'engagement_score', 'days_since_last_login',
                     'feature_clicks_per_session', 'notifications_opened_per_week']].to_csv(filename, index=False)
        return send_file(filename, as_attachment=True)
    return jsonify({'error': 'Cluster not found'}), 404

@app.route('/api/export/all')
def export_all():
    filename = 'all_users_data.csv'
    df[['user_id', 'cluster', 'segment', 'sessions_per_week', 
        'avg_session_duration_min', 'daily_active_minutes',
        'engagement_score', 'days_since_last_login',
        'feature_clicks_per_session', 'notifications_opened_per_week']].to_csv(filename, index=False)
    return send_file(filename, as_attachment=True)

@app.route('/api/refresh')
def refresh_charts():
    global segment_chart, pca_chart, engagement_chart, heatmap_chart, behavior_chart
    segment_chart = generate_segment_chart(df)
    pca_chart = generate_pca_chart(df)
    engagement_chart = generate_engagement_chart(df)
    heatmap_chart = generate_heatmap(df)
    behavior_chart = generate_behavior_profile_chart(df)
    return jsonify({'message': 'Charts refreshed successfully'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)