import logging
from typing import Dict, Any, List
from collections import deque

log = logging.getLogger(__name__)

class SmartContextManager:
    """Intelligent context management with auto-pruning"""
    
    def __init__(self, max_tokens: int = 4096):
        self.max_tokens = max_tokens
        self.contexts = {}
        
    def add_context(self, session_id: str, message: Dict[str, Any]):
        """Add message to context"""
        if session_id not in self.contexts:
            self.contexts[session_id] = {
                "messages": deque(maxlen=100),
                "summary": "",
                "token_count": 0
            }
        
        self.contexts[session_id]["messages"].append(message)
        self.contexts[session_id]["token_count"] += self._estimate_tokens(message)
        
        # Auto-prune if needed
        if self.contexts[session_id]["token_count"] > self.max_tokens:
            self._prune_context(session_id)
    
    def _estimate_tokens(self, message: Dict) -> int:
        """Estimate token count"""
        content = str(message.get("content", ""))
        return len(content) // 4  # Rough estimate
    
    def _prune_context(self, session_id: str):
        """Intelligently prune context"""
        ctx = self.contexts[session_id]
        
        # Keep first and last messages, summarize middle
        if len(ctx["messages"]) > 10:
            first_5 = list(ctx["messages"])[:5]
            last_5 = list(ctx["messages"])[-5:]
            middle = list(ctx["messages"])[5:-5]
            
            # Create summary of middle messages
            summary = f"[Summary of {len(middle)} messages]"
            
            ctx["messages"].clear()
            for msg in first_5:
                ctx["messages"].append(msg)
            ctx["messages"].append({"role": "system", "content": summary})
            for msg in last_5:
                ctx["messages"].append(msg)
            
            ctx["token_count"] = sum(self._estimate_tokens(m) for m in ctx["messages"])
    
    def get_context(self, session_id: str) -> List[Dict]:
        """Get context for session"""
        if session_id not in self.contexts:
            return []
        return list(self.contexts[session_id]["messages"])
    
    def clear_context(self, session_id: str):
        """Clear context"""
        if session_id in self.contexts:
            del self.contexts[session_id]
    
    def get_stats(self, session_id: str) -> Dict:
        """Get context statistics"""
        if session_id not in self.contexts:
            return {"messages": 0, "tokens": 0}
        
        ctx = self.contexts[session_id]
        return {
            "messages": len(ctx["messages"]),
            "tokens": ctx["token_count"],
            "max_tokens": self.max_tokens
        }

context_manager = SmartContextManager()
