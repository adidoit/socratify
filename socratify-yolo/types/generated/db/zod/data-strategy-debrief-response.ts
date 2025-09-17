import { z } from 'zod';

/**
 * Schema for Data exercise debrief with data strategy analysis
 * Used for analyzing user-defined data strategies and providing strategic refinement
 */

// Data strategy analysis point for insights/blindspots sections
export const DataAnalysisPointSchema = z.object({
  point: z.string().describe('Specific insight about what the data strategy reveals or misses'),
  explanation: z.string().describe('Brief explanation of why this point matters for decision-making'),
});

// Strategic data refinement in SocratifyTake format
export const DataStrategyRefinementSchema = z.object({
  title: z.string().describe('Pithy 2-4 word title for data strategy refinement focus'),
  text: z.string().describe('Strategic coaching with proposed alternative data approach in bold'),
});

// Complete response schema for data strategy debrief
export const DataStrategyDebriefResponseSchema = z.object({
  debrief: z.object({
    // User's proposed data approach context
    userDataApproach: z.string().describe('The data strategy or metrics the user proposed'),
    
    // Data strategy analysis (Page 1)
    insights: z.array(DataAnalysisPointSchema)
      .describe('What insights the user data strategy would reveal'),
    
    blindspots: z.array(DataAnalysisPointSchema)
      .describe('What blindspots or limitations the data strategy might have'),
    
    // Strategic refinement (Page 2)
    strategicRefinement: DataStrategyRefinementSchema
      .describe('Strategic coaching on improving the data approach with alternative proposal'),
      
    // Overall assessment
    dataStrategyQuality: z.object({
      comprehensivenessScore: z.number().min(1).max(5).describe('Overall comprehensiveness of the data strategy (1-5 scale)'),
      keyStrengths: z.array(z.string()).describe('Key strengths of the user data approach'),
      improvementAreas: z.array(z.string()).describe('Areas where the data strategy could be enhanced'),
      decisionReadiness: z.enum(['highly_actionable', 'somewhat_actionable', 'needs_refinement']).describe('How actionable the data would be for decision-making'),
    }).describe('Overall data strategy quality assessment'),
  }),
});

// Export types
export type DataAnalysisPoint = z.infer<typeof DataAnalysisPointSchema>;
export type DataStrategyRefinement = z.infer<typeof DataStrategyRefinementSchema>;
export type DataStrategyDebriefResponse = z.infer<typeof DataStrategyDebriefResponseSchema>;