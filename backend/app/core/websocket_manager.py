# backend/app/core/websocket_manager.py

from fastapi import WebSocket
from typing import Dict, List
import json
import structlog

logger = structlog.get_logger()

class WebSocketManager:
    """
    Manages WebSocket connections for real-time features in RelayPoint.
    
    Supports:
    - Real-time workflow execution updates
    - Collaborative editing notifications
    - System alerts and notifications
    - Live dashboard updates
    """
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_sessions: Dict[str, List[str]] = {}  # user_id -> [client_ids]
        
    async def connect(self, websocket: WebSocket, client_id: str):
        """Connect a new WebSocket client"""
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info("WebSocket client connected", client_id=client_id)
        
    def disconnect(self, client_id: str):
        """Disconnect a WebSocket client"""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            logger.info("WebSocket client disconnected", client_id=client_id)
            
    async def send_personal_message(self, message: str, client_id: str):
        """Send a message to a specific client"""
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            await websocket.send_text(message)
            
    async def send_json_message(self, data: dict, client_id: str):
        """Send JSON data to a specific client"""
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            await websocket.send_json(data)
            
    async def broadcast_message(self, message: str):
        """Broadcast a message to all connected clients"""
        for client_id, websocket in self.active_connections.items():
            try:
                await websocket.send_text(message)
            except Exception as e:
                logger.error("Failed to send broadcast message", 
                           client_id=client_id, error=str(e))
                
    async def broadcast_json(self, data: dict):
        """Broadcast JSON data to all connected clients"""
        for client_id, websocket in self.active_connections.items():
            try:
                await websocket.send_json(data)
            except Exception as e:
                logger.error("Failed to send broadcast JSON", 
                           client_id=client_id, error=str(e))
                
    async def send_to_user(self, user_id: str, data: dict):
        """Send data to all sessions of a specific user"""
        if user_id in self.user_sessions:
            for client_id in self.user_sessions[user_id]:
                await self.send_json_message(data, client_id)
                
    async def notify_workflow_update(self, workflow_id: str, update_type: str, data: dict):
        """Send workflow update notifications to subscribed clients"""
        notification = {
            "type": "workflow_update",
            "workflow_id": workflow_id,
            "update_type": update_type,
            "data": data,
            "timestamp": "2025-10-22T00:00:00Z"
        }
        await self.broadcast_json(notification)
        
    async def notify_collaboration_event(self, project_id: str, user_id: str, event: str):
        """Send collaboration event notifications"""
        notification = {
            "type": "collaboration",
            "project_id": project_id,
            "user_id": user_id,
            "event": event,
            "timestamp": "2025-10-22T00:00:00Z"
        }
        await self.broadcast_json(notification)

# Global WebSocket manager instance
websocket_manager = WebSocketManager()