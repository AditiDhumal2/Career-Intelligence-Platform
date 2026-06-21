"""
RAG (Retrieval-Augmented Generation) Retriever
Semantic search over career data using vector embeddings
"""

import pandas as pd
import numpy as np
from typing import List, Dict
import json
from pathlib import Path

# Try to import optional dependencies
try:
    import chromadb
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

class RAGRetriever:
    """
    RAG-based retrieval for career data
    Uses embeddings for semantic search
    """
    
    def __init__(self, df: pd.DataFrame, collection_name: str = "career_data"):
        """
        Initialize RAG retriever
        
        Args:
            df: Job data DataFrame
            collection_name: Name for the vector collection
        """
        self.df = df
        self.collection_name = collection_name
        self.collection = None
        self.model = None
        
        if CHROMADB_AVAILABLE and SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
                self.client = chromadb.PersistentClient(path="data/chroma_db")
                
                try:
                    self.collection = self.client.get_collection(collection_name)
                except:
                    self.collection = self._create_collection()
            except Exception as e:
                print(f"⚠️ RAG initialization failed: {e}")
    
    def _create_collection(self):
        """Create vector collection from job data"""
        print("🔧 Creating RAG vector collection...")
        
        collection = self.client.create_collection(self.collection_name)
        
        # Prepare documents
        documents = []
        metadatas = []
        ids = []
        
        for idx, row in self.df.iterrows():
            doc_text = f"""
            Job Title: {row['job_title']}
            Skills Required: {row['skill_required']}
            Salary: ${row['avg_salary']:,.0f}
            Location: {row['location']}
            Industry: {row['industry']}
            Demand Score: {row['demand_score']}
            """
            
            documents.append(doc_text)
            metadatas.append({
                'job_title': row['job_title'],
                'salary': float(row['avg_salary']),
                'location': row['location'],
                'industry': row['industry']
            })
            ids.append(f"job_{idx}")
        
        # Generate embeddings and add to collection
        embeddings = self.model.encode(documents)
        
        collection.add(
            documents=documents,
            embeddings=embeddings.tolist(),
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"✅ Created collection with {len(documents)} documents")
        return collection
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for relevant documents using semantic similarity
        
        Args:
            query: User query
            top_k: Number of results to return
            
        Returns:
            List of relevant documents
        """
        if self.collection is None or self.model is None:
            return self._fallback_search(query, top_k)
        
        try:
            query_embedding = self.model.encode(query)
            
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=top_k
            )
            
            return self._format_results(results)
        except Exception as e:
            print(f"Search error: {e}")
            return self._fallback_search(query, top_k)
    
    def _format_results(self, results) -> List[Dict]:
        """Format search results for display"""
        if not results or not results['documents']:
            return []
        
        formatted = []
        for i in range(len(results['documents'][0])):
            formatted.append({
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                'distance': results['distances'][0][i] if results.get('distances') else None
            })
        
        return formatted
    
    def _fallback_search(self, query: str, top_k: int) -> List[Dict]:
        """Fallback search using keyword matching"""
        results = []
        query_lower = query.lower()
        
        for idx, row in self.df.iterrows():
            text = f"{row['job_title']} {row['skill_required']} {row['location']}"
            if any(word in text.lower() for word in query_lower.split()):
                results.append({
                    'content': f"Job: {row['job_title']}\nSkills: {row['skill_required']}",
                    'metadata': {
                        'job_title': row['job_title'],
                        'salary': float(row['avg_salary']),
                        'location': row['location']
                    }
                })
        
        return results[:top_k]
    
    def get_job_recommendations(self, user_skills: List[str]) -> List[Dict]:
        """
        Get job recommendations based on user skills
        
        Args:
            user_skills: List of user's skills
            
        Returns:
            List of recommended jobs
        """
        query = f"Jobs requiring {', '.join(user_skills)} skills"
        results = self.search(query, top_k=10)
        
        recommendations = []
        for result in results:
            metadata = result.get('metadata', {})
            content = result.get('content', '')
            match_score = sum(1 for skill in user_skills if skill in content)
            
            recommendations.append({
                'job_title': metadata.get('job_title', 'Unknown'),
                'salary': metadata.get('salary', 0),
                'location': metadata.get('location', ''),
                'match_score': match_score,
                'content': content
            })
        
        return sorted(recommendations, key=lambda x: x['match_score'], reverse=True)