import { z } from 'zod';

/**
 * Common debrief response schemas used across debrief endpoints
 */

// Hot take response schema
export const HotTakeResponseSchema = z.object({
  hotTake: z.string().describe('AI-generated hot take or quick insight about user performance'),
});

// Socratify take response schema 
export const SocratifyTakeResponseSchema = z.object({
  socratifyTake: z.union([
    z.string(),
    z.object({
      // Can be either a string or structured object depending on API version
      text: z.string().optional(),
      insights: z.array(z.string()).optional(),
    })
  ]).describe('Socratify\'s structured take on the user\'s performance'),
});

// Rapid reaction response schema
export const RapidReactionResponseSchema = z.object({
  rapidReaction: z.string().describe('Quick initial reaction to user response (1-2 sentences)'),
  socratifyTake: z.string().describe('Expert analysis with key insights (2-3 sentences)'),
});

// Dimension feedback schema (for prioritized debriefs)
export const DimensionFeedbackSchema = z.object({
  dimensionName: z.string().describe('Name of the dimension being evaluated'),
  dimensionImage: z.string().describe('Image identifier for the dimension'),
  dimensionScore: z.number().min(0).max(100).describe('Score for this dimension (0-100)'),
  dimensionFeedbackText: z.string().describe('Personalized feedback text with specific quotes and insights'),
  priority: z.number().min(1).max(4).describe('Priority of this dimension (1 = most important, 4 = least)'),
  insightType: z.enum(['strength', 'weakness', 'opportunity', 'context']).describe('Type of insight provided'),
});

// Display configuration schema
export const DisplayConfigSchema = z.object({
  mode: z.enum(['single_focus', 'focused', 'balanced', 'comprehensive']).describe('Display mode based on engagement and performance'),
  primaryCount: z.number().describe('Number of dimensions to highlight prominently'),
  secondaryCount: z.number().optional().describe('Number of secondary dimensions to show'),
});

// Prioritized debrief response schema
export const PrioritizedDebriefResponseSchema = z.object({
  debrief: z.object({
    xpScore: z.string().describe('Experience points earned as string'),
    dimensions: z.array(DimensionFeedbackSchema).describe('Array of dimension feedback with priorities'),
    displayConfig: DisplayConfigSchema.describe('Configuration for how to display the debrief'),
  }),
  socratifyTake: SocratifyTakeResponseSchema.shape.socratifyTake.optional(),
});

// Generic debrief response schema (for simpler endpoints)
export const GenericDebriefResponseSchema = z.object({
  debrief: z.union([
    z.string(),
    z.object({
      text: z.string().optional(),
      score: z.number().optional(),
      feedback: z.string().optional(),
      dimensions: z.array(DimensionFeedbackSchema).optional(),
    })
  ]).describe('Debrief content - can be string or structured object'),
  socratifyTake: SocratifyTakeResponseSchema.shape.socratifyTake.optional(),
  hotTake: z.string().optional().describe('Optional hot take for the response'),
});

export type HotTakeResponse = z.infer<typeof HotTakeResponseSchema>;
export type SocratifyTakeResponse = z.infer<typeof SocratifyTakeResponseSchema>;
export type RapidReactionResponse = z.infer<typeof RapidReactionResponseSchema>;
export type DimensionFeedback = z.infer<typeof DimensionFeedbackSchema>;
export type DisplayConfig = z.infer<typeof DisplayConfigSchema>;
export type PrioritizedDebriefResponse = z.infer<typeof PrioritizedDebriefResponseSchema>;
export type GenericDebriefResponse = z.infer<typeof GenericDebriefResponseSchema>;