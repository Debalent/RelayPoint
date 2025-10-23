"""
Elite WebSocket Manager for Real-Time Collaboration

This module provides enterprise-grade WebSocket management for RelayPoint's
real-time collaboration features, supporting workflow updates, team notifications,
live editing, and system-wide broadcasting.
"""

import asyncio
import json
import logging
import time
from typing import Dict, List, Set, Optional, Any, Callable
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class MessageType(str, Enum):
    """WebSocket message types for different real-time events."""
    
    # Workflow Events
    WORKFLOW_STARTED = "workflow_started"
    WORKFLOW_COMPLETED = "workflow_completed"
    WORKFLOW_FAILED = "workflow_failed"
    WORKFLOW_STEP_UPDATE = "workflow_step_update"
    
    # Collaboration Events
    USER_JOINED = "user_joined"
    USER_LEFT = "user_left"
    USER_TYPING = "user_typing"
    CURSOR_MOVE = "cursor_move"
    LIVE_EDIT = "live_edit"
    
    # Notification Events
    NOTIFICATION = "notification"
    SYSTEM_ALERT = "system_alert"
    TEAM_UPDATE = "team_update"
    
    # Analytics Events
    METRICS_UPDATE = "metrics_update"
    DASHBOARD_UPDATE = "dashboard_update"
    
    # System Events
    HEARTBEAT = "heartbeat"
    RECONNECT = "reconnect"
    ERROR = "error"


@dataclass
class WebSocketMessage:
    """Structured WebSocket message."""
    
    type: MessageType
    data: Dict[str, Any]
    timestamp: datetime
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    room_id: Optional[str] = None
    
    def to_json(self) -> str:
        """Convert message to JSON string."""
        return json.dumps({
            "type": self.type.value,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
            "user_id": self.user_id,
            "session_id": self.session_id,
            "room_id": self.room_id
        })


@dataclass
class ConnectionInfo:
    """Information about a WebSocket connection."""
    
    websocket: WebSocket
    user_id: str
    session_id: str
    rooms: Set[str]
    connected_at: datetime
    last_activity: datetime
    metadata: Dict[str, Any]


class EliteWebSocketManager:
    """
    Enterprise-grade WebSocket manager for real-time collaboration.
    
    Features:
    - Room-based messaging for team collaboration
    - Automatic connection cleanup and heartbeat monitoring
    - Message broadcasting with filtering
    - Rate limiting and security controls
    - Analytics and monitoring integration
    """
    
    def __init__(self):
        # Active connections indexed by connection ID
        self.connections: Dict[str, ConnectionInfo] = {}
        
        # Room memberships for efficient broadcasting
        self.rooms: Dict[str, Set[str]] = {}
        
        # User to connections mapping (users can have multiple connections)
        self.user_connections: Dict[str, Set[str]] = {}
        
        # Message handlers for different types
        self.message_handlers: Dict[MessageType, List[Callable]] = {}
        
        # Rate limiting
        self.rate_limits: Dict[str, List[float]] = {}
        
        # Statistics
        self.stats = {
            "total_connections": 0,
            "active_connections": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "rooms_created": 0
        }
        
        # Start background tasks
        asyncio.create_task(self._heartbeat_monitor())
        asyncio.create_task(self._cleanup_disconnected())
    
    async def connect(self, 
                     websocket: WebSocket, 
                     user_id: str, 
                     metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Accept a new WebSocket connection.
        
        Args:
            websocket: FastAPI WebSocket instance
            user_id: ID of the connecting user
            metadata: Additional connection metadata
            
        Returns:
            Connection ID for this session
        """
        await websocket.accept()
        
        connection_id = str(uuid.uuid4())
        session_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        connection_info = ConnectionInfo(
            websocket=websocket,
            user_id=user_id,
            session_id=session_id,
            rooms=set(),
            connected_at=now,
            last_activity=now,
            metadata=metadata or {}
        )
        
        # Store connection
        self.connections[connection_id] = connection_info
        
        # Update user connections
        if user_id not in self.user_connections:
            self.user_connections[user_id] = set()
        self.user_connections[user_id].add(connection_id)
        
        # Update statistics
        self.stats["total_connections"] += 1
        self.stats["active_connections"] = len(self.connections)
        
        logger.info(f"User {user_id} connected with session {session_id}")
        
        # Send welcome message
        await self.send_to_connection(connection_id, WebSocketMessage(
            type=MessageType.USER_JOINED,
            data={"user_id": user_id, "session_id": session_id},
            timestamp=now,
            user_id=user_id,
            session_id=session_id
        ))
        
        return connection_id
    
    async def disconnect(self, connection_id: str):
        """
        Disconnect a WebSocket connection.
        
        Args:
            connection_id: ID of the connection to disconnect
        """
        if connection_id not in self.connections:
            return
        
        connection_info = self.connections[connection_id]
        user_id = connection_info.user_id
        
        # Leave all rooms
        for room_id in list(connection_info.rooms):
            await self.leave_room(connection_id, room_id)
        
        # Remove from user connections
        if user_id in self.user_connections:
            self.user_connections[user_id].discard(connection_id)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]
        
        # Remove connection
        del self.connections[connection_id]
        
        # Update statistics
        self.stats["active_connections"] = len(self.connections)
        
        logger.info(f"User {user_id} disconnected")
    
    async def join_room(self, connection_id: str, room_id: str):
        """
        Add a connection to a room for group messaging.
        
        Args:
            connection_id: ID of the connection
            room_id: ID of the room to join
        """
        if connection_id not in self.connections:
            return
        
        connection_info = self.connections[connection_id]
        
        # Add to room
        if room_id not in self.rooms:
            self.rooms[room_id] = set()
            self.stats["rooms_created"] += 1
        
        self.rooms[room_id].add(connection_id)
        connection_info.rooms.add(room_id)
        
        # Notify room of new member
        await self.broadcast_to_room(room_id, WebSocketMessage(
            type=MessageType.USER_JOINED,
            data={"user_id": connection_info.user_id, "room_id": room_id},
            timestamp=datetime.utcnow(),
            user_id=connection_info.user_id,
            session_id=connection_info.session_id,
            room_id=room_id
        ), exclude_connections={connection_id})
        
        logger.info(f"User {connection_info.user_id} joined room {room_id}")
    
    async def leave_room(self, connection_id: str, room_id: str):
        """
        Remove a connection from a room.
        
        Args:
            connection_id: ID of the connection
            room_id: ID of the room to leave
        """
        if connection_id not in self.connections:
            return
        
        connection_info = self.connections[connection_id]
        
        # Remove from room
        if room_id in self.rooms:
            self.rooms[room_id].discard(connection_id)
            if not self.rooms[room_id]:
                del self.rooms[room_id]
        
        connection_info.rooms.discard(room_id)
        
        # Notify room of member leaving
        await self.broadcast_to_room(room_id, WebSocketMessage(
            type=MessageType.USER_LEFT,
            data={"user_id": connection_info.user_id, "room_id": room_id},
            timestamp=datetime.utcnow(),
            user_id=connection_info.user_id,
            session_id=connection_info.session_id,
            room_id=room_id
        ))
        
        logger.info(f"User {connection_info.user_id} left room {room_id}")
    
    async def send_to_connection(self, connection_id: str, message: WebSocketMessage):
        """
        Send a message to a specific connection.
        
        Args:
            connection_id: ID of the target connection
            message: Message to send
        """
        if connection_id not in self.connections:
            return
        
        connection_info = self.connections[connection_id]
        
        try:
            await connection_info.websocket.send_text(message.to_json())
            connection_info.last_activity = datetime.utcnow()
            self.stats["messages_sent"] += 1
        except Exception as e:
            logger.error(f"Failed to send message to {connection_id}: {e}")
            await self.disconnect(connection_id)
    
    async def send_to_user(self, user_id: str, message: WebSocketMessage):
        """
        Send a message to all connections of a specific user.
        
        Args:
            user_id: ID of the target user
            message: Message to send
        """
        if user_id not in self.user_connections:
            return
        
        connection_ids = list(self.user_connections[user_id])
        for connection_id in connection_ids:
            await self.send_to_connection(connection_id, message)
    
    async def broadcast_to_room(self, 
                               room_id: str, 
                               message: WebSocketMessage,
                               exclude_connections: Optional[Set[str]] = None):
        """
        Broadcast a message to all connections in a room.
        
        Args:
            room_id: ID of the target room
            message: Message to broadcast
            exclude_connections: Set of connection IDs to exclude
        """
        if room_id not in self.rooms:
            return
        
        exclude_connections = exclude_connections or set()
        connection_ids = self.rooms[room_id] - exclude_connections
        
        for connection_id in list(connection_ids):
            await self.send_to_connection(connection_id, message)
    
    async def broadcast_to_all(self, message: WebSocketMessage):
        """
        Broadcast a message to all active connections.
        
        Args:
            message: Message to broadcast
        """
        connection_ids = list(self.connections.keys())
        for connection_id in connection_ids:
            await self.send_to_connection(connection_id, message)
    
    async def handle_message(self, connection_id: str, raw_message: str):
        """
        Handle incoming WebSocket message.
        
        Args:
            connection_id: ID of the sending connection
            raw_message: Raw message string
        """
        if connection_id not in self.connections:
            return
        
        connection_info = self.connections[connection_id]
        
        # Rate limiting check
        if not self._check_rate_limit(connection_id):
            await self.send_to_connection(connection_id, WebSocketMessage(
                type=MessageType.ERROR,
                data={"error": "Rate limit exceeded"},
                timestamp=datetime.utcnow()
            ))
            return
        
        try:
            message_data = json.loads(raw_message)
            message_type = MessageType(message_data.get("type"))
            
            # Update activity
            connection_info.last_activity = datetime.utcnow()
            self.stats["messages_received"] += 1
            
            # Execute registered handlers
            if message_type in self.message_handlers:
                for handler in self.message_handlers[message_type]:
                    await handler(connection_id, message_data)
            
        except Exception as e:
            logger.error(f"Error handling message from {connection_id}: {e}")
            await self.send_to_connection(connection_id, WebSocketMessage(
                type=MessageType.ERROR,
                data={"error": "Invalid message format"},
                timestamp=datetime.utcnow()
            ))
    
    def register_handler(self, message_type: MessageType, handler: Callable):
        """
        Register a handler for a specific message type.
        
        Args:
            message_type: Type of message to handle
            handler: Async function to handle the message
        """
        if message_type not in self.message_handlers:
            self.message_handlers[message_type] = []
        self.message_handlers[message_type].append(handler)
    
    def _check_rate_limit(self, connection_id: str, 
                         max_messages: int = 60, 
                         window_seconds: int = 60) -> bool:
        """
        Check if a connection is within rate limits.
        
        Args:
            connection_id: ID of the connection to check
            max_messages: Maximum messages per window
            window_seconds: Time window in seconds
            
        Returns:
            True if within limits, False otherwise
        """
        now = time.time()
        
        if connection_id not in self.rate_limits:
            self.rate_limits[connection_id] = []
        
        # Clean old entries
        cutoff = now - window_seconds
        self.rate_limits[connection_id] = [
            timestamp for timestamp in self.rate_limits[connection_id]
            if timestamp > cutoff
        ]
        
        # Check limit
        if len(self.rate_limits[connection_id]) >= max_messages:
            return False
        
        # Add current request
        self.rate_limits[connection_id].append(now)
        return True
    
    async def _heartbeat_monitor(self):
        """Background task to monitor connection health."""
        while True:
            try:
                await asyncio.sleep(30)  # Check every 30 seconds
                
                now = datetime.utcnow()
                stale_connections = []
                
                for connection_id, connection_info in self.connections.items():
                    # Check for stale connections (no activity for 5 minutes)
                    if (now - connection_info.last_activity).total_seconds() > 300:
                        stale_connections.append(connection_id)
                    else:
                        # Send heartbeat
                        await self.send_to_connection(connection_id, WebSocketMessage(
                            type=MessageType.HEARTBEAT,
                            data={"timestamp": now.isoformat()},
                            timestamp=now
                        ))
                
                # Disconnect stale connections
                for connection_id in stale_connections:
                    await self.disconnect(connection_id)
                    
            except Exception as e:
                logger.error(f"Error in heartbeat monitor: {e}")
    
    async def _cleanup_disconnected(self):
        """Background task to clean up disconnected connections."""
        while True:
            try:
                await asyncio.sleep(60)  # Clean up every minute
                
                # Clean up rate limiting data
                cutoff = time.time() - 3600  # Keep 1 hour of data
                for connection_id in list(self.rate_limits.keys()):
                    if connection_id not in self.connections:
                        del self.rate_limits[connection_id]
                    else:
                        self.rate_limits[connection_id] = [
                            timestamp for timestamp in self.rate_limits[connection_id]
                            if timestamp > cutoff
                        ]
                
            except Exception as e:
                logger.error(f"Error in cleanup task: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current WebSocket manager statistics."""
        return {
            **self.stats,
            "active_rooms": len(self.rooms),
            "active_users": len(self.user_connections)
        }
    
    def get_room_info(self, room_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific room."""
        if room_id not in self.rooms:
            return None
        
        connection_ids = self.rooms[room_id]
        users = set()
        
        for connection_id in connection_ids:
            if connection_id in self.connections:
                users.add(self.connections[connection_id].user_id)
        
        return {
            "room_id": room_id,
            "connection_count": len(connection_ids),
            "user_count": len(users),
            "users": list(users)
        }


# Global WebSocket manager instance
websocket_manager = EliteWebSocketManager()