import { z } from 'zod';

export const UserAnswerSchema = z.object({
  questionId: z.string(),
  answer: z.string(),
  timestamp: z.string(), // ISO-8601 string
  type: z.string(),
  selectedChoiceIndex: z.number().optional(),
});

export type UserAnswer = z.infer<typeof UserAnswerSchema>;

