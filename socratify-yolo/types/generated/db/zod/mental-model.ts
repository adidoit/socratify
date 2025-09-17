import { z } from 'zod';

const QuestionSchema = z.object({
  id: z.string(),
  text: z.string(),
  answer: z.string(),
  type: z.enum(['quick', 'deep']),
});

export const MentalModelSchema = z.object({
  mentalModelName: z.string(),
  mentalModelImageUrl: z.string().url(),
  mentalModelLinkText: z.string(),
  questions: z.array(QuestionSchema),
});

export type MentalModel = z.infer<typeof MentalModelSchema>;

