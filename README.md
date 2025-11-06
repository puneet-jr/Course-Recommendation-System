# Smart Course Recommendation System

A comprehensive, AI-powered course recommendation system built with Streamlit that provides personalized learning recommendations using content-based filtering and collaborative filtering techniques.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Data Description](#data-description)
- [Algorithm Details](#algorithm-details)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)

## 🎯 Overview

The Smart Course Recommendation System is a web application that helps learners discover relevant courses based on their interests, learning history, and preferences. The system uses machine learning algorithms to provide personalized course suggestions and detailed analytics about learning patterns.

### Key Capabilities

- **Personalized Recommendations**: Get course suggestions based on user preferences and history
- **Course Similarity**: Find courses similar to ones you already enjoy
- **Advanced Search**: Filter courses by subject, level, rating, and keywords
- **Learning Analytics**: Track progress and visualize learning patterns
- **Platform Insights**: Comprehensive analytics about course offerings and user engagement

## ✨ Features

### 🏠 Home Dashboard
- Platform overview with key statistics
- Trending courses based on popularity and ratings
- Feature highlights and system capabilities

### 🔍 Find Similar Courses
- Content-based recommendations using TF-IDF and cosine similarity
- Find courses similar to ones you already like
- Match percentage scoring for each recommendation

### 👤 Personalized Recommendations
- User-specific course suggestions
- Learning history and preference analysis
- Individual user dashboard with statistics

### 📚 Search & Filter
- Advanced search with multiple filters
- Sort by rating, popularity, duration, or title
- Real-time course discovery

### 📊 Analytics
- Course distribution by subject and difficulty level
- Rating analysis and trends
- User engagement metrics
- Platform performance insights

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step-by-Step Setup

1. **Clone or Download the Project**
   ```bash
   # If using git
   git clone <repository-url>
   cd puneet-jr-course-recommendation-system
   ```

2. **Create Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Data Files**
   Ensure all CSV files are present in the `data/` directory:
   - `courses.csv`
   - `user_interactions.csv`
   - `user_profiles.csv`
   - `course_reviews.csv`
   - `learning_paths.csv`
   - `user_learning_history.csv`
   - `user_preferences.csv`

5. **Run the Application**
   ```bash
   streamlit run app.py
   ```

6. **Access the Application**
   Open your web browser and navigate to:
   ```
   http://localhost:8501
   ```

## 📁 Project Structure

```
puneet-jr-course-recommendation-system/
├── app.py                 # Main Streamlit application
├── recommender.py         # Recommendation engine core logic
├── requirements.txt       # Python dependencies
└── data/
    ├── courses.csv                # Course catalog with details
    ├── user_interactions.csv      # User-course interactions and ratings
    ├── user_profiles.csv          # User learning profiles and statistics
    ├── course_reviews.csv         # Detailed course reviews
    ├── learning_paths.csv         # Structured learning paths
    ├── user_learning_history.csv  # User enrollment and progress
    └── user_preferences.csv       # User learning preferences
```

## 📊 Data Description

### Core Data Files

1. **courses.csv** - Course Catalog
   - `course_id`: Unique identifier for each course
   - `title`: Course name
   - `subject`: Category (Programming, Design, Business, etc.)
   - `level`: Difficulty (Beginner, Intermediate, Advanced)
   - `description`: Detailed course description
   - `rating`: Average user rating (0-5)
   - `students`: Number of enrolled students
   - `duration`: Course length in hours
   - `instructor`: Course instructor name
   - `skills`: Skills covered in the course

2. **user_interactions.csv** - User Engagement
   - `user_id`: Unique user identifier
   - `course_id`: Course the user interacted with
   - `rating`: User's rating for the course
   - `subject`, `level`: Course metadata
   - Various engagement metrics

3. **user_profiles.csv** - User Learning Patterns
   - `user_id`: Unique user identifier
   - `avg_study_hours`: Average weekly study time
   - `courses_completed`: Total courses finished
   - `learning_consistency`: Consistency score (0-1)

4. **Additional Supporting Files**
   - `user_preferences.csv`: User learning preferences and goals
   - `user_learning_history.csv`: Course progress and completion data
   - `course_reviews.csv`: Detailed user reviews and feedback
   - `learning_paths.csv`: Curated learning sequences

## 🧠 Algorithm Details

### Recommendation Engine

The system uses a hybrid approach combining:

1. **Content-Based Filtering (Primary)**
   - **TF-IDF Vectorization**: Converts course titles, subjects, levels, and descriptions into numerical vectors
   - **Cosine Similarity**: Measures similarity between courses based on their content features
   - **Feature Combination**: Combines title, subject, level, and description for comprehensive analysis

2. **Collaborative Filtering Elements**
   - User preference analysis based on interaction history
   - Rating patterns and subject preferences
   - Learning behavior modeling

### Key Methods

- `recommend_by_course()`: Finds similar courses using content similarity
- `recommend_by_user()`: Provides personalized recommendations based on user history
- `search_courses()`: Advanced filtering and keyword search
- `get_trending_courses()`: Identifies popular courses using engagement metrics

## ⚙️ Configuration

### Customizing the System

1. **Adding New Courses**
   - Update `data/courses.csv` with new course entries
   - Ensure consistent formatting for all columns

2. **Modifying User Data**
   - Add new users to `user_interactions.csv` and `user_profiles.csv`
   - Update interaction history as users engage with courses

3. **Algorithm Tuning**
   - Adjust TF-IDF parameters in `recommender.py`
   - Modify similarity thresholds in recommendation methods
   - Update trending score calculation weights

### Streamlit Configuration

The application uses Streamlit's wide layout with custom CSS styling for an enhanced user experience. Key configuration in `app.py`:

```python
st.set_page_config(
    page_title="Course Recommender",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

## 🛠️ Troubleshooting

### Common Issues

1. **Module Not Found Errors**
   ```bash
   # Ensure all dependencies are installed
   pip install -r requirements.txt
   ```

2. **Data File Errors**
   - Verify all CSV files are in the `data/` directory
   - Check file permissions and paths
   - Ensure CSV files are properly formatted

3. **Memory Issues**
   - The system loads all data into memory
   - For large datasets, consider chunk processing
   - Monitor system resources during operation

4. **Port Already in Use**
   ```bash
   # Use different port
   streamlit run app.py --server.port 8502
   ```

### Performance Tips

- The system caches the recommender for better performance
- Large datasets may require additional optimization
- Consider incremental loading for very large course catalogs

## 🔮 Future Enhancements

1. **Advanced Algorithms**
   - Matrix factorization for improved recommendations
   - Deep learning-based content understanding
   - Real-time preference adaptation

2. **Enhanced Analytics**
   - Predictive learning path success rates
   - Skill gap analysis and recommendations
   - Career progression tracking

3. **User Experience**
   - Social features and peer recommendations
   - Mobile application version
   - Offline functionality

4. **Integration Capabilities**
   - API endpoints for external systems
   - LMS integration support
   - Multi-language support
