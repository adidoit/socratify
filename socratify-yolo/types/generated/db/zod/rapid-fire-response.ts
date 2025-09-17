import { z } from 'zod';

/**
 * Choice option schema for rapid fire multiple choice questions
 */
const ChoiceSchema = z.object({
  title: z.string().describe("Short choice label"),
  text: z.string().describe("Longer choice explanation"),
  correct: z.boolean().describe("Whether this choice is correct")
});

/**
 * Response schema specifically for rapid fire debate exercises.
 * Extends the base debate response pattern with multiple choice questions.
 * Used for rapid fire follow-up and final response endpoints.
 * 
 * All fields are required but nullable for consistent response structure
 * between OpenAI and Gemini APIs.
 */
export const RapidFireResponseSchema = z.object({
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
   * The multiple choice question to pose to the user.
   * This drives the rapid fire exercise forward.
   * Required field, can be null if not applicable.
   */
  nextQuestion: z.string().nullable(),
  
  /**
   * Array of exactly 3 multiple choice options with exactly one correct answer.
   * Required for rapid fire exercises to test quick decision making.
   */
  choices: z.array(ChoiceSchema).describe("Array of multiple choice options"),
});

export type RapidFireResponse = z.infer<typeof RapidFireResponseSchema>;
export type Choice = z.infer<typeof ChoiceSchema>;