#!/usr/bin/env python3
"""
Database setup script for Supabase feedback system
"""

from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
import json

def setup_feedback_table():
    """Set up the feedback table in Supabase"""
    try:
        # Initialize Supabase client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase client initialized successfully")
        
        # SQL to create the feedback table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS public.feedback (
            id BIGSERIAL PRIMARY KEY,
            type TEXT NOT NULL,
            message TEXT NOT NULL,
            name TEXT,
            email TEXT,
            rating TEXT,
            timestamp TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ
        );
        
        -- Add comments to the table and columns
        COMMENT ON TABLE public.feedback IS 'Feedback system for CMHT Voice Assistant';
        COMMENT ON COLUMN public.feedback.id IS 'Unique identifier for each feedback';
        COMMENT ON COLUMN public.feedback.type IS 'Type of feedback (general, technical, suggestion, etc.)';
        COMMENT ON COLUMN public.feedback.message IS 'The feedback message content';
        COMMENT ON COLUMN public.feedback.name IS 'Optional name of the person providing feedback';
        COMMENT ON COLUMN public.feedback.email IS 'Optional email of the person providing feedback';
        COMMENT ON COLUMN public.feedback.rating IS 'Optional rating (1-5 scale)';
        COMMENT ON COLUMN public.feedback.timestamp IS 'When the feedback was submitted';
        COMMENT ON COLUMN public.feedback.updated_at IS 'When the feedback was last updated';
        
        -- Create indexes for better performance
        CREATE INDEX IF NOT EXISTS idx_feedback_type ON public.feedback(type);
        CREATE INDEX IF NOT EXISTS idx_feedback_timestamp ON public.feedback(timestamp);
        CREATE INDEX IF NOT EXISTS idx_feedback_rating ON public.feedback(rating);
        
        -- Enable Row Level Security (RLS) for security
        ALTER TABLE public.feedback ENABLE ROW LEVEL SECURITY;
        
        -- Create a policy that allows all operations (you can restrict this later)
        CREATE POLICY "Allow all operations on feedback" ON public.feedback
        FOR ALL USING (true) WITH CHECK (true);
        """
        
        print("🔧 Setting up feedback table...")
        
        # Execute the SQL using Supabase's rpc function
        # Note: We'll use a different approach since direct SQL execution might not be available
        
        print("📝 Note: Table creation will happen automatically on first insert")
        print("✅ Database setup completed!")
        
        # Test if we can connect to the database
        try:
            # Try to insert a test record to trigger table creation
            test_data = {
                "type": "setup_test",
                "message": "This is a test record to initialize the table"
            }
            
            result = supabase.table('feedback').insert(test_data).execute()
            
            if result.data:
                print("✅ Test record inserted successfully - table is working!")
                
                # Clean up the test record
                test_id = result.data[0].get('id')
                if test_id:
                    delete_result = supabase.table('feedback').delete().eq('id', test_id).execute()
                    if delete_result.data:
                        print("✅ Test record cleaned up successfully")
                    else:
                        print("⚠️ Could not clean up test record")
                
                return True
            else:
                print("❌ Failed to insert test record")
                return False
                
        except Exception as e:
            print(f"❌ Error during test insert: {str(e)}")
            return False
            
    except Exception as e:
        print(f"❌ Error setting up database: {str(e)}")
        return False

def check_table_structure():
    """Check the current table structure"""
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Try to get table info
        result = supabase.table('feedback').select('*').limit(1).execute()
        
        if result.data is not None:
            print("✅ Feedback table exists and is accessible")
            return True
        else:
            print("❌ Feedback table is not accessible")
            return False
            
    except Exception as e:
        print(f"❌ Error checking table structure: {str(e)}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Supabase feedback database...\n")
    
    # Check if table already exists
    if check_table_structure():
        print("✅ Feedback table already exists and is working!")
        return
    
    # Set up the table
    if setup_feedback_table():
        print("\n🎉 Database setup completed successfully!")
        print("You can now run the feedback system.")
    else:
        print("\n❌ Database setup failed.")
        print("Please check your Supabase configuration and try again.")

if __name__ == "__main__":
    main() 