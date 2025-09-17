import { z } from 'zod';
import { SkillOverridesSchema } from '../skill-overrides';

export const CuratedTrackExerciseModelSchema = z.object({
  id: z.number().int(),
  trackId: z.number().int(),
  levelId: z.number().int().optional(),
  exerciseUuid: z.string(),
  sequenceNumber: z.number().int(),
  createdAt: z.date(),
  updatedAt: z.date(),
  primarySkillUuid: z.string().optional(),
  selectionRationale: z.string(),
  skillFocusNote: z.string().optional(),
  skillOverrides: SkillOverridesSchema,
});
