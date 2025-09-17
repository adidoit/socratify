import { z } from 'zod';

/**
 * Schema for Fit Interview exercise debrief with culture dimension analysis
 * Used for company-specific culture fit assessment and interview coaching
 */

// Culture dimension assessment with clear strength indicators
export const CultureDimensionSchema = z.object({
  dimensionName: z.string().describe('Culture dimension name (e.g., "Customer Obsession", "Bias for Action")'),
  dimensionIcon: z.string().describe('Single emoji representing the dimension (e.g., "🚀", "💡")'),
  strengthLevel: z.enum(['strong', 'moderate', 'needs_growth']).describe('Assessment of user alignment with this dimension'),
  feedback: z.string().describe('Specific feedback about their examples and this dimension'),
});

// Interview improvement coaching in SocratifyTake format
export const InterviewCoachingSchema = z.object({
  title: z.string().describe('Pithy 2-4 word title for interview improvement focus'),
  text: z.string().describe('Specific coaching on strengthening culture fit with actionable examples'),
});

// Complete response schema for fit interview debrief
export const FitInterviewDebriefResponseSchema = z.object({
  debrief: z.object({
    // Company context
    companyName: z.string().describe('Company name for context (e.g., "Google", "Amazon")'),
    
    // Culture dimension assessments (Page 1)
    cultureDimensions: z.array(CultureDimensionSchema)
      .describe('Key culture dimensions with user assessments'),
    
    // Interview coaching (Page 2)
    interviewCoaching: InterviewCoachingSchema
      .describe('Specific guidance on strengthening culture fit for interviews'),
      
    // Overall culture fit summary
    overallFit: z.object({
      strongDimensionCount: z.number().describe('Number of dimensions showing strong fit'),
      readinessLevel: z.enum(['interview_ready', 'needs_preparation', 'significant_gaps']).describe('Overall interview readiness'),
      keyStrengths: z.array(z.string()).describe('Top culture alignment strengths'),
      growthAreas: z.array(z.string()).describe('Key areas for culture fit improvement'),
    }).describe('Overall culture fit assessment summary'),
  }),
});

// Export types
export type CultureDimension = z.infer<typeof CultureDimensionSchema>;
export type InterviewCoaching = z.infer<typeof InterviewCoachingSchema>;
export type FitInterviewDebriefResponse = z.infer<typeof FitInterviewDebriefResponseSchema>;