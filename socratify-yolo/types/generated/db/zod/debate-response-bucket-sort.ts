import { z } from 'zod';

/**
 * Schema for individual bucket definitions in bucket sort questions.
 * Defines the available buckets for categorization.
 */
export const BucketSchema = z.object({
  /**
   * Unique identifier for the bucket
   * Example: "winner", "loser", "neutral"
   */
  id: z.string().min(1).describe('Unique identifier for the bucket'),
  
  /**
   * Display label for the bucket (concise, 1-3 words)
   * Example: "Winner", "Loser", "Neutral"
   */
  label: z.string().min(1).describe('Display label for the bucket'),
  
  /**
   * Primary color for the bucket (hex format)
   * Example: "#22C55E", "#EF4444", "#9CA3AF"
   */
  color: z.string().regex(/^#[0-9A-Fa-f]{6}$/).describe('Primary color for the bucket in hex format'),
  
  /**
   * Gradient colors for enhanced visual appeal [start, end]
   * Example: ["#22C55E", "#16A34A"]
   */
  gradientColors: z.array(z.string().regex(/^#[0-9A-Fa-f]{6}$/)).length(2).describe('Two-color gradient array for bucket styling'),
});

/**
 * Schema for individual sortable items in bucket sort questions.
 * Follows the same structure as the BucketSort component expects.
 */
export const SortableItemSchema = z.object({
  /**
   * Unique identifier for the sortable item
   * Example: "impact-1", "factor-2"
   */
  id: z.string().min(1).describe('Unique identifier for the sortable item'),
  
  /**
   * Main text for the sortable item (concise, 3-10 words)
   * Example: "Customer loyalty from premium experience"
   */
  text: z.string().min(1).describe('Main text for the sortable item'),
  
  /**
   * Optional detailed description (8-25 words)
   * Example: "Building deeper customer relationships through enhanced store ambiance and longer visit times"
   */
  description: z.string().nullable().describe('Optional detailed description of the sortable item'),
});

/**
 * Response schema for debate exercise endpoints with bucket sort questions.
 * Used for v4 follow-up question APIs that provide bucket sorting items instead 
 * of text input to create more engaging, visual categorization experiences.
 * 
 * Maintains compatibility with existing DebateResponse structure while
 * adding bucket sort-specific data.
 */
export const DebateResponseBucketSortSchema = z.object({
  /**
   * Cleaned and formatted transcript of the user's previous answer.
   * This may be received via audio or as text input.
   * Required field, can be null if not applicable.
   */
  userAnswerTranscript: z.string().nullable(),
  
  /**
   * AI's internal thinking process for determining the bucket sort items.
   * Used to show reasoning and ensure quality categorization options.
   * Required field, can be null if not applicable.
   */
  scratchPad: z.string().nullable(),
  
  /**
   * The bucket sort question to pose to the user.
   * Should be clear and contextual, typically starts with "How would you categorize..."
   * Required field, can be null if not applicable.
   */
  nextQuestion: z.string().nullable(),
  
  /**
   * Array of 3 buckets for categorization (Winner/Loser/Neutral for trade-offs).
   * Each bucket has visual styling and clear labeling.
   */
  buckets: z.array(BucketSchema).length(3).describe('Three buckets for impact categorization'),
  
  /**
   * Array of 5-7 sortable items to be categorized into buckets.
   * Generated contextually based on the user's response and exercise type.
   * Each item represents a different impact or consequence of the trade-off.
   */
  items: z.array(SortableItemSchema).min(4).max(8).describe('4-8 contextual items to categorize'),
  
  /**
   * Title for the bucket sort activity.
   * Should provide clear categorization context.
   */
  title: z.string().describe('Title for the bucket sort activity'),
  
  /**
   * Whether all items must be sorted before proceeding.
   * Should be true to ensure complete categorization.
   */
  requireAllSorted: z.boolean().describe('Whether all items must be sorted before proceeding'),
});

export type Bucket = z.infer<typeof BucketSchema>;
export type SortableItem = z.infer<typeof SortableItemSchema>;
export type DebateResponseBucketSort = z.infer<typeof DebateResponseBucketSortSchema>;