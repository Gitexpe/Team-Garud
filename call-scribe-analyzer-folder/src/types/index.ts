
export interface CallRecording {
  id: number;
  filename: string;
  file_path: string;
  duration: number;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  created_at: string;
  updated_at: string;
}

export interface Transcription {
  id: number;
  recording_id: number;
  text: string;
  confidence: number;
  language: string;
  created_at: string;
}

export interface SilenceAnalysis {
  id: number;
  recording_id: number;
  total_silence_duration: number;
  silence_percentage: number;
  silence_segments?: { start: number; end: number }[];
  created_at: string;
}

export interface OvertalkAnalysis {
  id: number;
  recording_id: number;
  total_overtalk_duration: number;
  overtalk_percentage: number;
  overtalk_segments?: { start: number; end: number }[];
  created_at: string;
}

// Mock data for development
export const mockRecordings: CallRecording[] = [
  {
    id: 1,
    filename: 'sales_call_001.mp3',
    file_path: '/uploads/sales_call_001.mp3',
    duration: 325,
    status: 'completed',
    created_at: '2023-11-10T14:30:00Z',
    updated_at: '2023-11-10T14:35:00Z'
  },
  {
    id: 2,
    filename: 'customer_support_002.mp3',
    file_path: '/uploads/customer_support_002.mp3',
    duration: 542,
    status: 'processing',
    created_at: '2023-11-11T09:15:00Z',
    updated_at: '2023-11-11T09:17:00Z'
  },
  {
    id: 3,
    filename: 'interview_003.mp3',
    file_path: '/uploads/interview_003.mp3',
    duration: 1830,
    status: 'pending',
    created_at: '2023-11-12T16:45:00Z',
    updated_at: '2023-11-12T16:45:00Z'
  },
  {
    id: 4,
    filename: 'conference_call_004.mp3',
    file_path: '/uploads/conference_call_004.mp3',
    duration: 3650,
    status: 'completed',
    created_at: '2023-11-13T11:20:00Z',
    updated_at: '2023-11-13T11:30:00Z'
  },
  {
    id: 5,
    filename: 'training_session_005.mp3',
    file_path: '/uploads/training_session_005.mp3',
    duration: 4500,
    status: 'failed',
    created_at: '2023-11-14T13:50:00Z',
    updated_at: '2023-11-14T14:00:00Z'
  }
];
