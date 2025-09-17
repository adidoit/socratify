import { z } from 'zod';

/**
 * Schema for Questions exercise debrief with quality analysis
 * Used for the custom 2-page debrief experience
 */

// Individual question analysis
export const QuestionAnalysisSchema = z.object({
  questionText: z.string().describe('Original user question'),
  questionType: z.enum(['FACTUAL', 'ANALYTICAL', 'STRATEGIC', 'HYPOTHETICAL'])
    .describe('Simplified type categorization for depth level'),
  score: z.string().describe('Quality score as string "1" through "5"'),
  feedback: z.string().describe('Specific feedback on why this question is good/bad and how to improve'),
  betterVersion: z.string().optional().describe('Improved version of the question (only provided for scores 1-3)'),
});

// The key strategic question in SocratifyTake format
export const DebriefKeyQuestionSchema = z.object({
  title: z.string().describe('Pithy 2-4 word title capturing the strategic angle'),
  text: z.string().describe('Combined question and explanation with markdown formatting'),
});

// Framework explanation for expert questions
export const FrameworkExplanationSchema = z.object({
  pattern: z.string().describe('Question pattern like "What if" or "Why not"'),
  purpose: z.string().describe('What this pattern achieves like "tests durability"'),
  detail: z.string().describe('Additional context like "Forces defensive thinking"'),
});

// Complete response schema for questions debrief
export const QuestionsDebriefResponseSchema = z.object({
  debrief: z.object({
    // Question Analysis + User Intent
    questionAnalyses: z.array(QuestionAnalysisSchema)
      .length(3)
      .describe('Analysis for each of the 3 questions'),
    userRationale: z.object({
      stated: z.string().describe('What the user said they were trying to do'),
      feedback: z.string().describe('Brief feedback on their approach'),
    }).describe('User\'s stated intent and our feedback on it'),
    
    // The Key Question (Single Strategic Focus)
    keyQuestion: DebriefKeyQuestionSchema
      .describe('The one most important strategic question they should have asked'),
  }),
  
  // Optional Socratify Take (may be used elsewhere or omitted)
  socratifyTake: z.union([
    z.string(),
    z.object({
      title: z.string().optional(),
      text: z.string().optional(),
    })
  ]).optional().describe('AI insight about the user\'s questioning approach'),
});

// Export types
export type QuestionAnalysis = z.infer<typeof QuestionAnalysisSchema>;
export type DebriefKeyQuestion = z.infer<typeof DebriefKeyQuestionSchema>;
export type QuestionsDebriefResponse = z.infer<typeof QuestionsDebriefResponseSchema>;