import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Optional
import warnings
warnings.filterwarnings('ignore')


class CourseRecommender:
    
    def __init__(self, courses_file: str, interactions_file: str, profiles_file: str):
        try:
            self.courses_df = pd.read_csv(courses_file)
            self.interactions_df = pd.read_csv(interactions_file)
            self.profiles_df = pd.read_csv(profiles_file)
            
            self._prepare_data()
            
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Data file not found: {e}")
    
    def _prepare_data(self) -> None:
        self.courses_df['course_id'] = self.courses_df['course_id'].astype(str).str.strip()
        
        self.courses_df['title'] = self.courses_df['title'].fillna('')
        self.courses_df['subject'] = self.courses_df['subject'].fillna('')
        self.courses_df['level'] = self.courses_df['level'].fillna('')
        self.courses_df['description'] = self.courses_df['description'].fillna('')
        
        self.courses_df['combined_features'] = (
            self.courses_df['title'] + ' ' +
            self.courses_df['subject'] + ' ' +
            self.courses_df['level'] + ' ' +
            self.courses_df['description']
        )
        
        self.tfidf = TfidfVectorizer(stop_words='english', max_features=500)
        self.tfidf_matrix = self.tfidf.fit_transform(self.courses_df['combined_features'])
        
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix)
        
        self.course_id_to_idx = {
            course_id: idx for idx, course_id in enumerate(self.courses_df['course_id'])
        }
        
        self.interactions_df['user_id'] = self.interactions_df['user_id'].astype(str).str.strip()
        self.interactions_df['course_id'] = self.interactions_df['course_id'].astype(str).str.strip()
    
    def recommend_by_course(self, course_title: str, top_n: int = 5) -> List[Dict]:
        course_match = self.courses_df[self.courses_df['title'] == course_title]
        
        if course_match.empty:
            return []
        
        course_idx = course_match.index[0]
        
        sim_scores = list(enumerate(self.similarity_matrix[course_idx]))
        
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        sim_scores = sim_scores[1:top_n+1]
        
        recommendations = []
        for idx, score in sim_scores:
            course = self.courses_df.iloc[idx]
            match_percentage = round(score * 100, 1)
            
            recommendations.append({
                'course_id': course['course_id'],
                'title': course['title'],
                'subject': course['subject'],
                'level': course['level'],
                'description': course['description'][:200] + '...' if len(course['description']) > 200 else course['description'],
                'rating': course.get('rating', 0),
                'students': course.get('students', 0),
                'duration': course.get('duration', 0),
                'price': course.get('price', 0),
                'similarity_score': round(score, 3),
                'match_percentage': match_percentage
            })
        
        return recommendations
    
    def recommend_by_user(self, user_id: str, top_n: int = 5) -> List[Dict]:
        user_id = str(user_id).strip()
        
        user_courses = self.interactions_df[
            self.interactions_df['user_id'] == user_id
        ]
        
        if user_courses.empty:
            return []
        
        liked_courses = user_courses[user_courses['rating'] >= 4.5]
        
        if liked_courses.empty:
            liked_courses = user_courses
        
        liked_course_ids = liked_courses['course_id'].unique()
        liked_indices = []
        
        for course_id in liked_course_ids:
            if course_id in self.course_id_to_idx:
                liked_indices.append(self.course_id_to_idx[course_id])
        
        if not liked_indices:
            return []
        
        avg_similarity = np.zeros(len(self.courses_df))
        for idx in liked_indices:
            avg_similarity += self.similarity_matrix[idx]
        avg_similarity /= len(liked_indices)
        
        taken_course_ids = set(user_courses['course_id'].unique())
        
        recommendations = []
        for idx, score in enumerate(avg_similarity):
            course_id = self.courses_df.iloc[idx]['course_id']
            
            if course_id not in taken_course_ids:
                course = self.courses_df.iloc[idx]
                match_percentage = round(score * 100, 1)
                
                recommendations.append({
                    'course_id': course['course_id'],
                    'title': course['title'],
                    'subject': course['subject'],
                    'level': course['level'],
                    'description': course['description'][:200] + '...' if len(course['description']) > 200 else course['description'],
                    'rating': course.get('rating', 0),
                    'students': course.get('students', 0),
                    'duration': course.get('duration', 0),
                    'price': course.get('price', 0),
                    'similarity_score': round(score, 3),
                    'match_percentage': match_percentage
                })
        
        recommendations = sorted(recommendations, key=lambda x: x['similarity_score'], reverse=True)
        return recommendations[:top_n]
    
    def search_courses(self, query: Optional[str] = None, subject: Optional[str] = None, 
                      level: Optional[str] = None, min_rating: float = 0.0) -> pd.DataFrame:
        filtered_df = self.courses_df.copy()
        
        if query and query.strip():
            mask = (
                filtered_df['title'].str.contains(query, case=False, na=False) |
                filtered_df['description'].str.contains(query, case=False, na=False) |
                filtered_df['subject'].str.contains(query, case=False, na=False)
            )
            filtered_df = filtered_df[mask]
        
        if subject and subject != "All":
            filtered_df = filtered_df[filtered_df['subject'] == subject]
        
        if level and level != "All":
            filtered_df = filtered_df[filtered_df['level'] == level]
        
        if 'rating' in filtered_df.columns and min_rating > 0:
            filtered_df = filtered_df[filtered_df['rating'] >= min_rating]
        
        return filtered_df
    
    def get_all_courses(self) -> List[str]:
        return sorted(self.courses_df['title'].tolist())
    
    def get_all_users(self) -> List[str]:
        return sorted(self.interactions_df['user_id'].unique().tolist())
    
    def get_all_subjects(self) -> List[str]:
        return sorted(self.courses_df['subject'].unique().tolist())
    
    def get_all_levels(self) -> List[str]:
        return sorted(self.courses_df['level'].unique().tolist())
    
    def get_course_details(self, course_title: str) -> Optional[Dict]:
        course = self.courses_df[self.courses_df['title'] == course_title]
        
        if course.empty:
            return None
        
        return course.iloc[0].to_dict()
    
    def get_user_statistics(self, user_id: str) -> Optional[Dict]:
        user_id = str(user_id).strip()
        user_data = self.interactions_df[self.interactions_df['user_id'] == user_id]
        
        if user_data.empty:
            return None
        
        completed = len(user_data)
        in_progress = 0
        
        return {
            'total_courses': len(user_data),
            'avg_rating': round(user_data['rating'].mean(), 2),
            'favorite_subject': user_data['subject'].mode()[0] if len(user_data) > 0 else "N/A",
            'completed_courses': completed,
            'in_progress_courses': in_progress
        }
    
    def get_platform_statistics(self) -> Dict:
        return {
            'total_courses': len(self.courses_df),
            'total_users': len(self.profiles_df),
            'avg_course_rating': round(self.courses_df['rating'].mean(), 2) if 'rating' in self.courses_df.columns else 0,
            'subjects_count': self.courses_df['subject'].nunique(),
            'total_enrollments': len(self.interactions_df),
            'avg_students_per_course': int(self.courses_df['students'].mean()) if 'students' in self.courses_df.columns else 0
        }
    
    def get_trending_courses(self, top_n: int = 5) -> List[Dict]:
        trending = self.courses_df.copy()
        trending['trending_score'] = trending['rating'] * (trending['students'] ** 0.5)
        trending = trending.nlargest(top_n, 'trending_score')
        
        result = []
        for _, course in trending.iterrows():
            result.append({
                'course_id': course['course_id'],
                'title': course['title'],
                'subject': course['subject'],
                'level': course['level'],
                'rating': course['rating'],
                'students': course['students'],
                'duration': course.get('duration', 0),
                'trending_score': int(course['trending_score'])
            })
        
        return result
    
    def get_subject_distribution(self) -> Dict:
        return self.courses_df['subject'].value_counts().to_dict()
    
    def get_level_distribution(self) -> Dict:
        return self.courses_df['level'].value_counts().to_dict()
    