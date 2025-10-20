from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY
import json
from datetime import datetime
from typing import Dict, List, Optional

class FeedbackManager:
    def __init__(self):
        """Initialize Supabase client"""
        try:
            self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
            print("✅ Supabase client initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing Supabase client: {str(e)}")
            self.supabase = None
    
    def create_feedback_table(self) -> bool:
        """Create the feedback table in Supabase if it doesn't exist"""
        if not self.supabase:
            return False
        
        try:
            # This will be handled by Supabase's automatic table creation
            # when we insert the first record, or you can create it manually in the dashboard
            print("✅ Feedback table ready (will be created automatically on first insert)")
            return True
        except Exception as e:
            print(f"❌ Error creating feedback table: {str(e)}")
            return False
    
    def store_feedback(self, feedback_data: Dict) -> Dict:
        """Store feedback in Supabase"""
        if not self.supabase:
            return {
                "success": False,
                "message": "Supabase client not initialized",
                "error": "Client initialization failed"
            }
        
        try:
            # Add timestamp if not provided
            if 'timestamp' not in feedback_data:
                feedback_data['timestamp'] = datetime.utcnow().isoformat()
            
            # Insert feedback into the 'feedback' table
            result = self.supabase.table('feedback').insert(feedback_data).execute()
            
            if result.data:
                print(f"✅ Feedback stored successfully: {feedback_data.get('type', 'Unknown')}")
                return {
                    "success": True,
                    "message": "Feedback stored successfully",
                    "data": result.data[0],
                    "id": result.data[0].get('id')
                }
            else:
                return {
                    "success": False,
                    "message": "No data returned from Supabase",
                    "error": "Empty response"
                }
                
        except Exception as e:
            print(f"❌ Error storing feedback: {str(e)}")
            return {
                "success": False,
                "message": f"Error storing feedback: {str(e)}",
                "error": str(e)
            }
    
    def get_all_feedback(self, limit: int = 100) -> Dict:
        """Retrieve all feedback from Supabase"""
        if not self.supabase:
            return {
                "success": False,
                "message": "Supabase client not initialized",
                "error": "Client initialization failed"
            }
        
        try:
            result = self.supabase.table('feedback').select('*').order('timestamp', desc=True).limit(limit).execute()
            
            if result.data is not None:
                return {
                    "success": True,
                    "message": f"Retrieved {len(result.data)} feedback records",
                    "data": result.data,
                    "count": len(result.data)
                }
            else:
                return {
                    "success": False,
                    "message": "No data returned from Supabase",
                    "error": "Empty response"
                }
                
        except Exception as e:
            print(f"❌ Error retrieving feedback: {str(e)}")
            return {
                "success": False,
                "message": f"Error retrieving feedback: {str(e)}",
                "error": str(e)
            }
    
    def get_feedback_by_type(self, feedback_type: str, limit: int = 50) -> Dict:
        """Retrieve feedback by type"""
        if not self.supabase:
            return {
                "success": False,
                "message": "Supabase client not initialized",
                "error": "Client initialization failed"
            }
        
        try:
            result = self.supabase.table('feedback').select('*').eq('type', feedback_type).order('timestamp', desc=True).limit(limit).execute()
            
            if result.data is not None:
                return {
                    "success": True,
                    "message": f"Retrieved {len(result.data)} {feedback_type} feedback records",
                    "data": result.data,
                    "count": len(result.data)
                }
            else:
                return {
                    "success": False,
                    "message": "No data returned from Supabase",
                    "error": "Empty response"
                }
                
        except Exception as e:
            print(f"❌ Error retrieving {feedback_type} feedback: {str(e)}")
            return {
                "success": False,
                "message": f"Error retrieving {feedback_type} feedback: {str(e)}",
                "error": str(e)
            }
    
    def get_feedback_by_date_range(self, start_date: str, end_date: str, limit: int = 100) -> Dict:
        """Retrieve feedback within a date range"""
        if not self.supabase:
            return {
                "success": False,
                "message": "Supabase client not initialized",
                "error": "Client initialization failed"
            }
        
        try:
            result = self.supabase.table('feedback').select('*').gte('timestamp', start_date).lte('timestamp', end_date).order('timestamp', desc=True).limit(limit).execute()
            
            if result.data is not None:
                return {
                    "success": True,
                    "message": f"Retrieved {len(result.data)} feedback records in date range",
                    "data": result.data,
                    "count": len(result.data)
                }
            else:
                return {
                    "success": False,
                    "message": "No data returned from Supabase",
                    "error": "Empty response"
                }
                
        except Exception as e:
            print(f"❌ Error retrieving feedback by date range: {str(e)}")
            return {
                "success": False,
                "message": f"Error retrieving feedback by date range: {str(e)}",
                "error": str(e)
            }
    
    def delete_feedback(self, feedback_id: int) -> Dict:
        """Delete a specific feedback record"""
        if not self.supabase:
            return {
                "success": False,
                "message": "Supabase client not initialized",
                "error": "Client initialization failed"
            }
        
        try:
            result = self.supabase.table('feedback').delete().eq('id', feedback_id).execute()
            
            if result.data:
                print(f"✅ Feedback {feedback_id} deleted successfully")
                return {
                    "success": True,
                    "message": "Feedback deleted successfully",
                    "deleted_id": feedback_id
                }
            else:
                return {
                    "success": False,
                    "message": "No feedback found with that ID",
                    "error": "Record not found"
                }
                
        except Exception as e:
            print(f"❌ Error deleting feedback: {str(e)}")
            return {
                "success": False,
                "message": f"Error deleting feedback: {str(e)}",
                "error": str(e)
            }
    
    def update_feedback(self, feedback_id: int, update_data: Dict) -> Dict:
        """Update a specific feedback record"""
        if not self.supabase:
            return {
                "success": False,
                "message": "Supabase client not initialized",
                "error": "Client initialization failed"
            }
        
        try:
            # Add updated timestamp
            update_data['updated_at'] = datetime.utcnow().isoformat()
            
            result = self.supabase.table('feedback').update(update_data).eq('id', feedback_id).execute()
            
            if result.data:
                print(f"✅ Feedback {feedback_id} updated successfully")
                return {
                    "success": True,
                    "message": "Feedback updated successfully",
                    "data": result.data[0]
                }
            else:
                return {
                    "success": False,
                    "message": "No feedback found with that ID",
                    "error": "Record not found"
                }
                
        except Exception as e:
            print(f"❌ Error updating feedback: {str(e)}")
            return {
                "success": False,
                "message": f"Error updating feedback: {str(e)}",
                "error": str(e)
            }
    
    def get_feedback_stats(self) -> Dict:
        """Get feedback statistics"""
        if not self.supabase:
            return {
                "success": False,
                "message": "Supabase client not initialized",
                "error": "Client initialization failed"
            }
        
        try:
            # Get total count
            total_result = self.supabase.table('feedback').select('*', count='exact').execute()
            total_count = total_result.count if hasattr(total_result, 'count') else 0
            
            # Get count by type
            types_result = self.supabase.table('feedback').select('type').execute()
            type_counts = {}
            if types_result.data:
                for record in types_result.data:
                    feedback_type = record.get('type', 'Unknown')
                    type_counts[feedback_type] = type_counts.get(feedback_type, 0) + 1
            
            return {
                "success": True,
                "message": "Feedback statistics retrieved successfully",
                "stats": {
                    "total_feedback": total_count,
                    "by_type": type_counts,
                    "types_count": len(type_counts)
                }
            }
                
        except Exception as e:
            print(f"❌ Error getting feedback stats: {str(e)}")
            return {
                "success": False,
                "message": f"Error getting feedback stats: {str(e)}",
                "error": str(e)
            }

# Create a global instance
feedback_manager = FeedbackManager() 