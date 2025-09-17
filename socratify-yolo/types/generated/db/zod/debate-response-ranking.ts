import { z } from 'zod';

/**
 * Schema for individual ranking items in ranking questions.
 * Follows the same structure as the Ranking component expects.
 */
export const RankingItemSchema = z.object({
  /**
   * Unique identifier for the ranking item
   * Example: "priority-1", "consideration-2"
   */
  id: z.string().min(1).describe('Unique identifier for the ranking item'),
  
  /**
   * Main text for the ranking item (concise, 3-10 words)
   * Example: "Immediate Crisis Response"
   */
  text: z.string().min(1).describe('Main text for the ranking item'),
  
  /**
   * Optional detailed description (8-20 words)
   * Example: "Address immediate safety concerns and contain the crisis"
   */
  description: z.string().nullable().describe('Optional detailed description of the ranking item'),
});

/**
 * Response schema for debate exercise endpoints with ranking questions.
 * Used for v4 follow-up question APIs that provide ranking items instead 
 * of text input to create more engaging, structured responses.
 * 
 * Maintains compatibility with existing DebateResponse structure while
 * adding ranking-specific data.
 */
export const DebateResponseRankingSchema = z.object({
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
   * The ranking question to pose to the user.
   * This should be clear and contextual to the role and situation.
   * Required field, can be null if not applicable.
   */
  nextQuestion: z.string().nullable(),
  
  /**
   * Array of exactly 3 ranking items with id, text, and optional description.
   * Generated contextually based on the user's response and exercise type.
   * Each item represents a different strategic priority or consideration.
   */
  rankingItems: z.array(RankingItemSchema).describe('Array of contextual ranking items'),
  
  /**
   * Instructions for how the user should rank the items.
   * Should provide clear guidance on ranking criteria.
   */
  rankingInstructions: z.string().describe('Instructions for ranking the items'),
});

export type RankingItem = z.infer<typeof RankingItemSchema>;
export type DebateResponseRanking = z.infer<typeof DebateResponseRankingSchema>;