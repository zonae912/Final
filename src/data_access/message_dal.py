# AI Contribution: Copilot generated message DAL for threaded conversations
# Reviewed and approved by team

"""
Data Access Layer for Messages
Encapsulates all database operations for the Message model.
"""

from src.models.models import db, Message
from datetime import datetime


class MessageDAL:
    """Data Access Layer for Message operations."""
    
    @staticmethod
    def create_message(sender_id, receiver_id, content, thread_id=None, related_booking_id=None):
        """
        Create a new message.
        
        Args:
            sender_id (int): User ID of sender
            receiver_id (int): User ID of receiver
            content (str): Message content
            thread_id (int): Optional thread ID for grouping
            related_booking_id (int): Optional related booking ID
            
        Returns:
            Message: Created message object
        """
        # Auto-generate thread_id if not provided
        if not thread_id:
            # Create thread_id based on users (consistent for same pair)
            thread_id = hash(tuple(sorted([sender_id, receiver_id]))) % 1000000
        
        message = Message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
            thread_id=thread_id,
            related_booking_id=related_booking_id
        )
        
        try:
            db.session.add(message)
            db.session.commit()
            return message
        except Exception:
            db.session.rollback()
            return None
    
    @staticmethod
    def get_message_by_id(message_id):
        """Get message by ID."""
        return Message.query.get(message_id)
    
    @staticmethod
    def get_messages_for_user(user_id):
        """
        Get all messages for a user (sent or received).
        
        Args:
            user_id (int): User ID
            
        Returns:
            list: List of Message objects
        """
        return Message.query.filter(
            (Message.sender_id == user_id) | (Message.receiver_id == user_id)
        ).order_by(Message.timestamp.desc()).all()
    
    @staticmethod
    def get_thread_messages(thread_id):
        """
        Get all messages in a thread.
        
        Args:
            thread_id (int): Thread ID
            
        Returns:
            list: List of Message objects in chronological order
        """
        return Message.query.filter_by(thread_id=thread_id)\
            .order_by(Message.timestamp).all()
    
    @staticmethod
    def get_conversation(user1_id, user2_id):
        """
        Get all messages between two users.
        
        Args:
            user1_id (int): First user ID
            user2_id (int): Second user ID
            
        Returns:
            list: List of Message objects in chronological order
        """
        return Message.query.filter(
            ((Message.sender_id == user1_id) & (Message.receiver_id == user2_id)) |
            ((Message.sender_id == user2_id) & (Message.receiver_id == user1_id))
        ).order_by(Message.timestamp).all()
    
    @staticmethod
    def get_user_threads(user_id):
        """
        Get unique conversation threads for a user.
        
        Args:
            user_id (int): User ID
            
        Returns:
            list: List of unique thread IDs with last message info
        """
        # Get all unique threads (exclude None thread_ids)
        threads = db.session.query(Message.thread_id).filter(
            (Message.sender_id == user_id) | (Message.receiver_id == user_id),
            Message.thread_id.isnot(None)
        ).distinct().all()
        
        thread_ids = [t[0] for t in threads if t[0] is not None]
        
        # Get last message for each thread
        thread_info = []
        for thread_id in thread_ids:
            last_message = Message.query.filter_by(thread_id=thread_id)\
                .order_by(Message.timestamp.desc()).first()
            if last_message:
                thread_info.append({
                    'thread_id': thread_id,
                    'last_message': last_message,
                    'unread_count': MessageDAL.get_unread_count_in_thread(thread_id, user_id)
                })
        
        return sorted(thread_info, key=lambda x: x['last_message'].timestamp, reverse=True)
    
    @staticmethod
    def mark_as_read(message_id):
        """
        Mark a message as read.
        
        Args:
            message_id (int): Message ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        message = Message.query.get(message_id)
        if not message:
            return False
        
        message.is_read = True
        
        try:
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False
    
    @staticmethod
    def mark_thread_as_read(thread_id, user_id):
        """
        Mark all messages in a thread as read for a specific user.
        
        Args:
            thread_id (int): Thread ID
            user_id (int): User ID (receiver)
            
        Returns:
            int: Number of messages marked as read
        """
        count = Message.query.filter_by(
            thread_id=thread_id,
            receiver_id=user_id,
            is_read=False
        ).update({Message.is_read: True})
        
        try:
            db.session.commit()
            return count
        except Exception:
            db.session.rollback()
            return 0
    
    @staticmethod
    def get_unread_count(user_id):
        """
        Get count of unread messages for a user.
        
        Args:
            user_id (int): User ID
            
        Returns:
            int: Count of unread messages
        """
        return Message.query.filter_by(
            receiver_id=user_id,
            is_read=False
        ).count()
    
    @staticmethod
    def get_unread_count_in_thread(thread_id, user_id):
        """
        Get count of unread messages in a specific thread for a user.
        
        Args:
            thread_id (int): Thread ID
            user_id (int): User ID (receiver)
            
        Returns:
            int: Count of unread messages
        """
        return Message.query.filter_by(
            thread_id=thread_id,
            receiver_id=user_id,
            is_read=False
        ).count()
    
    @staticmethod
    def delete_message(message_id):
        """
        Delete a message.
        
        Args:
            message_id (int): Message ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        message = Message.query.get(message_id)
        if not message:
            return False
        
        try:
            db.session.delete(message)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False
