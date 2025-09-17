import { z } from 'zod';

/**
 * Streamlined debrief response schema for v6 APIs
 * Optimized for single-card UX showing only growth opportunity
 */

// Growth opportunity dimension schema
export const GrowthOpportunitySchema = z.object({
  dimensionName: z.string().describe('Name of the dimension needing improvement'),
  dimensionImage: z.string().describe('Image identifier for the dimension'),
  dimensionScore: z.number().min(0).max(100).describe('Score for this dimension (0-100)'),
  dimensionFeedbackText: z.string().describe('Focused feedback for improvement with specific quotes and insights'),
});

// API endpoint response schema (what the mobile app receives)
export const StreamlinedDebriefApiResponseSchema = z.object({
  debrief: z.object({
    xpScore: z.number().describe('Experience points earned (0-100)'),
    growthOpportunity: GrowthOpportunitySchema.describe('The single most important area for improvement'),
  }),
  socratifyTake: z.union([
    z.string(),
    z.object({
      title: z.string().optional().describe('Pithy 2-4 word title capturing the deeper insight'),
      text: z.string().optional().describe('Main insight content'),
      insights: z.array(z.string()).optional().describe('Array of additional insights'),
    })
  ]).optional().describe('Socratify\'s take on the user\'s performance'),
});

// Library internal response schema (what the AI generation returns)
export const StreamlinedDebriefLibraryResponseSchema = z.object({
  debrief: z.object({
    xpScore: z.number(),
    growthOpportunity: GrowthOpportunitySchema,
  }),
});

export type GrowthOpportunity = z.infer<typeof GrowthOpportunitySchema>;
export type StreamlinedDebriefApiResponse = z.infer<typeof StreamlinedDebriefApiResponseSchema>;
export type StreamlinedDebriefLibraryResponse = z.infer<typeof StreamlinedDebriefLibraryResponseSchema>;