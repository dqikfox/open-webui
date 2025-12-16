import logging
import asyncio
from typing import List
from datetime import datetime

log = logging.getLogger(__name__)

class AutoGenScheduler:
    """Automated scheduler for continuous improvements"""
    
    def __init__(self, autogen_studio, interval_minutes: int = 60):
        self.studio = autogen_studio
        self.interval = interval_minutes * 60
        self.running = False
        self.task = None
        self.last_run = None
        self.results = []
        
    async def start(self, scan_dirs: List[str]):
        """Start continuous improvement scheduler"""
        if self.running:
            return {"status": "already_running"}
        
        self.running = True
        self.task = asyncio.create_task(self._run_loop(scan_dirs))
        log.info(f"AutoGen scheduler started: scanning every {self.interval/60} minutes")
        
        return {"status": "started", "interval_minutes": self.interval/60}
    
    async def stop(self):
        """Stop scheduler"""
        self.running = False
        if self.task:
            self.task.cancel()
        log.info("AutoGen scheduler stopped")
        return {"status": "stopped"}
    
    async def _run_loop(self, scan_dirs: List[str]):
        """Main scheduler loop"""
        while self.running:
            try:
                log.info("Running scheduled code improvement scan...")
                result = await self.studio.continuous_improvement(scan_dirs)
                
                self.last_run = datetime.now()
                self.results.append({
                    "timestamp": self.last_run.isoformat(),
                    "improvements": result.get("count", 0),
                    "summary": result.get("summary", "")
                })
                
                # Keep only last 10 results
                if len(self.results) > 10:
                    self.results = self.results[-10:]
                
                log.info(f"Scan complete: {result.get('count', 0)} improvements found")
                
            except Exception as e:
                log.error(f"Scheduler error: {e}")
            
            await asyncio.sleep(self.interval)
    
    def get_status(self):
        """Get scheduler status"""
        return {
            "running": self.running,
            "interval_minutes": self.interval / 60,
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "total_runs": len(self.results),
            "recent_results": self.results[-5:]
        }
