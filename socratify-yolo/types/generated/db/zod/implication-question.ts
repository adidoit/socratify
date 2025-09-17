import { z } from 'zod';

const ChoiceSchema = z.object({
  title: z.string(),
  text: z.string(),
  feedback: z.string(),
  correct: z.boolean(),
});

export const ImplicationQuestionSchema = z.object({
  question: z.string(),
  choices: z.array(ChoiceSchema),
});

export type ImplicationQuestion = z.infer<typeof ImplicationQuestionSchema>;

