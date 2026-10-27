import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

log = logging.getLogger(__name__)

class KnowledgeBase:
    """Persistent knowledge base for agents"""
    
    def __init__(self, storage_path: str = "/tmp/oasis_kb.json"):
        self.storage_path = storage_path
        self.knowledge = self._load()
        
    def _load(self) -> Dict:
        """Load knowledge from disk"""
        try:
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except:
            return {
                "facts": [],
                "patterns": [],
                "solutions": [],
                "learnings": []
            }
    
    def _save(self):
        """Save knowledge to disk"""
        try:
            with open(self.storage_path, 'w') as f:
                json.dump(self.knowledge, f, indent=2)
        except Exception as e:
            log.error(f"Save error: {e}")
    
    def add_fact(self, category: str, content: str, metadata: Optional[Dict] = None):
        """Add fact to knowledge base"""
        fact = {
            "category": category,
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }
        self.knowledge["facts"].append(fact)
        self._save()
        return {"status": "success", "fact_id": len(self.knowledge["facts"]) - 1}
    
    def add_pattern(self, pattern_type: str, description: str, examples: List[str]):
        """Add code pattern"""
        pattern = {
            "type": pattern_type,
            "description": description,
            "examples": examples,
            "timestamp": datetime.now().isoformat()
        }
        self.knowledge["patterns"].append(pattern)
        self._save()
        return {"status": "success"}
    
    def add_solution(self, problem: str, solution: str, tags: List[str]):
        """Add problem-solution pair"""
        sol = {
            "problem": problem,
            "solution": solution,
            "tags": tags,
            "timestamp": datetime.now().isoformat()
        }
        self.knowledge["solutions"].append(sol)
        self._save()
        return {"status": "success"}
    
    def add_learning(self, topic: str, insight: str, source: str):
        """Add learning insight"""
        learning = {
            "topic": topic,
            "insight": insight,
            "source": source,
            "timestamp": datetime.now().isoformat()
        }
        self.knowledge["learnings"].append(learning)
        self._save()
        return {"status": "success"}
    
    def search(self, query: str, category: Optional[str] = None) -> List[Dict]:
        """Search knowledge base"""
        results = []
        query_lower = query.lower()
        
        for cat in ["facts", "patterns", "solutions", "learnings"]:
            if category and category != cat:
                continue
            
            for item in self.knowledge[cat]:
                content = json.dumps(item).lower()
                if query_lower in content:
                    results.append({"category": cat, "item": item})
        
        return results
    
    def get_stats(self) -> Dict:
        """Get knowledge base statistics"""
        return {
            "facts": len(self.knowledge["facts"]),
            "patterns": len(self.knowledge["patterns"]),
            "solutions": len(self.knowledge["solutions"]),
            "learnings": len(self.knowledge["learnings"]),
            "total": sum(len(v) for v in self.knowledge.values())
        }
    
    def export(self) -> Dict:
        """Export entire knowledge base"""
        return self.knowledge
    
    def clear(self, category: Optional[str] = None):
        """Clear knowledge base"""
        if category:
            self.knowledge[category] = []
        else:
            self.knowledge = {"facts": [], "patterns": [], "solutions": [], "learnings": []}
        self._save()
        return {"status": "success"}

knowledge_base = KnowledgeBase()
