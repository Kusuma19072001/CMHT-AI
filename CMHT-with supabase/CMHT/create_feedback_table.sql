-- Create the feedback table for CMHT Voice Assistant
-- Run this script in your Supabase SQL Editor

-- Create the feedback table
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

-- Insert some sample feedback data for testing
INSERT INTO public.feedback (type, message, name, email, rating) VALUES
('general', 'Great voice assistant! Very helpful for finding faculty offices.', 'John Doe', 'john@example.com', '5'),
('suggestion', 'It would be great to have more detailed room directions.', 'Jane Smith', 'jane@example.com', '4'),
('technical', 'The voice recognition works well in quiet environments.', 'Bob Johnson', 'bob@example.com', '5'),
('praise', 'This system has made navigating the building much easier.', 'Alice Brown', 'alice@example.com', '5'),
('feature', 'Could you add support for finding available study rooms?', 'Charlie Wilson', 'charlie@example.com', '4');

-- Verify the table was created
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name = 'feedback' 
ORDER BY ordinal_position;

-- Show sample data
SELECT * FROM public.feedback ORDER BY timestamp DESC LIMIT 5; 