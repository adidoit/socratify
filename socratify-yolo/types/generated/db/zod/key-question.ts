import { z } from 'zod';

const KeyQuestionChoiceSchema = z.object({
  title: z.string(),
  text: z.string(),
  followUpQuestion: z.string(),
});

export const KeyQuestionSchema = z.object({
  keyQuestionRole: z.string(),
  keyQuestionText: z.string(),
  hintText: z.string(),
  shortKeyQuestionText: z.string(),
  choices: z.array(KeyQuestionChoiceSchema),
});

export type KeyQuestion = z.infer<typeof KeyQuestionSchema>;

