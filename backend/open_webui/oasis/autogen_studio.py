import logging
import asyncio
import json
from typing import Optional, Dict, Any, List

log = logging.getLogger(__name__)

class AutoGenStudio:
    def __init__(self, llm_config: Optional[Dict] = None):
        self.llm_config = llm_config or {
            "model": "llama3.1",
            "base_url": "http://localhost:11434",
            "temperature": 0.7
        }
        self.llm = None
        self.agents = {}
        try:
            from open_webui.oasis.llm_connector import LLMConnector
            self.llm = LLMConnector()
            self._init_agents()
        except Exception as e:
            log.error(f"Failed to init AutoGen: {e}")
    
    def _init_agents(self):
        """Initialize agent personas"""
        self.agents = {
            "architect": {
                "name": "Architect",
                "role": "Software architect analyzing code and suggesting improvements",
                "system": "You are an expert software architect. Analyze code structure, design patterns, and suggest architectural improvements following OASIS patterns."
            },
            "developer": {
                "name": "Developer",
                "role": "Senior developer implementing features",
                "system": "You are a senior developer. Write clean, efficient code following OASIS conventions: PersistentConfig pattern, FastAPI routes, Svelte components."
            },
            "reviewer": {
                "name": "Reviewer",
                "role": "Code reviewer checking quality and security",
                "system": "You are a code reviewer. Check for security issues, performance problems, code quality, and adherence to best practices."
            },
            "optimizer": {
                "name": "Optimizer",
                "role": "Performance optimizer",
                "system": "You are a performance optimizer. Identify bottlenecks, suggest optimizations, and improve efficiency."
            }
        }
    
    async def _agent_chat(self, agent_name: str, prompt: str) -> str:
        """Chat with specific agent"""
        if not self.llm:
            return "LLM not available"
        
        agent = self.agents.get(agent_name, self.agents["architect"])
        full_prompt = f"{agent['system']}\n\n{prompt}"
        
        response = await self.llm.generate(full_prompt, model=self.llm_config["model"])
        return response
    
    async def _multi_agent_discussion(self, topic: str, agents: List[str]) -> List[Dict[str, str]]:
        """Multi-agent discussion"""
        discussion = []
        context = topic
        
        for agent_name in agents:
            response = await self._agent_chat(agent_name, f"{context}\n\nProvide your perspective.")
            discussion.append({
                "agent": agent_name,
                "message": response
            })
            context += f"\n\n{self.agents[agent_name]['name']}: {response[:500]}"
        
        return discussion
        
    async def analyze_codebase(self, file_path: str, content: str) -> Dict[str, Any]:
        """Analyze code with multi-agent review"""
        try:
            prompt = f"""Analyze this OASIS file:

File: {file_path}
Content:
{content[:2000]}

Provide:
1. Code quality (1-10)
2. Top 3 improvements
3. Security issues
4. Performance concerns
"""
            
            # Multi-agent analysis
            discussion = await self._multi_agent_discussion(
                prompt,
                ["reviewer", "optimizer"]
            )
            
            # Synthesize results
            synthesis = await self._agent_chat(
                "architect",
                f"Synthesize these reviews into actionable recommendations:\n{json.dumps(discussion)}"
            )
            
            return {
                "status": "success",
                "analysis": synthesis,
                "reviews": discussion,
                "file": file_path
            }
        except Exception as e:
            log.exception(e)
            return {"status": "error", "error": str(e)}
    
    async def suggest_enhancements(self, context: str) -> List[Dict[str, str]]:
        """Generate enhancement suggestions with multi-agent brainstorming"""
        try:
            prompt = f"""Context: {context}

Suggest 3 concrete enhancements for OASIS.

Format:
TITLE: <title>
DESCRIPTION: <description>
PRIORITY: <High/Medium/Low>
IMPLEMENTATION: <steps>
---
"""
            
            # Get suggestions from multiple agents
            architect_suggestions = await self._agent_chat("architect", prompt)
            developer_suggestions = await self._agent_chat("developer", prompt)
            
            # Parse and combine
            all_suggestions = self._parse_suggestions(architect_suggestions + "\n" + developer_suggestions)
            
            return all_suggestions[:5]  # Top 5
        except Exception as e:
            log.exception(e)
            return []
    
    async def auto_implement(self, feature_request: str, file_context: Dict[str, str]) -> Dict[str, Any]:
        """Auto-implement with multi-agent collaboration"""
        try:
            # Phase 1: Architecture
            design = await self._agent_chat(
                "architect",
                f"Design solution for: {feature_request}\nContext: {file_context}\nProvide architecture and file structure."
            )
            
            # Phase 2: Implementation
            code = await self._agent_chat(
                "developer",
                f"Implement this design:\n{design}\n\nFeature: {feature_request}\nProvide complete code."
            )
            
            # Phase 3: Review
            review = await self._agent_chat(
                "reviewer",
                f"Review this implementation:\n{code}\n\nCheck for issues and suggest fixes."
            )
            
            return {
                "status": "success",
                "design": design,
                "implementation": code,
                "review": review,
                "discussion": [
                    {"agent": "architect", "message": design},
                    {"agent": "developer", "message": code},
                    {"agent": "reviewer", "message": review}
                ]
            }
        except Exception as e:
            log.exception(e)
            return {"status": "error", "error": str(e)}
    
    async def continuous_improvement(self, scan_dirs: List[str]) -> Dict[str, Any]:
        """Continuous improvement scan with prioritization"""
        improvements = []
        priority_files = []
        
        for dir_path in scan_dirs:
            try:
                import os
                if not os.path.exists(dir_path):
                    continue
                    
                for root, _, files in os.walk(dir_path):
                    for file in files[:3]:  # Limit to 3 files per dir
                        if file.endswith(('.py', '.svelte')):
                            file_path = os.path.join(root, file)
                            priority_files.append(file_path)
            except Exception as e:
                log.error(f"Error scanning {dir_path}: {e}")
        
        # Analyze priority files
        for file_path in priority_files[:5]:  # Max 5 files
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                
                analysis = await self.analyze_codebase(file_path, content)
                if analysis["status"] == "success":
                    improvements.append(analysis)
            except Exception as e:
                log.error(f"Error analyzing {file_path}: {e}")
        
        # Generate summary
        if improvements:
            summary = await self._agent_chat(
                "architect",
                f"Summarize these {len(improvements)} code reviews and prioritize top 3 actions:\n{json.dumps([i['analysis'][:200] for i in improvements])}"
            )
        else:
            summary = "No improvements found"
        
        return {
            "status": "success",
            "improvements": improvements,
            "summary": summary,
            "count": len(improvements)
        }
    
    def _parse_suggestions(self, response: str) -> List[Dict[str, str]]:
        """Parse suggestion response"""
        suggestions = []
        blocks = response.split("---")
        
        for block in blocks:
            if "TITLE:" in block:
                suggestion = {}
                for line in block.split("\n"):
                    if line.startswith("TITLE:"):
                        suggestion["title"] = line.replace("TITLE:", "").strip()
                    elif line.startswith("DESCRIPTION:"):
                        suggestion["description"] = line.replace("DESCRIPTION:", "").strip()
                    elif line.startswith("PRIORITY:"):
                        suggestion["priority"] = line.replace("PRIORITY:", "").strip()
                    elif line.startswith("IMPLEMENTATION:"):
                        suggestion["implementation"] = line.replace("IMPLEMENTATION:", "").strip()
                
                if suggestion:
                    suggestions.append(suggestion)
        
        return suggestions
    
    def _extract_code(self, messages: List[Dict]) -> str:
        """Extract code from messages"""
        code_blocks = []
        for msg in messages:
            content = msg.get("content", "")
            if "```" in content:
                blocks = content.split("```")
                for i, block in enumerate(blocks):
                    if i % 2 == 1:
                        code_blocks.append(block.strip())
        
        return "\n\n".join(code_blocks)
