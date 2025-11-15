# AI Contribution: Copilot generated resource CRUD controller with image upload
# Reviewed and enhanced by team for security and validation

"""
Resource Controller
Handles resource CRUD operations and detail views.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import json
import bleach

from src.data_access import ResourceDAL, ReviewDAL
from src.models.models import db

resource_bp = Blueprint('resource', __name__, url_prefix='/resources')


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@resource_bp.route('/')
def list_resources():
    """List all published resources with filtering."""
    from datetime import datetime
    
    category = request.args.get('category', '')
    location = request.args.get('location', '')
    sort_by = request.args.get('sort', 'recent')
    min_capacity = request.args.get('capacity', type=int)
    keyword = request.args.get('q', '')
    
    # Parse availability dates
    start_date = request.args.get('start_date', '')
    start_time = request.args.get('start_time', '')
    end_date = request.args.get('end_date', '')
    end_time = request.args.get('end_time', '')
    
    start_datetime = None
    end_datetime = None
    
    # Parse datetime if provided
    if start_date and start_time:
        try:
            start_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            pass
    
    if end_date and end_time:
        try:
            end_datetime = datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            pass
    
    resources = ResourceDAL.search_resources(
        keyword=keyword if keyword else None,
        category=category if category else None,
        location=location if location else None,
        min_capacity=min_capacity,
        sort_by=sort_by,
        start_datetime=start_datetime,
        end_datetime=end_datetime
    )
    
    categories = ResourceDAL.get_categories()
    
    return render_template('resources/list.html',
                         resources=resources,
                         categories=categories,
                         selected_category=category,
                         location=location,
                         sort_by=sort_by,
                         capacity=min_capacity,
                         keyword=keyword,
                         start_date=start_date,
                         start_time=start_time,
                         end_date=end_date,
                         end_time=end_time)


@resource_bp.route('/<int:resource_id>')
def detail(resource_id):
    """Resource detail page with reviews and availability."""
    resource = ResourceDAL.get_resource_by_id(resource_id)
    
    if not resource or resource.status != 'published':
        flash('Resource not found.', 'danger')
        return redirect(url_for('resource.list_resources'))
    
    # Parse JSON fields
    images = ResourceDAL.parse_json_field(resource, 'images')
    equipment = ResourceDAL.parse_json_field(resource, 'equipment_list')
    availability = ResourceDAL.parse_json_field(resource, 'availability_rules')
    
    # Get reviews
    reviews = ReviewDAL.get_reviews_for_resource(resource_id)
    avg_rating = ReviewDAL.get_average_rating(resource_id)
    rating_dist = ReviewDAL.get_rating_distribution(resource_id)
    
    # Check if current user can review
    can_review = False
    if current_user.is_authenticated:
        can_review = ReviewDAL.can_user_review(current_user.user_id, resource_id)
    
    return render_template('resources/detail.html',
                         resource=resource,
                         images=images,
                         equipment=equipment,
                         availability=availability,
                         reviews=reviews,
                         avg_rating=avg_rating,
                         rating_dist=rating_dist,
                         can_review=can_review)


@resource_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create new resource."""
    if request.method == 'POST':
        # Get and sanitize form data
        title = bleach.clean(request.form.get('title', '').strip())
        description = bleach.clean(request.form.get('description', '').strip())
        category = request.form.get('category', '')
        location = bleach.clean(request.form.get('location', '').strip())
        capacity = request.form.get('capacity', type=int)
        requires_approval = request.form.get('requires_approval') == 'on'
        status = 'published' if request.form.get('publish') == 'yes' else 'draft'
        
        # Validation
        errors = []
        
        if not title or len(title) < 3:
            errors.append('Title must be at least 3 characters long.')
        
        if not category:
            errors.append('Please select a category.')
        
        if capacity and capacity < 1:
            errors.append('Capacity must be at least 1.')
        
        # Handle file uploads
        uploaded_images = []
        if 'images' in request.files:
            files = request.files.getlist('images')
            for file in files:
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    # Add timestamp to avoid conflicts
                    from datetime import datetime
                    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                    filename = f"{timestamp}_{filename}"
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    uploaded_images.append(f"uploads/{filename}")
        
        # Parse equipment list
        equipment_str = request.form.get('equipment', '')
        equipment_list = [e.strip() for e in equipment_str.split(',') if e.strip()]
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('resources/create.html')
        
        # Create resource
        resource = ResourceDAL.create_resource(
            owner_id=current_user.user_id,
            title=title,
            description=description,
            category=category,
            location=location,
            capacity=capacity,
            images=uploaded_images if uploaded_images else None,
            requires_approval=requires_approval,
            equipment_list=equipment_list if equipment_list else None,
            status=status
        )
        
        if resource:
            flash('Resource created successfully!', 'success')
            return redirect(url_for('resource.detail', resource_id=resource.resource_id))
        else:
            flash('Failed to create resource.', 'danger')
    
    categories = ['study-room', 'equipment', 'lab', 'event-space', 'tutoring', 'other']
    return render_template('resources/create.html', categories=categories)


@resource_bp.route('/<int:resource_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(resource_id):
    """Edit existing resource."""
    resource = ResourceDAL.get_resource_by_id(resource_id)
    
    if not resource:
        flash('Resource not found.', 'danger')
        return redirect(url_for('resource.list_resources'))
    
    # Check ownership or admin privileges
    if resource.owner_id != current_user.user_id and not current_user.is_admin():
        flash('You do not have permission to edit this resource.', 'danger')
        return redirect(url_for('resource.detail', resource_id=resource_id))
    
    if request.method == 'POST':
        # Get and sanitize form data
        title = bleach.clean(request.form.get('title', '').strip())
        description = bleach.clean(request.form.get('description', '').strip())
        category = request.form.get('category', '')
        location = bleach.clean(request.form.get('location', '').strip())
        capacity = request.form.get('capacity', type=int)
        requires_approval = request.form.get('requires_approval') == 'on'
        status = request.form.get('status', resource.status)
        
        # Validation
        if not title or len(title) < 3:
            flash('Title must be at least 3 characters long.', 'danger')
            return render_template('resources/edit.html', resource=resource)
        
        # Update resource
        updated = ResourceDAL.update_resource(
            resource_id,
            title=title,
            description=description,
            category=category,
            location=location,
            capacity=capacity,
            requires_approval=requires_approval,
            status=status
        )
        
        if updated:
            flash('Resource updated successfully!', 'success')
            return redirect(url_for('resource.detail', resource_id=resource_id))
        else:
            flash('Failed to update resource.', 'danger')
    
    # Parse JSON fields for display
    images = ResourceDAL.parse_json_field(resource, 'images')
    equipment = ResourceDAL.parse_json_field(resource, 'equipment_list')
    
    categories = ['study-room', 'equipment', 'lab', 'event-space', 'tutoring', 'other']
    return render_template('resources/edit.html', 
                         resource=resource,
                         images=images,
                         equipment=equipment,
                         categories=categories)


@resource_bp.route('/<int:resource_id>/delete', methods=['POST'])
@login_required
def delete(resource_id):
    """Delete a resource."""
    resource = ResourceDAL.get_resource_by_id(resource_id)
    
    if not resource:
        flash('Resource not found.', 'danger')
        return redirect(url_for('resource.list_resources'))
    
    # Check ownership or admin privileges
    if resource.owner_id != current_user.user_id and not current_user.is_admin():
        flash('You do not have permission to delete this resource.', 'danger')
        return redirect(url_for('resource.detail', resource_id=resource_id))
    
    if ResourceDAL.delete_resource(resource_id):
        flash('Resource deleted successfully.', 'info')
        return redirect(url_for('main.dashboard'))
    else:
        flash('Failed to delete resource.', 'danger')
        return redirect(url_for('resource.detail', resource_id=resource_id))


@resource_bp.route('/my-resources')
@login_required
def my_resources():
    """List current user's resources."""
    resources = ResourceDAL.get_resources_by_owner(current_user.user_id)
    return render_template('resources/my_resources.html', resources=resources)
