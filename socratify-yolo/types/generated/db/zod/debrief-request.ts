import { z } from 'zod';
import { SocratifyQuestionSchema } from './socratify-question';
import { UserAnswerSchema } from './user-answer';

/**
 * Common debrief request schema used across all debrief endpoints
 * Contains the core data structure that most debrief APIs expect
 */
export const DebriefRequestSchema = z.object({
  socratifyQuestions: z.array(SocratifyQuestionSchema).describe('Array of questions asked to the user during the exercise'),
  userAnswers: z.array(UserAnswerSchema).describe('Array of user responses to the questions'),
  exerciseUuid: z.string().optional().describe('Exercise UUID for database lookup of context and happyPath'),
  context: z.string().optional().describe('Additional context about the exercise or situation (deprecated - use exerciseUuid)'),
  currentUserXP: z.number().optional().describe('User experience points/level'),
  userGoals: z.string().optional().describe('User-defined goals or objectives'),
  happyPath: z.string().optional().describe('Whether the user followed the expected happy path (deprecated - use exerciseUuid)'),
  answerText: z.string().optional().describe('Additional answer text (for intro/rapid reaction)'),
  answerAudio: z.any().optional().describe('Audio data if applicable'),
  isAudio: z.boolean().optional().describe('Whether the response includes audio'),
  keyQuestionText: z.string().optional().describe('Key question text for specific debriefs'),
  keyQuestionRole: z.string().optional().describe('Role context for the key question'),
});

export type DebriefRequest = z.infer<typeof DebriefRequestSchema>;