import { z } from 'zod';

export const ExerciseSkillModelSchema = z.object({
  id: z.number().int(),
  exerciseUuid: z.string(),
  skillUuid: z.string(),
  weight: z.number(),
  targetMinLevel: z.enum(['BEGINNER', 'APPRENTICE', 'PRACTITIONER', 'EXPERT', 'TOP_10']),
  targetMaxLevel: z.enum(['BEGINNER', 'APPRENTICE', 'PRACTITIONER', 'EXPERT', 'TOP_10']),
  createdAt: z.date(),
  updatedAt: z.date(),
});
