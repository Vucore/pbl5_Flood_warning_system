import csv
import os
from datetime import datetime
from typing import List, Dict, Optional

class ConversationLogger:
    def __init__(self, log_dir: str = "conversation_logs"):
        self.log_dir = log_dir
        self._ensure_log_directory()
        self.current_log_file = self._get_log_file_path()
        self._initialize_csv()

    def _ensure_log_directory(self):
        """Create log directory if it doesn't exist"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def _get_log_file_path(self) -> str:
        """Generate log file path based on current date"""
        current_date = datetime.now().strftime("%Y-%m-%d")
        return os.path.join(self.log_dir, f"conversation_log_{current_date}.csv")

    def _initialize_csv(self):
        """Initialize CSV file with headers if it doesn't exist"""
        if not os.path.exists(self.current_log_file):
            with open(self.current_log_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp',
                    'question',
                    'answer',
                    'rag_used',
                    'rag_documents',
                    'response_type'
                ])

    def log_conversation(
        self,
        question: str,
        answer: str,
        rag_used: bool = False,
        rag_documents: Optional[List[Dict]] = None,
        response_type: str = "unknown"
    ):
        """
        Log a conversation entry to CSV
        
        Args:
            question: User's question
            answer: Bot's response
            rag_used: Whether RAG was used for this response
            rag_documents: List of documents used by RAG (if any)
            response_type: Type of response (e.g., 'simple', 'chat', 'call')
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Format RAG documents if present
        rag_docs_str = ""
        if rag_documents:
            rag_docs_str = " | ".join([
                f"Doc{i+1}: {doc.page_content[:100]}..."
                for i, doc in enumerate(rag_documents)
            ])


        with open(self.current_log_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                question,
                answer,
                rag_used,
                rag_docs_str,
                response_type
            ]) 