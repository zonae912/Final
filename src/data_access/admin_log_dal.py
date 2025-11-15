# AI Contribution: Copilot generated admin log DAL for audit trail
# Reviewed and approved by team

"""
Data Access Layer for Admin Logs
Encapsulates all database operations for the AdminLog model.
"""

from src.models.models import db, AdminLog
from datetime import datetime, timedelta
import json


class AdminLogDAL:
    """Data Access Layer for Admin Log operations."""
    
    @staticmethod
    def create_log(admin_id, action, target_table=None, target_id=None, details=None):
        """
        Create a new admin log entry.
        
        Args:
            admin_id (int): Admin user ID
            action (str): Action performed (e.g., 'user_suspend', 'review_hide')
            target_table (str): Target database table
            target_id (int): Target record ID
            details (dict): Additional details as dictionary
            
        Returns:
            AdminLog: Created log object
        """
        log = AdminLog(
            admin_id=admin_id,
            action=action,
            target_table=target_table,
            target_id=target_id,
            details=json.dumps(details) if details else None
        )
        
        try:
            db.session.add(log)
            db.session.commit()
            return log
        except Exception:
            db.session.rollback()
            return None
    
    @staticmethod
    def get_log_by_id(log_id):
        """Get admin log by ID."""
        return AdminLog.query.get(log_id)
    
    @staticmethod
    def get_logs_by_admin(admin_id, limit=100):
        """
        Get logs for a specific admin.
        
        Args:
            admin_id (int): Admin user ID
            limit (int): Maximum number of logs to return
            
        Returns:
            list: List of AdminLog objects
        """
        return AdminLog.query.filter_by(admin_id=admin_id)\
            .order_by(AdminLog.timestamp.desc())\
            .limit(limit).all()
    
    @staticmethod
    def get_recent_logs(limit=100):
        """
        Get recent admin logs.
        
        Args:
            limit (int): Maximum number of logs to return
            
        Returns:
            list: List of AdminLog objects
        """
        return AdminLog.query.order_by(AdminLog.timestamp.desc())\
            .limit(limit).all()
    
    @staticmethod
    def get_logs_by_action(action, limit=100):
        """
        Get logs filtered by action type.
        
        Args:
            action (str): Action type to filter
            limit (int): Maximum number of logs to return
            
        Returns:
            list: List of AdminLog objects
        """
        return AdminLog.query.filter_by(action=action)\
            .order_by(AdminLog.timestamp.desc())\
            .limit(limit).all()
    
    @staticmethod
    def get_logs_for_target(target_table, target_id):
        """
        Get all logs for a specific target record.
        
        Args:
            target_table (str): Target table name
            target_id (int): Target record ID
            
        Returns:
            list: List of AdminLog objects
        """
        return AdminLog.query.filter_by(
            target_table=target_table,
            target_id=target_id
        ).order_by(AdminLog.timestamp.desc()).all()
    
    @staticmethod
    def get_logs_in_date_range(start_date, end_date):
        """
        Get logs within a date range.
        
        Args:
            start_date (datetime): Start date
            end_date (datetime): End date
            
        Returns:
            list: List of AdminLog objects
        """
        return AdminLog.query.filter(
            AdminLog.timestamp >= start_date,
            AdminLog.timestamp <= end_date
        ).order_by(AdminLog.timestamp.desc()).all()
    
    @staticmethod
    def get_action_statistics(days=30):
        """
        Get statistics on admin actions over a period.
        
        Args:
            days (int): Number of days to look back
            
        Returns:
            dict: Statistics like {'user_suspend': 5, 'review_hide': 12}
        """
        start_date = datetime.utcnow() - timedelta(days=days)
        
        logs = AdminLog.query.filter(AdminLog.timestamp >= start_date).all()
        
        stats = {}
        for log in logs:
            stats[log.action] = stats.get(log.action, 0) + 1
        
        return stats
    
    @staticmethod
    def parse_details(log):
        """
        Parse JSON details from an admin log.
        
        Args:
            log (AdminLog): Admin log object
            
        Returns:
            dict: Parsed details or empty dict
        """
        if not log.details:
            return {}
        try:
            return json.loads(log.details)
        except:
            return {}
    
    @staticmethod
    def delete_old_logs(days=365):
        """
        Delete logs older than specified days.
        
        Args:
            days (int): Delete logs older than this many days
            
        Returns:
            int: Number of logs deleted
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        count = AdminLog.query.filter(AdminLog.timestamp < cutoff_date).delete()
        
        try:
            db.session.commit()
            return count
        except Exception:
            db.session.rollback()
            return 0
