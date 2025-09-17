import { z } from 'zod';

/**
 * Schema for individual choice options in multiple choice questions.
 * Follows the same title/text pattern as real_play exercises.
 */
export const ChoiceSchema = z.object({
  /**
   * Short, punchy headline for the choice (3-6 words)
   * Example: "Studio Revenue Sharing"
   */
  title: z.string().min(1).describe('Short, punchy headline for the choice'),
  
  /**
   * Detailed description/subtitle for the choice (8-15 words)  
   * Example: "Studios take 70% of ticket revenue, limiting theaters' pricing control"
   */
  text: z.string().min(1).describe('Detailed description/subtitle for the choice'),
});

/**
 * Enhanced response schema for debate exercise endpoints with multiple choice options.
 * Used for v4 follow-up question APIs that provide structured choice selection
 * instead of free text input to break up conversation monotony.
 * 
 * Maintains all existing fields from DebateResponse while adding choice generation.
 */
export const DebateResponseMultipleChoiceSchema = z.object({
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
   * The acknowledgment and follow-up question to pose to the user.
   * This maintains the personalized, contextual questioning approach.
   * Required field, can be null if not applicable.
   */
  nextQuestion: z.string().nullable(),
  
  /**
   * Array of exactly 3 choice options with title and text.
   * Generated contextually based on the user's response and exercise type.
   * Each choice represents a different strategic angle or perspective.
   */
  choices: z.array(ChoiceSchema).describe('Array of contextual choice options'),
  
  /**
   * Selection type for the choices.
   * "single" - user can select one choice (default)
   * "multiple" - user can select multiple choices (for questions asking for multiple perspectives)
   */
  selectionType: z.enum(['single', 'multiple']).describe('Choice selection mode'),
});

export type Choice = z.infer<typeof ChoiceSchema>;
export type DebateResponseMultipleChoice = z.infer<typeof DebateResponseMultipleChoiceSchema>;