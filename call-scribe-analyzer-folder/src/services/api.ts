
import { mockRecordings } from '@/types';

// This is a mock API service for development
// In production, this would connect to a real backend API

const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export const api = {
  // Get all recordings
  getRecordings: async () => {
    await delay(800); // Simulate network delay
    return mockRecordings;
  },

  // Get a single recording by ID
  getRecording: async (id: number) => {
    await delay(600);
    const recording = mockRecordings.find(r => r.id === id);
    if (!recording) {
      throw new Error(`Recording with ID ${id} not found`);
    }
    return recording;
  },

  // Upload a new recording
  uploadRecording: async (file: File) => {
    await delay(1500); // Simulate upload time
    const newId = Math.max(...mockRecordings.map(r => r.id)) + 1;
    const newRecording: typeof mockRecordings[0] = {
      id: newId,
      filename: file.name,
      file_path: `/uploads/${file.name}`,
      duration: Math.floor(Math.random() * 1800) + 300, // Random duration between 5-35 minutes
      status: 'pending',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };
    
    mockRecordings.push(newRecording);
    return newRecording;
  },
  
  // Get silence analysis for a recording
  getSilenceAnalysis: async (recordingId: number) => {
    await delay(700);
    return {
      id: recordingId,
      recording_id: recordingId,
      total_silence_duration: Math.floor(Math.random() * 100) + 20,
      silence_percentage: Math.random() * 30,
      silence_segments: Array.from({ length: 8 }, () => ({
        start: Math.floor(Math.random() * 300),
        end: Math.floor(Math.random() * 300) + 300
      })),
      created_at: new Date().toISOString()
    };
  },
  
  // Get overtalk analysis for a recording
  getOvertalkAnalysis: async (recordingId: number) => {
    await delay(700);
    return {
      id: recordingId,
      recording_id: recordingId,
      total_overtalk_duration: Math.floor(Math.random() * 100) + 10,
      overtalk_percentage: Math.random() * 20,
      overtalk_segments: Array.from({ length: 5 }, () => ({
        start: Math.floor(Math.random() * 300),
        end: Math.floor(Math.random() * 300) + 300
      })),
      created_at: new Date().toISOString()
    };
  },
  
  // Get transcription for a recording
  getTranscription: async (recordingId: number) => {
    await delay(800);
    return {
      id: recordingId,
      recording_id: recordingId,
      text: "This is a sample transcription of a call. The conversation includes discussion about product features, pricing, and next steps. There are some moments of silence and a few instances where participants speak over each other.",
      confidence: 0.87,
      language: "en",
      created_at: new Date().toISOString()
    };
  }
};
