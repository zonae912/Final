# URL Routing Fixes for Campus Resource Hub

## Issues Found and Fixed

### 1. Function Name Mismatches
- ❌ `url_for('resource.list')` → ✅ `url_for('resource.list_resources')`
- ❌ `url_for('main.help_page')` → ✅ `url_for('main.help')`

### 2. Parameter Name Mismatches

#### Booking Routes
Route definition: `@booking_bp.route('/<int:booking_id>')`
- ❌ `url_for('booking.detail', id=booking.id)` 
- ✅ `url_for('booking.detail', booking_id=booking.booking_id)`

- ❌ `url_for('booking.approve', id=booking.id)`
- ✅ `url_for('booking.approve', booking_id=booking.booking_id)`

- ❌ `url_for('booking.reject', id=booking.id)`
- ✅ `url_for('booking.reject', booking_id=booking.booking_id)`

- ❌ `url_for('booking.cancel', id=booking.id)`
- ✅ `url_for('booking.cancel', booking_id=booking.booking_id)`

#### Message Routes
Route definition: `@message_bp.route('/thread/<int:thread_id>')`
- ❌ `url_for('message.thread', message_id=message.id)`
- ✅ `url_for('message.thread', thread_id=thread_id)`

- ❌ `url_for('message.reply', message_id=thread[0].id)`
- ✅ `url_for('message.reply', thread_id=thread_id)`

### 3. Files that Need Fixing

1. **src/views/base.html** - ✅ FIXED (help_page → help)
2. **src/views/resources/list.html** - ✅ FIXED (resource.list → resource.list_resources)
3. **src/views/bookings/my_bookings.html** - NEEDS FIX (id → booking_id)
4. **src/views/bookings/detail.html** - NEEDS FIX (id → booking_id)
5. **src/views/messages/inbox.html** - NEEDS FIX (message_id → thread_id)
6. **src/views/messages/thread.html** - NEEDS FIX (message_id → thread_id)
7. **src/views/messages/send.html** - CHECK
8. **src/views/reviews/create.html** - CHECK
9. **src/views/admin/dashboard.html** - NEEDS FIX (id → booking_id)
10. **src/views/dashboard.html** - NEEDS FIX (booking_id parameter)

### Status
- ✅ 2 files fixed
- ⏳ 8 files need fixing

## Next Steps
Run comprehensive find-and-replace for all remaining parameter mismatches.
