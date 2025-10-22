"""
Performance monitoring utilities for CrewAI applications.
"""

import time
import psutil
import threading
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict

from .logging_utils import get_logger, log_performance_metrics


@dataclass
class PerformanceMetrics:
    """Performance metrics data structure."""
    
    start_time: float
    end_time: Optional[float] = None
    duration: Optional[float] = None
    cpu_usage: List[float] = field(default_factory=list)
    memory_usage: List[float] = field(default_factory=list)
    peak_memory: float = 0.0
    average_cpu: float = 0.0
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    
    def finalize(self) -> None:
        """Finalize metrics calculation."""
        if self.end_time:
            self.duration = self.end_time - self.start_time
            
        if self.cpu_usage:
            self.average_cpu = sum(self.cpu_usage) / len(self.cpu_usage)
            
        if self.memory_usage:
            self.peak_memory = max(self.memory_usage)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary."""
        return {
            "duration": self.duration,
            "average_cpu": self.average_cpu,
            "peak_memory": self.peak_memory,
            "total_tasks": self.total_tasks,
            "completed_tasks": self.completed_tasks,
            "failed_tasks": self.failed_tasks,
            "success_rate": self.completed_tasks / max(self.total_tasks, 1),
            "cpu_samples": len(self.cpu_usage),
            "memory_samples": len(self.memory_usage)
        }


class PerformanceMonitor:
    """Monitor performance of CrewAI executions."""
    
    def __init__(self, sample_interval: float = 1.0):
        """
        Initialize performance monitor.
        
        Args:
            sample_interval: Interval between performance samples in seconds
        """
        self.sample_interval = sample_interval
        self.logger = get_logger("performance_monitor")
        
        # Active monitoring sessions
        self._active_sessions: Dict[str, PerformanceMetrics] = {}
        self._monitoring_threads: Dict[str, threading.Thread] = {}
        self._stop_events: Dict[str, threading.Event] = {}
        
        # Global metrics
        self._global_metrics = defaultdict(list)
        self._session_history: Dict[str, PerformanceMetrics] = {}
        
        self.logger.info("Performance monitor initialized")
    
    def start_monitoring(self, session_id: str) -> None:
        """
        Start monitoring a session.
        
        Args:
            session_id: Unique identifier for the monitoring session
        """
        if session_id in self._active_sessions:
            self.logger.warning(f"Session {session_id} is already being monitored")
            return
        
        # Initialize metrics
        metrics = PerformanceMetrics(start_time=time.time())
        self._active_sessions[session_id] = metrics
        
        # Create stop event
        stop_event = threading.Event()
        self._stop_events[session_id] = stop_event
        
        # Start monitoring thread
        monitor_thread = threading.Thread(
            target=self._monitor_session,
            args=(session_id, metrics, stop_event),
            daemon=True
        )
        
        self._monitoring_threads[session_id] = monitor_thread
        monitor_thread.start()
        
        self.logger.info(f"Started monitoring session: {session_id}")
    
    def stop_monitoring(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Stop monitoring a session and return metrics.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Performance metrics dictionary
        """
        if session_id not in self._active_sessions:
            self.logger.warning(f"Session {session_id} is not being monitored")
            return None
        
        # Stop monitoring thread
        stop_event = self._stop_events.get(session_id)
        if stop_event:
            stop_event.set()
        
        # Wait for thread to finish
        monitor_thread = self._monitoring_threads.get(session_id)
        if monitor_thread and monitor_thread.is_alive():
            monitor_thread.join(timeout=5.0)
        
        # Finalize metrics
        metrics = self._active_sessions[session_id]
        metrics.end_time = time.time()
        metrics.finalize()
        
        # Store in history
        self._session_history[session_id] = metrics
        
        # Clean up
        self._active_sessions.pop(session_id, None)
        self._monitoring_threads.pop(session_id, None)
        self._stop_events.pop(session_id, None)
        
        # Log metrics
        metrics_dict = metrics.to_dict()
        log_performance_metrics(session_id, metrics_dict)
        
        self.logger.info(f"Stopped monitoring session: {session_id}")
        return metrics_dict
    
    def _monitor_session(
        self,
        session_id: str,
        metrics: PerformanceMetrics,
        stop_event: threading.Event
    ) -> None:
        """
        Monitor system performance for a session.
        
        Args:
            session_id: Session identifier
            metrics: Metrics object to update
            stop_event: Event to signal monitoring stop
        """
        process = psutil.Process()
        
        while not stop_event.is_set():
            try:
                # Sample CPU usage
                cpu_percent = process.cpu_percent()
                metrics.cpu_usage.append(cpu_percent)
                
                # Sample memory usage (in MB)
                memory_info = process.memory_info()
                memory_mb = memory_info.rss / 1024 / 1024
                metrics.memory_usage.append(memory_mb)
                
                # Update global metrics
                self._global_metrics[session_id].append({
                    "timestamp": time.time(),
                    "cpu": cpu_percent,
                    "memory": memory_mb
                })
                
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                self.logger.warning(f"Error sampling performance for {session_id}: {e}")
            
            # Wait for next sample
            stop_event.wait(self.sample_interval)
    
    def update_task_metrics(
        self,
        session_id: str,
        total_tasks: Optional[int] = None,
        completed_tasks: Optional[int] = None,
        failed_tasks: Optional[int] = None
    ) -> None:
        """
        Update task-related metrics for a session.
        
        Args:
            session_id: Session identifier
            total_tasks: Total number of tasks
            completed_tasks: Number of completed tasks
            failed_tasks: Number of failed tasks
        """
        if session_id not in self._active_sessions:
            return
        
        metrics = self._active_sessions[session_id]
        
        if total_tasks is not None:
            metrics.total_tasks = total_tasks
        if completed_tasks is not None:
            metrics.completed_tasks = completed_tasks
        if failed_tasks is not None:
            metrics.failed_tasks = failed_tasks
    
    def get_session_metrics(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get current metrics for an active session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Current metrics dictionary
        """
        if session_id in self._active_sessions:
            metrics = self._active_sessions[session_id]
            # Create temporary metrics for current state
            temp_metrics = PerformanceMetrics(
                start_time=metrics.start_time,
                end_time=time.time(),
                cpu_usage=metrics.cpu_usage.copy(),
                memory_usage=metrics.memory_usage.copy(),
                total_tasks=metrics.total_tasks,
                completed_tasks=metrics.completed_tasks,
                failed_tasks=metrics.failed_tasks
            )
            temp_metrics.finalize()
            return temp_metrics.to_dict()
        
        elif session_id in self._session_history:
            return self._session_history[session_id].to_dict()
        
        return None
    
    def get_global_metrics(self) -> Dict[str, Any]:
        """
        Get global performance metrics across all sessions.
        
        Returns:
            Global metrics dictionary
        """
        total_sessions = len(self._session_history) + len(self._active_sessions)
        active_sessions = len(self._active_sessions)
        
        # Calculate averages from completed sessions
        completed_durations = [
            m.duration for m in self._session_history.values()
            if m.duration is not None
        ]
        
        completed_cpu_averages = [
            m.average_cpu for m in self._session_history.values()
            if m.average_cpu > 0
        ]
        
        completed_memory_peaks = [
            m.peak_memory for m in self._session_history.values()
            if m.peak_memory > 0
        ]
        
        return {
            "total_sessions": total_sessions,
            "active_sessions": active_sessions,
            "completed_sessions": len(self._session_history),
            "average_duration": (
                sum(completed_durations) / len(completed_durations)
                if completed_durations else 0
            ),
            "average_cpu_usage": (
                sum(completed_cpu_averages) / len(completed_cpu_averages)
                if completed_cpu_averages else 0
            ),
            "average_peak_memory": (
                sum(completed_memory_peaks) / len(completed_memory_peaks)
                if completed_memory_peaks else 0
            ),
            "system_cpu_count": psutil.cpu_count(),
            "system_memory_total": psutil.virtual_memory().total / 1024 / 1024 / 1024,  # GB
        }
    
    def get_session_history(self) -> Dict[str, Dict[str, Any]]:
        """
        Get performance history for all completed sessions.
        
        Returns:
            Dictionary mapping session IDs to metrics
        """
        return {
            session_id: metrics.to_dict()
            for session_id, metrics in self._session_history.items()
        }
    
    def clear_history(self) -> None:
        """Clear performance history."""
        self._session_history.clear()
        self._global_metrics.clear()
        self.logger.info("Performance history cleared")
    
    def export_metrics(self, filepath: str, format: str = "json") -> None:
        """
        Export performance metrics to file.
        
        Args:
            filepath: Path to save metrics
            format: Export format ('json' or 'csv')
        """
        import json
        from pathlib import Path
        
        data = {
            "global_metrics": self.get_global_metrics(),
            "session_history": self.get_session_history(),
            "export_timestamp": datetime.now().isoformat()
        }
        
        filepath = Path(filepath)
        
        if format.lower() == "json":
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        elif format.lower() == "csv":
            import pandas as pd
            
            # Convert session history to DataFrame
            rows = []
            for session_id, metrics in self._session_history.items():
                row = {"session_id": session_id, **metrics.to_dict()}
                rows.append(row)
            
            df = pd.DataFrame(rows)
            df.to_csv(filepath, index=False)
        else:
            raise ValueError(f"Unsupported export format: {format}")
        
        self.logger.info(f"Metrics exported to {filepath}")
    
    def __del__(self):
        """Cleanup when monitor is destroyed."""
        # Stop all active monitoring
        for session_id in list(self._active_sessions.keys()):
            self.stop_monitoring(session_id)