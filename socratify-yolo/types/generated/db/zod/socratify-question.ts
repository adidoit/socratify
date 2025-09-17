import { z } from 'zod';

export const SocratifyQuestionSchema = z.object({
  id: z.string(),
  text: z.string(),
  type: z.string(),
  timestamp: z.string(), // ISO-8601 string
  choices: z.array(z.object({
    title: z.string(),
    text: z.string(),
    correct: z.boolean().optional(),
  })).optional(),
  // Ranking-specific properties
  rankingItems: z.array(z.object({
    id: z.string(),
    text: z.string(),
    description: z.string().optional(),
  })).optional().describe('Items to be ranked by the user'),
  rankingInstructions: z.string().optional().describe('Instructions for how to rank the items'),
  isRanking: z.boolean().optional().describe('Whether this is a ranking-type question'),
});

export type SocratifyQuestion = z.infer<typeof SocratifyQuestionSchema>;

