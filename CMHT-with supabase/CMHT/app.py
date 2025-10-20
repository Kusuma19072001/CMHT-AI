from flask import Flask, request, jsonify, send_from_directory
import sqlite3
from gtts import gTTS
import base64
import io
import re
import smtplib
import os
from flask_cors import CORS
import time
from feedback_manager import feedback_manager
from config import SENDER_EMAIL, EMAIL_PASSWORD, RECEIVER_EMAIL, SILENCE_TIMEOUT_SECONDS

# Email configuration - Set these values directly for now
# TODO: Move to .env file in production
# Configuration moved to config.py
ENDING_PHRASES = [
    'thank you', 'thanks', 'thank you so much', 'thanks a lot',
    'okay', 'ok', 'alright', 'all right', 'sure', 'yeah', 'yes',
    'goodbye', 'bye', 'see you', 'see ya', 'take care', 'have a good day',
    'that\'s all', 'that is all', 'that\'s it', 'that is it',
    'i\'m done', 'i am done', 'i\'m finished', 'i am finished',
    'finished', 'done', 'complete', 'got it', 'understood',
    'no more questions', 'no more', 'nothing else', 'that\'s everything'
]

print("✅ Email configuration loaded")
print("⚠️ NOTE: Credentials are hardcoded - move to .env file for production!")
print(f"✅ Auto-end interaction configured: {SILENCE_TIMEOUT_SECONDS}s silence timeout")
print(f"✅ Ending phrases detected: {len(ENDING_PHRASES)} phrases configured")

app = Flask(__name__)
CORS(app)

def init_database():
    """Initialize the database with faculty data and room directions"""
    conn = sqlite3.connect("college.db")
    c = conn.cursor()
    
    # Create faculty table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS faculty (
            name TEXT,
            room TEXT,
            building TEXT,
            email TEXT
        )
    ''')
    
    # Create room directions table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS room_directions (
            room TEXT,
            direction TEXT
        )
    ''')
    
    # Check if faculty data already exists
    c.execute("SELECT COUNT(*) FROM faculty")
    if c.fetchone()[0] == 0:
        # Insert faculty data with emails
        faculty_data = [
            ("Dr. Sanjukta Pookulangara", "342 J", "MDR Building", "Sanjukta.Pookulangara@unt.edu"),
            ("Dr. Lynn Brandon", "342 E", "MDR Building", "Lynn.Brandon@unt.edu"),
            ("Ms. Kristina Bruder", "330 E", "MDR Building", "Kristina.Bruder@unt.edu"),
            ("Dr. Swagata Chakraborty", "342 B", "MDR Building", "Swagata.Chakraborty@unt.edu"),
            ("Dr. Christy Crutsinger", "330 P", "MDR Building", "Christy.Crutsinger@unt.edu"),
            ("Dr. Jonghan Hyun", "330 H", "MDR Building", "Jonghan.Hyun@unt.edu"),
            ("Dr. Iva Jestratijevic", "330 F", "MDR Building", "Iva. Jestratijevic@unt.edu"),
            ("Dr. HaeJung Kim (Maria)", "342 G", "MDR Building", "Haejung.Kim@unt.edu"),
            ("Dr. Tammy Kinley", "330 M", "MDR Building", "Tammy.Kinley@unt.edu"),
            ("Dr. Dee Knight", "330 D", "MDR Building", "Dee.Knight@unt.edu"),
            ("Ms. Malini Ratnam", "330 G", "MDR Building", "Malini.Ratnam@unt.edu"),
            ("Dr. Kelcie Slaton", "342 D", "MDR Building", "Kelcie.Slaton@unt.edu"),
            ("Dr. Bugao Xu", "330 B", "MDR Building", "Bugao.Xu@unt.edu"),
            ("Dr. Kiseol Yang", "342 C", "MDR Building", "Kiseol.Yang@unt.edu"),
            ("Ms. Marissa Zorola", "342 F", "MDR Building", "Marissa.Zorola@unt.edu"),
            ("Dr. Kim Williams", "343 B", "MDR Building", "Kim.Williams2@unt.edu"),
            ("Ms. Ann Afflerbach", "359 C", "MDR Building", "Ann.Afflerbach@unt.edu"),
            ("Mr. Jeffrey Britain", "355 E", "MDR Building", "Jeffrey.Britain@unt.edu"),
            ("Dr. Priscilla Connors", "343 H", "MDR Building", "Priscilla.Connors@unt.edu"),
            ("Ms. Jodi Duryea", "343 F", "MDR Building", "Jodi.Duryea@unt.edu"),
            ("Ms. MT Hickman", "359 E", "MDR Building", "M.T.Hickman@unt.edu"),
            ("Dr. Yidan Huang", "359 B", "MDR Building", "Yidan.Huang@unt.edu"),
            ("Dr. Birendra KC", "343 E", "MDR Building", "Birendra.KC@unt.edu"),
            ("Dr. Lisa Kennon", "359 J", "MDR Building", "Lisa.Kennon@unt.edu"),
            ("Dr. Harold Lee", "355 C", "MDR Building", "Harold.Lee@unt.edu"),
            ("Dr. Xi Leung (Cece)", "359 G", "MDR Building", "Xi.Leung@unt.edu"),
            ("Dr. Luwis Mhlanga", "Gateway 077", "Gateway Building", "Luwis.Mhlanga@unt.edu"),
            ("Dr. Jihye Min (Ellie)", "359 H", "MDR Building", "Jihye.Min@unt.edu"),
            ("Dr. Joseph O'Donnell", "359 E", "MDR Building", "Joseph.O'Donnell@unt.edu"),
            ("Dr. Soona Park", "343 D", "MDR Building", "Soona.Park@unt.edu"),
            ("Mr. Mark Schneider", "Online", "Online", "Mark.Schneider@unt.edu"),
            ("Dr. Dan Spears", "343 A", "MDR Building", "Daniel.Spears@unt.edu"),
            ("Mr. Todd Uglow JD", "359 M", "MDR Building", "Todd.Uglow@unt.edu"),
            ("Dr. Han Wen", "359 F", "MDR Building", "Han.Wen@unt.edu"),
            ("Dr. Xingyi Zhang", "343 G", "MDR Building", "Xingyi.Zhang@unt.edu"),
            ("Dr. Yanyan Zheng", "355 D", "MDR Building", "Yanyan.Zheng@unt.edu"),
            ("Kelly Spry", "385 C", "MDR Building", "Kelly.Spry@unt.edu"),
            ("Jennifer Landeros", "385 B", "MDR Building", "Jennifer.Landeros@unt.edu"),
            ("Syleria Skinner", "385", "MDR Building", "Skinner@unt.edu"),
            ("Jaymi Wenzel", "385 D", "MDR Building", "Jaymi.Wenzel@unt.edu"),
            ("Lakshimi Arumagam", "331 E", "MDR Building", "Thanalakshimi.Arumagam@unt.edu"),
            ("Dawn Paine", "342 H", "MDR Building", "Paine@unt.edu"),
            ("Cody Palmer", "359 A", "MDR Building", "Cody.Palmer2@unt.edu"),
            ("Dee Wilson", "333", "MDR Building", "Dee.Wilson@unt.edu"),
            ("Sampath Pamidimukkala", "355 A", "MDR Building", "Sampath.Pamidimukkala@unt.edu"),
            ("Andrew Johnston", "355 B", "MDR Building", "Andrew.Johnston@unt.edu"),
            ("Kyle White", "355 F", "MDR Building", "Kyle.White@unt.edu"),
            ("Kristen Kendrick Bigley", "207 N Elm", "207 N Elm", "Kristen.KendrickBigley@unt.edu"),
            ("John Munoz", "207 N Elm", "207 N Elm", "John.Munoz@unt.edu"),
            ("Hawley Jana", "Dean's Office", "MDR Building", "jana.hawley@unt.edu"),
            ("Sankaramanchi Pvsss Manikanth", "IT Services", "MDR Building", "PvsssManikanth.Sankaramanchi@unt.edu"),
            ("Makkapati Abhiram", "IT Services", "MDR Building", "Abhiram.Makkapati@unt.edu"),
            ("Chalasani Kusuma Satya Sreeja", "IT Services", "MDR Building", "KusumaSatyaSreeja.Chalasani@unt.edu"),
            ("Gogineni Varshitha", "IT Services", "MDR Building", "Varshitha.Gogineni@unt.edu"),
            ("Mohammed Imaduddin Ahmed", "IT Services", "MDR Building", "ImaduddinAhmed.Mohammed@unt.edu")
        ]
        
        c.executemany("INSERT INTO faculty VALUES (?, ?, ?, ?)", faculty_data)
        print("✅ Faculty data inserted successfully.")
    
    # Check if room directions data already exists
    c.execute("SELECT COUNT(*) FROM room_directions")
    if c.fetchone()[0] == 0:
        # Insert room directions data
        room_directions = []
        for room_num in range(300, 400):
            room_directions.append((f"Room {room_num}", ""))
        
        # Add specific room directions from the JSON file
        specific_directions = [
            ("Room 300", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 301", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 302", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 303", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 304", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 305", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 306", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 307", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 308", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 309", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 310", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 311", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 312", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 313", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 314", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 315", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 316", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 317", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 318", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 319", "To your Right from help desk and then left"),
            ("Room 320", "To your Right from help desk and then left"),
            ("Room 321", "To your Right from help desk and then left"),
            ("Room 322", "To your Right from help desk and then left"),
            ("Room 323", "To your Right from help desk and then left"),
            ("Room 324", "To your Right from help desk and then left"),
            ("Room 325", "To your Right from help desk and then left"),
            ("Room 326", "To your Right from help desk and then left"),
            ("Room 327", "To your Right from help desk and then left"),
            ("Room 328", "To your Right from help desk and then left"),
            ("Room 329", "To your RIGHT from the Help Desk."),
            ("Room 330", "To your RIGHT from the Help Desk."),
            ("Room 331", "To your RIGHT from the Help Desk."),
            ("Room 332", "To your RIGHT from the Help Desk."),
            ("Room 333", "To your RIGHT from the Help Desk."),
            ("Room 334", "To your RIGHT from the Help Desk."),
            ("Room 335", "To your RIGHT from the Help Desk."),
            ("Room 336", "To your RIGHT from the Help Desk."),
            ("Room 337", "To your RIGHT from the Help Desk."),
            ("Room 338", "To your RIGHT from the Help Desk."),
            ("Room 339", "To your RIGHT from the Help Desk."),
            ("Room 340", "BACK SIDE of the Help Desk (can go left or right to reach)."),
            ("Room 341", "BACK SIDE of the Help Desk (can go left or right to reach)."),
            ("Room 342", "BACK SIDE of the Help Desk (can go left or right to reach)."),
            ("Room 343", "BACK SIDE of the Help Desk (can go left or right to reach)."),
            ("Room 344", "BACK SIDE of the Help Desk (can go left or right to reach)."),
            ("Room 345", "BACK SIDE of the Help Desk (can go left or right to reach)."),
            ("Room 346", "BACK SIDE of the Help Desk (can go left or right to reach)."),
            ("Room 347", "BACK SIDE of the Help Desk (can go left or right to reach)."),
            ("Room 348", "BACK SIDE of the Help Desk (can go left or right to reach)."),
            ("Room 349", "BACK SIDE of the Help Desk (can go left or right to reach)."),
            ("Room 350", "BACK SIDE of the Help Desk (can go left or right to reach)."),
            ("Room 351", "BACK SIDE of the Help Desk (can go left or right to reach)."),
            ("Room 352", "BACK SIDE of the Help Desk (can go left or right to reach)."),
            ("Room 353", "BACK SIDE of the Help Desk (can go left or right to reach)."),
            ("Room 354", "BACK SIDE of the Help Desk (can go left or right to reach)."),
            ("Room 355", "BACK SIDE of the Help Desk (can go left or right to reach)."),
            ("Room 356", "To your LEFT from the Help Desk and you will find stairs to department of behaviour analysis block"),
            ("Room 357", "To your LEFT from the Help Desk and you will find stairs to department of behaviour analysis block"),
            ("Room 358", "To your LEFT from the Help Desk and you will find stairs to department of behaviour analysis block"),
            ("Room 359", "To your LEFT from the Help Desk and you will find stairs to department of behaviour analysis block"),
            ("Room 360", "To your LEFT from the Help Desk and you will find stairs to department of behaviour analysis block"),
            ("Room 361", "To your LEFT from the Help Desk and you will find stairs to department of behaviour analysis block"),
            ("Room 362", "To your LEFT from the Help Desk and you will find stairs to department of behaviour analysis block"),
            ("Room 363", "To your LEFT from the Help Desk and you will find stairs to department of behaviour analysis block"),
            ("Room 364", "To your LEFT from the Help Desk and you will find stairs to department of behaviour analysis block"),
            ("Room 365", "To your LEFT from the Help Desk and you will find stairs to department of behaviour analysis block"),
            ("Room 366", "To your LEFT from the Help Desk and you will find stairs to department of behaviour analysis block"),
            ("Room 367", "To your LEFT from the Help Desk and you will find stairs to department of behaviour analysis block"),
            ("Room 368", "To your LEFT from the Help Desk and you will find stairs to department of behaviour analysis block"),
            ("Room 369", "To your LEFT from the Help Desk and you will find stairs to department of behaviour analysis block"),
            ("Room 370", "To your LEFT from the Help Desk and you will find stairs to department of behaviour analysis block"),
            ("Room 371", "To your LEFT from the Help Desk and you will find stairs to department of behaviour analysis block"),
            ("Room 372", "To your LEFT from the Help Desk and you will find stairs to department of behaviour analysis block"),
            ("Room 373", "To your LEFT from the Help Desk and you will find stairs to department of behaviour analysis block"),
            ("Room 374", "To your LEFT from the Help Desk and you will find stairs to department of behaviour analysis block"),
            ("Room 375", "To your LEFT from the Help Desk and you will find stairs to department of behaviour analysis block"),
            ("Room 376", "To your LEFT from the Help Desk and you will find stairs to department of behaviour analysis block"),
            ("Room 377", "To your LEFT from the Help Desk and you will find stairs to department of behaviour analysis block"),
            ("Room 378", "To your LEFT from the Help Desk and you will find stairs to department of behaviour analysis block"),
            ("Room 379", "To your LEFT from the Help Desk and you will find stairs to department of behaviour analysis block"),
            ("Room 380", "To your LEFT from the Help Desk and you will find stairs to department of behaviour analysis block"),
            ("Room 381", "FURTHER BACK past the Help Desk (left turn near stairs)."),
            ("Room 382", "FURTHER BACK past the Help Desk (left turn near stairs)."),
            ("Room 383", "FURTHER BACK past the Help Desk (left turn near stairs)."),
            ("Room 384", "FURTHER BACK past the Help Desk (left turn near stairs)."),
            ("Room 385", "Advising room (Next to the Elevator)"),
            ("Room 386", "Help Desk (Room 386) is here."),
            ("Room 387", "Right beside the Help Desk."),
            ("Room 388", "To your left from the Help Desk go straight, right turn and then you will find 388 room"),
            ("Room 389", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 390", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 391", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 392", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 393", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 394", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 395", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 396", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 397", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 398", "IN FRONT of the Help Desk (towards the entrance)."),
            ("Room 399", "IN FRONT of the Help Desk (towards the entrance).")
        ]
        
        # Insert all room directions
        c.executemany("INSERT INTO room_directions VALUES (?, ?)", room_directions)
        c.executemany("INSERT OR REPLACE INTO room_directions VALUES (?, ?)", specific_directions)
        print("✅ Room directions data inserted successfully.")
    
    conn.commit()
    conn.close()

def search_faculty(query):
    """Search for faculty members in the database with intelligent fuzzy matching"""
    # Store original query for error messages
    original_query = query
    
    # First preprocess the query to handle common variations
    query = preprocess_query(query)
    
    conn = sqlite3.connect("college.db")
    c = conn.cursor()
    
    # Clean and prepare the query for searching
    query_clean = query.lower().strip()
    
    # Remove common filler words that don't help with search
    filler_words = ['where', 'is', 'are', 'the', 'office', 'room', 'located', 'find', 'can', 'i', 'do', 'live', 'work', 'teach', 'professor', 'dr', 'doctor', 's', "'s", 'please', 'tell', 'me', 'about', 'show', 'give', 'directions', 'to', 'faculty', 'member', 'staff', 'academic', 'teacher', 'instructor', 'lecturer']
    for word in filler_words:
        query_clean = query_clean.replace(word, ' ').strip()
    
    # Clean up extra spaces
    query_clean = ' '.join(query_clean.split())
    
    # Split into potential name parts
    name_parts = [part.strip() for part in query_clean.split() if part.strip() and len(part) > 1]
    
    if not name_parts:
        conn.close()
        return "I couldn't understand the name. Please try saying the professor's name more clearly."
    
    # Get all faculty members for comparison
    c.execute("SELECT * FROM faculty")
    all_faculty = c.fetchall()
    
    # Score-based search system with enhanced matching
    best_matches = []
    
    for faculty in all_faculty:
        faculty_name = faculty[0].lower()
        faculty_name_parts = faculty_name.split()
        
        score = 0
        
        # Exact match gets highest score
        if query_clean == faculty_name:
            score = 100
        # Contains the full query
        elif query_clean in faculty_name:
            score = 90
        # Faculty name contains the query
        elif faculty_name in query_clean:
            score = 85
        
        # Enhanced partial matching for individual words
        for query_part in name_parts:
            for faculty_part in faculty_name_parts:
                # Exact word match
                if query_part == faculty_part:
                    score += 35
                # Partial word match (for typos or abbreviations)
                elif query_part in faculty_part or faculty_part in query_part:
                    score += 25
                # Sound-alike matching (enhanced version)
                elif len(query_part) > 2 and len(faculty_part) > 2:
                    # Check if words start with same letters (common abbreviation)
                    if query_part[:3] == faculty_part[:3]:
                        score += 20
                    # Check if words end with same letters
                    elif len(query_part) >= 3 and len(faculty_part) >= 3:
                        if query_part[-3:] == faculty_part[-3:]:
                            score += 15
                    # Check for common phonetic variations
                    elif len(query_part) >= 4 and len(faculty_part) >= 4:
                        # Handle common sound-alike patterns
                        if query_part[:4] == faculty_part[:4]:
                            score += 18
                        elif query_part[-4:] == faculty_part[-4:]:
                            score += 12
        
        # Bonus for having multiple matching parts
        if len(name_parts) > 1:
            matching_parts = sum(1 for qp in name_parts if any(qp in fp or fp in qp for fp in faculty_name_parts))
            if matching_parts >= 2:
                score += 30
            # Extra bonus for having most parts match
            if matching_parts >= len(name_parts) * 0.7:  # 70% or more parts match
                score += 20
        
        # Bonus for matching first or last name specifically
        if len(faculty_name_parts) >= 2:
            # Check if query matches first name
            if name_parts[0] in faculty_name_parts[0] or faculty_name_parts[0] in name_parts[0]:
                score += 15
            # Check if query matches last name
            if len(name_parts) > 1 and (name_parts[-1] in faculty_name_parts[-1] or faculty_name_parts[-1] in name_parts[-1]):
                score += 15
        
        # Add to results if we have any score
        if score > 0:
            best_matches.append((faculty, score))
    
    # Sort by score (highest first)
    best_matches.sort(key=lambda x: x[1], reverse=True)
    
    conn.close()
    
    if best_matches:
        # Get the best match
        best_match = best_matches[0]
        faculty = best_match[0]
        score = best_match[1]
        
        # Only return if score is high enough (to avoid false positives)
        if score >= 25:  # Increased threshold for better accuracy
            faculty_name = faculty[0]
            faculty_room = faculty[1]
            faculty_building = faculty[2]
            faculty_email = faculty[3]
            
            # Validate that we have the required information
            if not faculty_name or not faculty_room or not faculty_building:
                return "Information not available. Please contact help desk."
            
            # Get room directions for the faculty's room
            conn = sqlite3.connect("college.db")
            c = conn.cursor()
            
            # Extract base room number (remove letters like A, B, C, etc.)
            import re
            base_room_match = re.search(r'(\d+)', faculty_room)
            if base_room_match:
                base_room_number = base_room_match.group(1)
                room_query = f"Room {base_room_number}"
                
                # Search for room direction for the base room number
                c.execute("SELECT * FROM room_directions WHERE room = ? AND direction != ''", (room_query,))
                room_results = c.fetchall()
                
                conn.close()
                
                # Build the response with only available information
                response = f"{faculty_name} is located in Room {faculty_room} in {faculty_building}."
                
                if room_results:
                    response += f" {room_results[0][1]}"
                
                if faculty_email and faculty_email != "":
                    response += f" Contact: {faculty_email}."
                
                return response
            else:
                conn.close()
                # Fallback if we can't extract room number
                response = f"{faculty_name} is located in Room {faculty_room} in {faculty_building}."
                if faculty_email and faculty_email != "":
                    response += f" Contact: {faculty_email}."
                return response
    
    # If no good matches found, provide specific response with user's input
    # Extract the name from the original query for better error message
    original_words = original_query.lower().split()
    
    # Remove common question words and filler words to get the actual name
    question_words = ['where', 'is', 'are', 'the', 'office', 'room', 'located', 'find', 'can', 'i', 'do', 'live', 'work', 'teach', 'professor', 'dr', 'doctor', 's', "'s", 'please', 'tell', 'me', 'about', 'show', 'give', 'directions', 'to', 'faculty', 'member', 'staff', 'academic', 'teacher', 'instructor', 'lecturer', 'who', 'what', 'how', 'when', 'why', 'which']
    
    # Filter out question words and keep potential name parts
    name_parts = [word for word in original_words if word.lower() not in question_words and len(word) > 1]
    
    if name_parts:
        # Join the name parts to form the requested name
        requested_name = ' '.join(name_parts).title()
        return f"I don't have information about {requested_name}. Please contact the help desk."
    else:
        return "I don't have information about that person. Please contact the help desk."

def search_room(query):
    """Search for room directions in the database with enhanced pattern recognition"""
    conn = sqlite3.connect("college.db")
    c = conn.cursor()
    
    # Extract room number from query using multiple patterns
    import re
    
    # Multiple patterns to match room queries
    room_patterns = [
        r'room\s*(\d+)',           # "room 304", "room304"
        r'(\d+)\s*room',           # "304 room", "304room"
        r'office\s*(\d+)',         # "office 304", "office304"
        r'(\d+)\s*office',         # "304 office", "304office"
        r'classroom\s*(\d+)',      # "classroom 304", "classroom304"
        r'(\d+)\s*classroom',      # "304 classroom", "304classroom"
        r'lab\s*(\d+)',            # "lab 304", "lab304"
        r'(\d+)\s*lab',            # "304 lab", "304lab"
        r'lecture\s*(\d+)',        # "lecture 304", "lecture304"
        r'(\d+)\s*lecture',        # "304 lecture", "304lecture"
        r'studio\s*(\d+)',         # "studio 304", "studio304"
        r'(\d+)\s*studio',         # "304 studio", "304studio"
        r'seminar\s*(\d+)',        # "seminar 304", "seminar304"
        r'(\d+)\s*seminar',        # "304 seminar", "304seminar"
        r'conference\s*(\d+)',     # "conference 304", "conference304"
        r'(\d+)\s*conference',     # "304 conference", "304conference"
        r'(\d+)',                  # Just the number "304" (fallback)
    ]
    
    room_number = None
    for pattern in room_patterns:
        room_match = re.search(pattern, query.lower())
        if room_match:
            room_number = room_match.group(1)
            break
    
    if room_number:
        room_query = f"Room {room_number}"
        
        # Search for room direction - get the one with actual direction text
        c.execute("SELECT * FROM room_directions WHERE room = ? AND direction != ''", (room_query,))
        results = c.fetchall()
        
        conn.close()
        
        if results:
            return f"Room {room_number} is {results[0][1]}."
        else:
            return "Information not available. Please contact help desk."
    else:
        conn.close()
        return "Please specify a room number."

def send_email_alert(subject, body):
    """Send email alert using Gmail SMTP"""
    if not all([SENDER_EMAIL, EMAIL_PASSWORD, RECEIVER_EMAIL]):
        print("❌ Email credentials not configured")
        return False
        
    try:
        message = f"Subject: {subject}\n\n{body}"
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, EMAIL_PASSWORD)
            smtp.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)
            
        print(f"✅ Email alert sent: {subject}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return False

def preprocess_query(query):
    """Preprocess the query to handle common variations and improve search accuracy"""
    query = query.lower().strip()
    
    # Common variations and their standard forms
    variations = {
        # Common abbreviations and titles
        "dr": "doctor",
        "prof": "professor",
        "mr": "mister",
        "ms": "miss",
        "mrs": "missus",
        "assoc": "associate",
        "asst": "assistant",
        "adj": "adjunct",
        
        # Common misspellings or phonetic variations
        "johnston": "johnston",  # Keep as is
        "johnson": "johnston",   # Common misspelling
        "andrew": "andrew",      # Keep as is
        "andy": "andrew",        # Common nickname
        "kim": "kim",
        "kime": "kim",           # Common misspelling
        "williams": "williams",
        "william": "williams",   # Common variation
        "brandon": "brandon",
        "branden": "brandon",    # Common misspelling
        "kyle": "kyle",
        "kile": "kyle",          # Common misspelling
        "white": "white",
        "whyte": "white",        # Common variation
        "kristina": "kristina",
        "christina": "kristina", # Common variation
        "swagata": "swagata",
        "swagatha": "swagata",   # Common misspelling
        "christy": "christy",
        "christie": "christy",   # Common variation
        "jonghan": "jonghan",
        "jong": "jonghan",       # Common abbreviation
        "iva": "iva",
        "eva": "iva",            # Common misspelling
        "haejung": "haejung",
        "hae": "haejung",        # Common abbreviation
        "tammy": "tammy",
        "tami": "tammy",         # Common variation
        "dee": "dee",
        "de": "dee",             # Common abbreviation
        "malini": "malini",
        "malini": "malini",      # Keep as is
        "kelcie": "kelcie",
        "kelsie": "kelcie",      # Common variation
        "bugao": "bugao",
        "bug": "bugao",          # Common abbreviation
        "kiseol": "kiseol",
        "kiseol": "kiseol",      # Keep as is
        "marissa": "marissa",
        "marisa": "marissa",     # Common variation
        
        # Common question variations and phrasings
        "where is": "where",
        "where's": "where",
        "where are": "where",
        "where can i find": "where",
        "where do i find": "where",
        "where is the": "where",
        "where's the": "where",
        "where can i locate": "where",
        "where do i locate": "where",
        "where is located": "where",
        "where are located": "where",
        "can you tell me": "",
        "could you tell me": "",
        "i need to find": "",
        "i'm looking for": "",
        "i want to find": "",
        "i would like to find": "",
        "i would like to meet": "",
        "i want to meet": "",
        "i need to meet": "",
        "i'm trying to find": "",
        "i'm trying to locate": "",
        "i need to locate": "",
        "i'm searching for": "",
        "i'm looking to find": "",
        "i need directions to": "where",
        "i need directions for": "where",
        "i need help finding": "",
        "i need help locating": "",
        "show me": "",
        "give me": "",
        "tell me about": "",
        "what about": "",
        "how do i find": "where",
        "how can i find": "where",
        "how do i get to": "where",
        "how can i get to": "where",
        "which way to": "where",
        "what's the way to": "where",
        "what is the way to": "where",
        "directions to": "where",
        "location of": "where",
        "office of": "where",
        "room of": "where",
        "classroom of": "where",
        "whereabouts of": "where",
        "position of": "where",
        "situation of": "where",
        
        # Room-related variations
        "room": "room",
        "office": "room",
        "classroom": "room",
        "lecture hall": "room",
        "lecture room": "room",
        "lab": "room",
        "laboratory": "room",
        "studio": "room",
        "seminar room": "room",
        "conference room": "room",
        "meeting room": "room",
        "workshop": "room",
        "computer lab": "room",
        "research lab": "room",
        "study room": "room",
        "tutorial room": "room",
        
        # Building-related variations
        "building": "building",
        "mdr": "mdr building",
        "mdr building": "mdr building",
        "gateway": "gateway building",
        "gateway building": "gateway building",
        "elm": "207 n elm",
        "207 n elm": "207 n elm",
        "207 north elm": "207 n elm",
        "north elm": "207 n elm",
        "elm street": "207 n elm",
        "main building": "mdr building",
        "merchandising building": "mdr building",
        "hospitality building": "mdr building",
        "tourism building": "mdr building",
        
        # Faculty-related variations
        "professor": "faculty",
        "teacher": "faculty",
        "instructor": "faculty",
        "lecturer": "faculty",
        "staff": "faculty",
        "faculty member": "faculty",
        "academic": "faculty",
        "doctor": "faculty",
        "dr": "faculty",
        "educator": "faculty",
        "scholar": "faculty",
        "researcher": "faculty",
        "academic staff": "faculty",
        "teaching staff": "faculty",
        "faculty staff": "faculty",
        
        # Common filler words and speech patterns
        "um": "",
        "uh": "",
        "like": "",
        "you know": "",
        "i mean": "",
        "actually": "",
        "basically": "",
        "literally": "",
        "sort of": "",
        "kind of": "",
        "well": "",
        "so": "",
        "right": "",
        "okay": "",
        "ok": "",
        "yeah": "",
        "yes": "",
        "no": "",
        "not": "",
        "just": "",
        "only": "",
        "really": "",
        "very": "",
        "quite": "",
        "rather": "",
        "somewhat": "",
        "somehow": "",
        "anyway": "",
        "anyhow": "",
        "therefore": "",
        "thus": "",
        "hence": "",
        "consequently": "",
        "however": "",
        "nevertheless": "",
        "nonetheless": "",
        "meanwhile": "",
        "furthermore": "",
        "moreover": "",
        "additionally": "",
        "besides": "",
        "also": "",
        "too": "",
        "as well": "",
        "in addition": "",
        "further": "",
        "furthermore": "",
        "by the way": "",
        "speaking of": "",
        "in terms of": "",
        "as far as": "",
        "in regard to": "",
        "with regard to": "",
        "concerning": "",
        "regarding": "",
        "about": "",
        "concerning": "",
        "pertaining to": "",
        "related to": "",
        "in relation to": "",
        "in connection with": "",
        "in conjunction with": "",
        "together with": "",
        "along with": "",
        "as well as": "",
        "in addition to": "",
        "apart from": "",
        "other than": "",
        "except for": "",
        "excluding": "",
        "including": "",
        "such as": "",
        "for example": "",
        "for instance": "",
        "namely": "",
        "specifically": "",
        "particularly": "",
        "especially": "",
        "notably": "",
        "remarkably": "",
        "significantly": "",
        "considerably": "",
        "substantially": "",
        "largely": "",
        "mainly": "",
        "mostly": "",
        "primarily": "",
        "chiefly": "",
        "principally": "",
        "essentially": "",
        "fundamentally": "",
        "basically": "",
        "essentially": "",
        "virtually": "",
        "practically": "",
        "nearly": "",
        "almost": "",
        "approximately": "",
        "roughly": "",
        "about": "",
        "around": "",
        "circa": "",
        "somewhere": "",
        "someplace": "",
        "anywhere": "",
        "anyplace": "",
        "everywhere": "",
        "everyplace": "",
        "nowhere": "",
        "noplace": "",
        "somewhere": "",
        "someplace": "",
        "anywhere": "",
        "anyplace": "",
        "everywhere": "",
        "everyplace": "",
        "nowhere": "",
        "noplace": ""
    }
    
    # Apply variations
    for variation, replacement in variations.items():
        if replacement:
            query = query.replace(variation, replacement)
        else:
            # Remove the word entirely
            query = query.replace(variation, "")
    
    # Clean up extra spaces and normalize
    query = ' '.join(query.split())
    
    # Remove common punctuation that might interfere with search
    query = query.replace("?", "").replace(".", "").replace(",", "").replace("!", "").replace(":", "").replace(";", "").replace("-", " ").replace("_", " ")
    
    # Clean up extra spaces again after punctuation removal
    query = ' '.join(query.split())
    
    return query

def is_ending_phrase(query):
    """Check if the query contains ending phrases that should automatically end the interaction"""
    query_lower = query.lower().strip()
    
    for phrase in ENDING_PHRASES:
        if phrase in query_lower:
            return True
    
    return False

def get_ending_response(query):
    """Generate an appropriate ending response based on the user's input"""
    query_lower = query.lower().strip()
    
    if any(phrase in query_lower for phrase in ['thank you', 'thanks']):
        return "You're welcome! I'm glad I could help. Have a great day!"
    elif any(phrase in query_lower for phrase in ['okay', 'ok', 'alright']):
        return "Alright! Feel free to ask if you need anything else. Have a great day!"
    elif any(phrase in query_lower for phrase in ['goodbye', 'bye', 'see you']):
        return "Goodbye! Have a wonderful day!"
    elif any(phrase in query_lower for phrase in ['that\'s all', 'that is all', 'i\'m done', 'i am done', 'finished', 'done']):
        return "Perfect! I'm here whenever you need assistance. Have a great day!"
    else:
        return "Thank you for using the CMHT-IT Voice Assistant. Have a great day!"

def analyze_query_intent(query):
    """Analyze the intent of a query to better understand what the user is asking for"""
    query_lower = query.lower().strip()
    
    # Intent patterns for different types of queries
    intent_patterns = {
        'faculty_search': [
            'dr', 'doctor', 'professor', 'prof', 'teacher', 'instructor', 'lecturer',
            'faculty', 'staff', 'academic', 'member', 'where', 'find', 'located',
            'meet', 'looking', 'trying', 'need', 'want', 'would like', 'office', 'room'
        ],
        'room_search': [
            'room', 'office', 'classroom', 'lab', 'laboratory', 'lecture', 'studio',
            'seminar', 'conference', 'where', 'location', 'directions', 'find', 'show', 'tell'
        ],
        'greeting': [
            'hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening',
            'greetings', 'howdy'
        ],
        'help_request': [
            'help', 'what can you do', 'assist', 'capabilities', 'support', 'guide',
            'explain', 'tell me about', 'what about'
        ],
        'ending': [
            'thank you', 'thanks', 'okay', 'ok', 'alright', 'goodbye', 'bye',
            'see you', 'that\'s all', 'i\'m done', 'finished', 'done'
        ]
    }
    
    # Score each intent based on pattern matches
    intent_scores = {}
    for intent, patterns in intent_patterns.items():
        score = 0
        for pattern in patterns:
            if pattern in query_lower:
                score += 1
        intent_scores[intent] = score
    
    # Return the intent with the highest score
    if intent_scores:
        best_intent = max(intent_scores, key=intent_scores.get)
        if intent_scores[best_intent] > 0:
            return best_intent
    
    # Default to faculty search if no clear intent
    return 'faculty_search'

def get_query_suggestions(query_type):
    """Provide helpful suggestions based on the type of query"""
    suggestions = {
        'faculty_search': [
            "Try saying: 'Where is Dr. Kim Williams?'",
            "Or: 'I need to find Andrew Johnston'",
            "Or: 'Show me Kyle White's office'",
            "Or: 'I would like to meet Dr. Lynn Brandon'"
        ],
        'room_search': [
            "Try saying: 'Where is room 304?'",
            "Or: 'Show me office 330'",
            "Or: 'Directions to classroom 342'",
            "Or: 'How do I find lab 385?'"
        ],
        'general': [
            "Ask about any faculty member by name",
            "Ask about any room number",
            "Say 'hello' for a greeting",
            "Say 'help' to learn what I can do"
        ]
    }
    
    return suggestions.get(query_type, suggestions['general'])

def process_voice_query(text):
    """Process the voice query and return appropriate response with enhanced pattern recognition"""
    # Check for ending phrases first
    if is_ending_phrase(text):
        return get_ending_response(text)
    
    # Store original text for faculty search
    original_text = text
    
    # Preprocess the query to handle common variations
    processed_text = preprocess_query(text)
    
    # Analyze query intent to better understand what the user is asking for
    intent = analyze_query_intent(text)
    
    # Enhanced room number detection - check for any numeric patterns that might be room numbers
    if any(char.isdigit() for char in processed_text):
        # Check if this looks like a room query
        room_indicators = ["room", "office", "classroom", "lab", "laboratory", "lecture", "studio", "seminar", "conference", "where", "location", "directions", "find", "show", "tell"]
        if any(indicator in processed_text for indicator in room_indicators):
            room_result = search_room(processed_text)
            if "Please specify a room number" not in room_result:
                return room_result
    
    # Enhanced faculty query detection with multiple patterns
    faculty_indicators = [
        "dr", "doctor", "professor", "prof", "faculty", "teacher", "instructor", "lecturer", 
        "staff", "academic", "member", "where", "find", "located", "who", "what", "how",
        "meet", "looking", "trying", "need", "want", "would like", "office", "room"
    ]
    
    # Check if query contains faculty indicators or looks like a name query
    if any(indicator in processed_text for indicator in faculty_indicators):
        # Try faculty search first
        faculty_result = search_faculty(original_text)
        if "I don't have information about" not in faculty_result:
            return faculty_result
    
    # Check for greeting patterns
    greeting_patterns = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "greetings", "howdy"]
    if any(greeting in processed_text for greeting in greeting_patterns):
        return "Hello! I can help you find faculty rooms and classroom locations."
    
    # Check for help request patterns
    help_patterns = ["help", "what can you do", "assist", "capabilities", "support", "guide", "explain", "tell me about", "what about"]
    if any(help_pattern in processed_text for help_pattern in help_patterns):
        return "I can help you find faculty rooms and classroom locations."
    
    # Enhanced name pattern detection
    words = processed_text.split()
    if len(words) >= 2:
        # Check if the query looks like it could be a name (2+ words, no obvious question words)
        potential_name_query = True
        question_words = ["what", "where", "when", "why", "how", "which", "who", "when", "why"]
        
        # If it starts with a question word, it's probably not a name
        if words[0] in question_words:
            potential_name_query = False
        
        # If it contains obvious non-name words, it's probably not a name
        non_name_words = ["room", "building", "floor", "class", "course", "schedule", "time", "email", "phone", "number", "address", "location", "directions"]
        if any(word in non_name_words for word in words):
            potential_name_query = False
        
        # If it looks like a potential name, try faculty search
        if potential_name_query:
            faculty_result = search_faculty(original_text)
            if "I don't have information about" not in faculty_result:
                return faculty_result
    
    # Check for general room queries without specific numbers
    # Remove "where" from room indicators since it's also used for faculty searches
    room_general_indicators = ["room", "office", "location", "classroom", "lab", "lecture", "studio"]
    if any(indicator in processed_text for indicator in room_general_indicators):
        return "Please specify which professor or room number."
    
    # Try faculty search as last resort for any query that might be a name
    faculty_result = search_faculty(original_text)
    if "I don't have information about" not in faculty_result:
        return faculty_result
    
    # Simple default response
    return "I didn't understand that. Please try again."

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/feedback-form')
def feedback_form():
    return send_from_directory('.', 'feedback.html')

@app.route('/config', methods=['GET'])
def get_config():
    """Get configuration settings for the frontend"""
    return jsonify({
        'silence_timeout_ms': SILENCE_TIMEOUT_SECONDS * 1000,
        'ending_phrases_count': len(ENDING_PHRASES)
    })

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        query = data.get('text', '')
        
        if not query:
            return jsonify({'answer': 'I didn\'t hear anything. Please try again.'})
        
        # Check if this is an ending phrase
        should_end_interaction = is_ending_phrase(query)
        
        # Process the voice query using local database
        answer = process_voice_query(query)
        
        # TTS
        tts = gTTS(answer)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        audio_bytes = fp.read()
        audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        return jsonify({
            "answer": answer, 
            "audio": audio_b64,
            "should_end_interaction": should_end_interaction
        })
    
    except Exception as e:
        return jsonify({'answer': f'Sorry, there was an error: {str(e)}'})

@app.route('/assistance', methods=['POST'])
def assistance():
    """Handle assistance requests and send email alerts"""
    try:
        data = request.get_json()
        assistance_type = data.get('type', '').lower()
        
        # Customize subject and body based on assistance type
        if assistance_type == 'laptop checkout':
            subject = "Laptop Checkout Request"
            body = "A student is at the help desk requesting a laptop checkout."
        elif assistance_type == 'laptop checkin':
            subject = "Laptop Checkin Request"
            body = "A student is at the help desk requesting a laptop."
        elif assistance_type == 'information':
            subject = "Student Needs Information/Assistance"
            body = "A student is at the help desk and needs information/assistance."
        else:
            subject = "Student at Help Desk"
            body = "A student is at the help desk."
        
        # Send email alert
        success = send_email_alert(subject, body)
        
        if success:
            return jsonify({
                "success": True, 
                "message": "<strong style='color: #00ff00; font-size: 16px;'>EMAIL SENT SUCCESSFULLY!</strong><br><br>A team member will be with you shortly. Thank you for your patience."
            })
        else:
            return jsonify({
                "success": False, 
                "message": "Failed to send email alert. Please check the console for errors."
            })
            
    except Exception as e:
        return jsonify({
            "success": False, 
            "message": f"Error processing assistance request: {str(e)}"
        })

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    """Submit feedback to Supabase"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'type' not in data or 'message' not in data:
            return jsonify({
                "success": False,
                "message": "Missing required fields: type and message are required"
            }), 400
        
        # Store feedback in Supabase
        result = feedback_manager.store_feedback(data)
        
        if result["success"]:
            return jsonify({
                "success": True,
                "message": "Feedback submitted successfully!",
                "feedback_id": result.get("id")
            })
        else:
            return jsonify({
                "success": False,
                "message": f"Failed to submit feedback: {result.get('message', 'Unknown error')}"
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error submitting feedback: {str(e)}"
        }), 500

@app.route('/feedback', methods=['GET'])
def get_feedback():
    """Retrieve feedback from Supabase"""
    try:
        # Get query parameters
        feedback_type = request.args.get('type')
        limit = request.args.get('limit', 100, type=int)
        
        if feedback_type:
            result = feedback_manager.get_feedback_by_type(feedback_type, limit)
        else:
            result = feedback_manager.get_all_feedback(limit)
        
        if result["success"]:
            return jsonify(result)
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error retrieving feedback: {str(e)}"
        }), 500

@app.route('/feedback/stats', methods=['GET'])
def get_feedback_stats():
    """Get feedback statistics"""
    try:
        result = feedback_manager.get_feedback_stats()
        
        if result["success"]:
            return jsonify(result)
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error getting feedback stats: {str(e)}"
        }), 500

@app.route('/feedback/<int:feedback_id>', methods=['PUT'])
def update_feedback(feedback_id):
    """Update a specific feedback record"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "message": "No update data provided"
            }), 400
        
        result = feedback_manager.update_feedback(feedback_id, data)
        
        if result["success"]:
            return jsonify(result)
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error updating feedback: {str(e)}"
        }), 500

@app.route('/feedback/<int:feedback_id>', methods=['DELETE'])
def delete_feedback(feedback_id):
    """Delete a specific feedback record"""
    try:
        result = feedback_manager.delete_feedback(feedback_id)
        
        if result["success"]:
            return jsonify(result)
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error deleting feedback: {str(e)}"
        }), 500

if __name__ == '__main__':
    print("Starting College Voice Assistant with SQLite database...")
    print("Initializing database...")
    init_database()
    
    # Initialize Supabase feedback manager
    print("Initializing Supabase feedback manager...")
    feedback_manager.create_feedback_table()
    
    print("Open your browser and go to: http://localhost:8080")
    print("Make sure to allow microphone access when prompted.")
    app.run(debug=False, port=8080)
