import { z } from 'zod';

/**
 * Schema for Define Success exercise debrief with metric analysis
 * Used for analyzing user-defined success metrics and providing strategic refinement
 */

// Metric analysis point for captures/overlooks sections
export const MetricAnalysisPointSchema = z.object({
  point: z.string().describe('Specific insight about what the metric captures or overlooks'),
  explanation: z.string().describe('Brief explanation of why this point matters for the business'),
});

// Strategic refinement coaching in SocratifyTake format
export const StrategicRefinementSchema = z.object({
  title: z.string().describe('Pithy 2-4 word title for strategic refinement focus'),
  text: z.string().describe('Strategic coaching with proposed alternative metric in bold'),
});

// Complete response schema for define success debrief
export const DefineSuccessDebriefResponseSchema = z.object({
  debrief: z.object({
    // User's proposed metric context
    userMetric: z.string().describe('The success metric the user defined'),
    
    // Metric analysis (Page 1)
    captures: z.array(MetricAnalysisPointSchema)
      .describe('What the user metric effectively captures or measures'),
    
    overlooks: z.array(MetricAnalysisPointSchema)
      .describe('What the user metric might miss or overlook'),
    
    // Strategic refinement (Page 2)
    strategicRefinement: StrategicRefinementSchema
      .describe('Strategic coaching on improving the success metric with alternative proposal'),
      
    // Overall assessment
    metricQuality: z.object({
      strengthScore: z.number().min(1).max(5).describe('Overall strength of the proposed metric (1-5 scale)'),
      primaryStrengths: z.array(z.string()).describe('Key strengths of the user metric'),
      improvementAreas: z.array(z.string()).describe('Areas where the metric could be enhanced'),
      contextAppropriateness: z.enum(['highly_appropriate', 'somewhat_appropriate', 'needs_refinement']).describe('How well the metric fits the business context'),
    }).describe('Overall metric quality assessment'),
  }),
});

// Export types
export type MetricAnalysisPoint = z.infer<typeof MetricAnalysisPointSchema>;
export type StrategicRefinement = z.infer<typeof StrategicRefinementSchema>;
export type DefineSuccessDebriefResponse = z.infer<typeof DefineSuccessDebriefResponseSchema>;