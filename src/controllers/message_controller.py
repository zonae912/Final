# AI Contribution: Copilot generated messaging controller
# Reviewed and approved by team

"""
Message Controller
Handles user messaging and conversations.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
import bleach

from src.data_access import MessageDAL, UserDAL

message_bp = Blueprint('message', __name__, url_prefix='/messages')


@message_bp.route('/')
@login_required
def inbox():
    """View all message threads."""
    threads = MessageDAL.get_user_threads(current_user.user_id)
    return render_template('messages/inbox.html', threads=threads)


@message_bp.route('/thread/<int:thread_id>')
@login_required
def thread(thread_id):
    """View a specific message thread."""
    messages = MessageDAL.get_thread_messages(thread_id)
    
    if not messages:
        flash('Thread not found.', 'danger')
        return redirect(url_for('message.inbox'))
    
    # Check access permission
    first_msg = messages[0]
    if first_msg.sender_id != current_user.user_id and \
       first_msg.receiver_id != current_user.user_id:
        flash('You do not have permission to view this thread.', 'danger')
        return redirect(url_for('message.inbox'))
    
    # Mark messages as read
    MessageDAL.mark_thread_as_read(thread_id, current_user.user_id)
    
    # Get other user
    other_user_id = first_msg.sender_id if first_msg.sender_id != current_user.user_id else first_msg.receiver_id
    other_user = UserDAL.get_user_by_id(other_user_id)
    
    return render_template('messages/thread.html', 
                         thread=messages,
                         messages=messages,
                         other_user=other_user,
                         thread_id=thread_id)


@message_bp.route('/compose', methods=['GET', 'POST'])
@login_required
def compose():
    """Compose a new message to any user."""
    if request.method == 'POST':
        receiver_id = request.form.get('receiver_id', type=int)
        subject = bleach.clean(request.form.get('subject', '').strip())
        content = bleach.clean(request.form.get('body', '').strip())
        
        if not receiver_id:
            flash('Please select a recipient.', 'danger')
            users = UserDAL.get_all_users()
            return render_template('messages/send.html', users=users)
        
        if not content:
            flash('Message cannot be empty.', 'danger')
            users = UserDAL.get_all_users()
            return render_template('messages/send.html', users=users, selected_receiver_id=receiver_id)
        
        receiver = UserDAL.get_user_by_id(receiver_id)
        if not receiver:
            flash('User not found.', 'danger')
            return redirect(url_for('message.inbox'))
        
        message = MessageDAL.create_message(
            sender_id=current_user.user_id,
            receiver_id=receiver_id,
            content=content
        )
        
        if message:
            flash('Message sent successfully!', 'success')
            return redirect(url_for('message.thread', thread_id=message.thread_id))
        else:
            flash('Failed to send message.', 'danger')
    
    # GET request - show compose form with user list
    users = UserDAL.get_all_users()
    if users:
        users = [u for u in users if u.user_id != current_user.user_id]  # Exclude self
    else:
        users = []
    return render_template('messages/send.html', users=users)


@message_bp.route('/send/<int:receiver_id>', methods=['GET', 'POST'])
@login_required
def send(receiver_id):
    """Send a new message to a user."""
    receiver = UserDAL.get_user_by_id(receiver_id)
    
    if not receiver:
        flash('User not found.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        subject = bleach.clean(request.form.get('subject', '').strip())
        content = bleach.clean(request.form.get('body', '').strip())
        
        if not content:
            flash('Message cannot be empty.', 'danger')
            return render_template('messages/send.html', receiver=receiver)
        
        message = MessageDAL.create_message(
            sender_id=current_user.user_id,
            receiver_id=receiver_id,
            content=content
        )
        
        if message:
            flash('Message sent successfully!', 'success')
            return redirect(url_for('message.thread', thread_id=message.thread_id))
        else:
            flash('Failed to send message.', 'danger')
    
    return render_template('messages/send.html', receiver=receiver)


@message_bp.route('/reply/<int:thread_id>', methods=['POST'])
@login_required
def reply(thread_id):
    """Reply to a message thread."""
    content = bleach.clean(request.form.get('body', '').strip())
    
    if not content:
        flash('Message cannot be empty.', 'danger')
        return redirect(url_for('message.thread', thread_id=thread_id))
    
    # Get thread to determine receiver
    thread_messages = MessageDAL.get_thread_messages(thread_id)
    if not thread_messages:
        flash('Thread not found.', 'danger')
        return redirect(url_for('message.inbox'))
    
    # Determine receiver (the other person in the conversation)
    first_msg = thread_messages[0]
    receiver_id = first_msg.sender_id if first_msg.sender_id != current_user.user_id else first_msg.receiver_id
    
    message = MessageDAL.create_message(
        sender_id=current_user.user_id,
        receiver_id=receiver_id,
        content=content,
        thread_id=thread_id
    )
    
    if message:
        flash('Reply sent successfully!', 'success')
    else:
        flash('Failed to send reply.', 'danger')
    
    return redirect(url_for('message.thread', thread_id=thread_id))
