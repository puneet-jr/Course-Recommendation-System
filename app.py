import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from recommender import CourseRecommender

st.set_page_config(
    page_title="Course Recommender",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* CSS Variables for Theme */
    :root {
        --primary-gradient-start: #667eea;
        --primary-gradient-end: #764ba2;
        --success-color: #28a745;
        --text-primary: #ffffff;
        --text-secondary: rgba(255, 255, 255, 0.7);
        --bg-overlay: rgba(255, 255, 255, 0.05);
        --border-color: rgba(102, 126, 234, 0.3);
        --shadow-light: 0 2px 4px rgba(0, 0, 0, 0.1);
        --shadow-medium: 0 4px 8px rgba(0, 0, 0, 0.15);
        --shadow-heavy: 0 10px 20px rgba(0, 0, 0, 0.2);
        --transition-fast: 0.2s ease;
        --transition-medium: 0.3s ease;
        --border-radius-sm: 10px;
        --border-radius-md: 15px;
        --border-radius-lg: 25px;
    }
    
    /* Typography */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: var(--primary-gradient-start);
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 2rem;
        letter-spacing: -0.5px;
    }
    
    /* Card Components */
    .card {
        padding: 2rem;
        border-radius: var(--border-radius-md);
        margin: 1rem 0;
        transition: transform var(--transition-medium), box-shadow var(--transition-medium);
    }
    
    .course-card {
        background: linear-gradient(135deg, var(--primary-gradient-start) 0%, var(--primary-gradient-end) 100%);
        box-shadow: var(--shadow-heavy);
        color: var(--text-primary);
    }
    
    .course-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
    }
    
    .course-card h3 {
        color: var(--text-primary);
        margin: 0 0 1rem 0;
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    /* Stat Container */
    .stat-container {
        background: var(--bg-overlay);
        padding: 2rem;
        border-radius: var(--border-radius-md);
        text-align: center;
        border: 2px solid var(--border-color);
        backdrop-filter: blur(10px);
        transition: transform var(--transition-medium), border-color var(--transition-medium);
    }
    
    .stat-container:hover {
        transform: translateY(-3px);
        border-color: rgba(102, 126, 234, 0.6);
    }
    
    .stat-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1;
    }
    
    /* Feature Box */
    .feature-box {
        background: var(--bg-overlay);
        padding: 1.5rem;
        border-radius: var(--border-radius-sm);
        border-left: 4px solid var(--success-color);
        margin: 1rem 0;
        box-shadow: var(--shadow-medium);
        backdrop-filter: blur(10px);
        transition: transform var(--transition-fast), box-shadow var(--transition-fast);
    }
    
    .feature-box:hover {
        transform: translateX(5px);
        box-shadow: var(--shadow-heavy);
    }
    
    .feature-box h4 {
        color: var(--success-color);
        margin: 0 0 0.5rem 0;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    .feature-box p {
        color: rgba(255, 255, 255, 0.9);
        margin: 0;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(90deg, var(--primary-gradient-start) 0%, var(--primary-gradient-end) 100%);
        color: var(--text-primary);
        border: none;
        padding: 0.75rem 2rem;
        border-radius: var(--border-radius-lg);
        font-weight: 600;
        font-size: 1rem;
        transition: transform var(--transition-fast), box-shadow var(--transition-fast);
        cursor: pointer;
        box-shadow: var(--shadow-medium);
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: var(--shadow-heavy);
    }
    
    .stButton > button:active {
        transform: scale(0.98);
    }
    
    /* Responsive Adjustments */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
            padding: 1rem 0;
        }
        
        .stat-value {
            font-size: 2rem;
        }
        
        .card {
            padding: 1.5rem;
        }
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_recommender():
    try:
        return CourseRecommender(
            courses_file='data/courses.csv',
            interactions_file='data/user_interactions.csv',
            profiles_file='data/user_profiles.csv'
        )
    except Exception as e:
        st.error(f"Error loading system: {e}")
        return None


def display_stat_card(icon: str, label: str, value):
    st.markdown(f"""
        <div class="stat-container">
            <span class="stat-icon">{icon}</span>
            <div class="stat-label">{label}</div>
            <div class="stat-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)


def display_course_card(course: dict, index: int):
    st.markdown(f"""
        <div class="course-card">
            <h3>#{index} {course['title']}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.write(f"**Subject:** {course.get('subject', 'N/A')}")
        st.write(f"**Level:** {course.get('level', 'N/A')}")
    
    with col2:
        rating = course.get('rating', 0)
        st.metric("Rating", f"{rating:.1f}/5.0")
        st.progress(rating / 5.0)
    
    with col3:
        match_score = course.get('similarity_score', 0) * 100
        st.metric("Match", f"{match_score:.0f}%")
        st.progress(match_score / 100)
    
    with col4:
        st.metric("Students", f"{int(course.get('students', 0)):,}")
        st.metric("Duration", f"{course.get('duration', 0)}h")
    
    with st.expander("View Description"):
        st.write(course.get('description', 'No description available'))
    
    st.markdown("---")


def create_subject_chart(recommender):
    courses_df = recommender.courses_df
    subject_counts = courses_df['subject'].value_counts().reset_index()
    subject_counts.columns = ['Subject', 'Count']
    
    fig = px.bar(
        subject_counts,
        x='Subject',
        y='Count',
        title='Courses by Subject',
        color='Count',
        color_continuous_scale='Blues',
        labels={'Count': 'Number of Courses'}
    )
    fig.update_layout(height=400)
    return fig


def create_level_distribution_chart(recommender):
    courses_df = recommender.courses_df
    level_counts = courses_df['level'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=level_counts.index,
        values=level_counts.values,
        hole=0.4,
        marker_colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    )])
    fig.update_layout(title='Course Difficulty Distribution', height=400)
    return fig


def create_rating_distribution(recommender):
    courses_df = recommender.courses_df
    
    fig = px.histogram(
        courses_df,
        x='rating',
        nbins=20,
        title='Course Rating Distribution',
        labels={'rating': 'Rating', 'count': 'Number of Courses'},
        color_discrete_sequence=['#667eea']
    )
    fig.update_layout(height=400)
    return fig


def show_trending_courses(recommender):
    trending = recommender.get_trending_courses(5)
    
    st.subheader("Trending Courses")
    
    for course in trending:
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        
        with col1:
            st.write(f"**{course['title']}**")
            st.caption(f"{course['subject']} • {course['level']}")
        
        with col2:
            st.metric("Rating", f"{course['rating']:.1f}")
        
        with col3:
            st.metric("Students", f"{int(course['students']):,}")
        
        with col4:
            st.metric("Score", f"{int(course['trending_score'])}")


def show_user_dashboard(recommender, user_id):
    user_stats = recommender.get_user_statistics(user_id)
    user_interactions = recommender.interactions_df[
        recommender.interactions_df['user_id'] == user_id
    ]
    
    if user_stats:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            display_stat_card("📚", "Courses Enrolled", user_stats['total_courses'])
        
        with col2:
            display_stat_card("⭐", "Avg Rating Given", user_stats['avg_rating'])
        
        with col3:
            display_stat_card("📖", "Favorite Subject", user_stats['favorite_subject'])
        
        with col4:
            display_stat_card("✓", "Completed", user_stats['completed_courses'])
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            subject_counts = user_interactions['subject'].value_counts()
            fig = px.bar(
                x=subject_counts.index,
                y=subject_counts.values,
                title='Your Learning Interests',
                labels={'x': 'Subject', 'y': 'Courses'},
                color=subject_counts.values,
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            level_counts = user_interactions['level'].value_counts()
            fig = go.Figure(data=[go.Pie(
                labels=level_counts.index,
                values=level_counts.values,
                hole=0.4,
                marker_colors=['#1f77b4', '#ff7f0e', '#2ca02c']
            )])
            fig.update_layout(title='Course Levels')
            st.plotly_chart(fig, use_container_width=True)


def main():
    st.markdown('<div class="main-header">Smart Course Recommender</div>', unsafe_allow_html=True)
    
    recommender = load_recommender()
    if recommender is None:
        st.error("Failed to load the system. Please check your data files.")
        return
    
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Choose a page:",
        ["Home", "Find Similar", "For You", "Search Courses", "Analytics"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Platform Overview")
    stats = recommender.get_platform_statistics()
    st.sidebar.metric("Total Courses", stats['total_courses'])
    st.sidebar.metric("Active Users", stats['total_users'])
    st.sidebar.metric("Platform Rating", f"{stats['avg_course_rating']:.1f}")
    st.sidebar.metric("Subjects", stats['subjects_count'])
    
    if page == "Home":
        st.header("Welcome to Your Learning Journey")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            display_stat_card("📚", "Courses", stats['total_courses'])
        
        with col2:
            display_stat_card("👥", "Learners", stats['total_users'])
        
        with col3:
            display_stat_card("⭐", "Avg Rating", f"{stats['avg_course_rating']:.1f}")
        
        with col4:
            display_stat_card("🎯", "Categories", stats['subjects_count'])
        
        st.markdown("---")
        
        show_trending_courses(recommender)
        
        st.markdown("---")
        
        st.subheader("Key Features")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="feature-box">
                <h4>Smart Recommendations</h4>
                <p>Get personalized course suggestions based on your interests and learning history</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-box">
                <h4>Learning Analytics</h4>
                <p>Track your progress and discover insights about your learning journey</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-box">
                <h4>Find Similar Courses</h4>
                <p>Discover courses similar to ones you already love</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-box">
                <h4>Advanced Search</h4>
                <p>Filter and find exactly what you're looking for</p>
            </div>
            """, unsafe_allow_html=True)
    
    elif page == "Find Similar":
        st.header("Find Similar Courses")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            courses = recommender.get_all_courses()
            selected_course = st.selectbox(
                "Select a course you like:",
                [""] + courses,
                help="Choose a course to find similar ones"
            )
        
        with col2:
            top_n = st.slider("Number of results:", 3, 10, 5)
        
        if selected_course:
            course_details = recommender.get_course_details(selected_course)
            
            if course_details:
                st.info(f"**Subject:** {course_details['subject']} | **Level:** {course_details['level']} | **Rating:** {course_details.get('rating', 0):.1f}")
            
            st.markdown("---")
            st.subheader(f"Courses similar to: **{selected_course}**")
            
            with st.spinner("Finding similar courses..."):
                recommendations = recommender.recommend_by_course(selected_course, top_n)
            
            if recommendations:
                for i, course in enumerate(recommendations, 1):
                    display_course_card(course, i)
            else:
                st.warning("No similar courses found.")
    
    elif page == "For You":
        st.header("Your Personalized Recommendations")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            users = recommender.get_all_users()
            selected_user = st.selectbox(
                "Select your profile:",
                [""] + users,
                help="Choose a user to see personalized recommendations"
            )
        
        with col2:
            top_n = st.slider("Number of recommendations:", 3, 10, 5)
        
        if selected_user:
            # Show user dashboard
            show_user_dashboard(recommender, selected_user)
            
            st.markdown("---")
            st.subheader(f"Recommended Courses for You")
            
            with st.spinner("Analyzing your preferences..."):
                recommendations = recommender.recommend_by_user(selected_user, top_n)
            
            if recommendations:
                for i, course in enumerate(recommendations, 1):
                    display_course_card(course, i)
            else:
                st.warning("No recommendations available. Start taking some courses!")
    
    elif page == "Search Courses":
        st.header("Search & Filter Courses")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            search_query = st.text_input("Keyword:", placeholder="e.g., Python, Design")
        
        with col2:
            subjects = ["All"] + recommender.get_all_subjects()
            selected_subject = st.selectbox("Subject:", subjects)
        
        with col3:
            levels = ["All"] + recommender.get_all_levels()
            selected_level = st.selectbox("Level:", levels)
        
        with col4:
            min_rating = st.slider("Min Rating:", 0.0, 5.0, 0.0, 0.5)
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            search_clicked = st.button("Search", type="primary", use_container_width=True)
        with col2:
            if st.button("Reset", use_container_width=True):
                st.rerun()
        
        if search_clicked or search_query or selected_subject != "All" or selected_level != "All" or min_rating > 0:
            with st.spinner("Searching..."):
                results = recommender.search_courses(
                    query=search_query if search_query else None,
                    subject=selected_subject if selected_subject != "All" else None,
                    level=selected_level if selected_level != "All" else None,
                    min_rating=min_rating
                )
            
            st.markdown("---")
            st.subheader(f"Found {len(results)} courses")
            
            if not results.empty:
                # Sorting options
                sort_by = st.selectbox(
                    "Sort by:",
                    ["Rating (High to Low)", "Students (High to Low)", "Duration (Short to Long)", "Title (A-Z)"]
                )
                
                if sort_by == "Rating (High to Low)":
                    results = results.sort_values('rating', ascending=False)
                elif sort_by == "Students (High to Low)":
                    results = results.sort_values('students', ascending=False)
                elif sort_by == "Duration (Short to Long)":
                    results = results.sort_values('duration')
                else:
                    results = results.sort_values('title')
                
                for idx, (row_idx, course) in enumerate(results.iterrows(), 1):
                    display_course_card(course.to_dict(), idx)
            else:
                st.warning("No courses found. Try different filters.")
    
    elif page == "Analytics":
        st.header("Platform Analytics")
        
        tab1, tab2, tab3 = st.tabs(["Course Insights", "User Trends", "Ratings"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(create_subject_chart(recommender), use_container_width=True)
            
            with col2:
                st.plotly_chart(create_level_distribution_chart(recommender), use_container_width=True)
            
            st.subheader("Top Rated Courses")
            top_courses = recommender.courses_df.nlargest(10, 'rating')[
                ['title', 'subject', 'level', 'rating', 'students']
            ]
            st.dataframe(top_courses, use_container_width=True, hide_index=True)
        
        with tab2:
            st.info("User engagement analytics")
            
            user_subject_prefs = recommender.interactions_df['subject'].value_counts().reset_index()
            user_subject_prefs.columns = ['Subject', 'Enrollments']
            
            fig = px.bar(
                user_subject_prefs,
                x='Subject',
                y='Enrollments',
                title='Most Popular Subjects',
                color='Enrollments',
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.plotly_chart(create_rating_distribution(recommender), use_container_width=True)
            
            avg_by_subject = recommender.courses_df.groupby('subject')['rating'].mean().reset_index()
            avg_by_subject.columns = ['Subject', 'Average Rating']
            
            fig = px.bar(
                avg_by_subject,
                x='Subject',
                y='Average Rating',
                title='Average Rating by Subject',
                color='Average Rating',
                color_continuous_scale='RdYlGn',
                range_y=[0, 5]
            )
            st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()