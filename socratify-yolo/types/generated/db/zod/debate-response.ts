import { z } from 'zod';

/**
 * Common response schema for debate exercise endpoints.
 * Used across all debate exercise types (options, questions, assumptions, etc.)
 * for follow-up, first-question, and final response endpoints.
 * 
 * All fields are required but nullable for consistent response structure
 * between OpenAI and Gemini APIs.
 */
export const DebateResponseSchema = z.object({
  /**
   * Cleaned and formatted transcript of the user's previous answer.
   * This may be received via audio or as text input.
   * Required field, can be null if not applicable.
   */
  userAnswerTranscript: z.string().nullable(),
  
  /**
   * AI's internal thinking process for determining the next question.
   * Used to show reasoning and ensure quality responses.
   * Required field, can be null if not applicable.
   */
  scratchPad: z.string().nullable(),
  
  /**
   * The summary sentence and final question to pose to the user.
   * This drives the Socratic dialogue forward.
   * Required field, can be null if not applicable.
   */
  nextQuestion: z.string().nullable(),
});

export type DebateResponse = z.infer<typeof DebateResponseSchema>;