# Classroom Images

Please save the provided classroom images to this directory with the following filenames:

## Specific Room Images:
- **cg_0001.jpg** - Standard classroom with whiteboards and desks (Image 1)
- **cg_0030_lab.jpg** - Computer lab with workstations (Image 2)
- **cg_1004.jpg** - Collaborative classroom with movable tables (Image 3)
- **cg_1014_lecture.jpg** - Lecture hall with fixed seating (Image 5 or 6)
- **cg_1022_lecture.jpg** - Another lecture hall view (Image 7 or 8)

## Generic Images (used for multiple rooms):
- **classroom.jpg** - Standard classroom (use Image 1 or 7)
- **lecture_hall.jpg** - Tiered lecture hall (use Image 11-16 - amphitheater style)
- **computer_lab.jpg** - Computer/teaching lab (use Image 2)

## Image Mapping Guide:

From your 18 provided images:

1. **Image 1** (classroom with whiteboards) → `cg_0001.jpg` and `classroom.jpg`
2. **Image 2** (computer lab) → `cg_0030_lab.jpg` and `computer_lab.jpg`
3. **Image 3** (collaborative room) → `cg_1004.jpg`
4. **Image 4** (media/presentation room) → Can use for special classrooms
5-10. **Images 5-10** (various lecture halls) → Use for `cg_1014_lecture.jpg`, `cg_1022_lecture.jpg`
11-16. **Images 11-16** (tiered amphitheater halls) → `lecture_hall.jpg`
17-18. **Images 17-18** (additional classroom views) → Backup images

## Quick Setup:

To quickly populate the database with these images:

1. Save the 18 images to this directory with the names above
2. Run: `python scripts/init_database.py`
3. The resources will now display with actual classroom photos!

## Current Database Resources Using These Images:

- CG 0001 Classroom (40 seats)
- CG 0030 Teaching Lab (45 seats)
- CG 1004 Classroom (25 seats)
- CG 1014-1056 Lecture Halls (60-80 seats)
- CG 2061-2077 Lecture Halls (40-60 seats)
- CG 3044, 3059 Classrooms (35-48 seats)
- CG 3075 Teaching Lab (40 seats)
