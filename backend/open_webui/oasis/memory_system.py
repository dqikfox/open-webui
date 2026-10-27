import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

log = logging.getLogger(__name__)


class OasisMemory:
    """Memory system for OASIS agent"""
    
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.short_term: List[Dict[str, Any]] = []
        self.long_term: Dict[str, Any] = {}
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """Add a message to short-term memory"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.short_term.append(message)
        
        # Trim if exceeds max size
        if len(self.short_term) > self.max_size:
            self.short_term = self.short_term[-self.max_size:]
        
        log.debug(f"Added message to memory: {role}")
    
    def get_recent(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get recent messages"""
        return self.short_term[-count:]
    
    def get_context(self) -> str:
        """Get formatted context from recent messages"""
        recent = self.get_recent(5)
        return "\n".join([f"{msg['role']}: {msg['content']}" for msg in recent])
    
    def store_fact(self, key: str, value: Any):
        """Store a fact in long-term memory"""
        self.long_term[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        log.debug(f"Stored fact: {key}")
    
    def recall_fact(self, key: str) -> Optional[Any]:
        """Recall a fact from long-term memory"""
        fact = self.long_term.get(key)
        return fact["value"] if fact else None
    
    def clear_short_term(self):
        """Clear short-term memory"""
        self.short_term = []
        log.info("Short-term memory cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        return {
            "short_term_size": len(self.short_term),
            "long_term_size": len(self.long_term),
            "max_size": self.max_size
        }
